import json
import pprint
import pelops.logging.mylogger
from hippodamia.enums import Necessity
from hippodamia.enums import StatType
import hippodamia.agentshadow.states.state_machine
from hippodamia.agentshadow.states.event_ids import event_ids
from hippodamia.agentshadow.states.state_ids import state_ids
from hippodamia.agentshadow.messagearchive import MessageArchive
from hippodamia.agentshadow.logarchive import LogArchive
from hippodamia.agentshadow.properties import Properties


class AgentShadow:
    _mqtt_client = None
    _logger = None

    _state_machine = None

    _basic_topics = None
    _topic_cmd_reonboarding = None

    service_timings = None
    _agent_timings = None
    activity_topics = None

    message_archive = None
    log_archive = None
    properties = None
    states = None

    def __init__(self, topics, service_timings, agent_timings, mongo_client, mqtt_client, logger,
                 preload_config=None, gid=None):
        self._mqtt_client = mqtt_client
        self._logger = pelops.logging.mylogger.get_child(logger, "AgentShadow")
        self._basic_topics = topics
        self._topic_cmd_reonboarding = self._basic_topics["command-reonboarding"]
        self.service_timings = service_timings
        self._agent_timings = agent_timings

        self.properties = Properties(self._logger)

        if gid:
            self._logger.info("__init__ - setting gid")
            self.properties.gid = str(gid)
            self.properties.necessity = Necessity.SPONTANEOUS
        elif preload_config:
            self._process_preload_config(preload_config)
        else:
            self._logger.error("__init__ - preload_config and gid are None")
            raise ValueError("__init__ - preload_config and gid are None")

        if self.properties.gid is None:
            self._logger.error("__init__ - gid is None")
            raise ValueError("__init__ - gid is None")
        else:
            self._logger = pelops.logging.mylogger.get_child(logger, str(self.properties.gid))

        self.message_archive = MessageArchive()
        self.log_archive = LogArchive(set_health=self.properties.set_log_health)

        self._set_activity_topics()
        self._init_state_machine((preload_config is not None))

    def get_state_id(self):
        return self._state_machine.get_active_state().id

    def _set_activity_topics(self):
        self.activity_topics = {}
        activity_base = self._basic_topics["activity-base"]
        if activity_base[-1] == "/":
            activity_base = activity_base[:-1]
        self.activity_topics["ping"] = "{}/{}/ping".format(activity_base, self.properties.gid)
        self.activity_topics["runtime"] = "{}/{}/runtime".format(activity_base, self.properties.gid)
        self.activity_topics["config"] = "{}/{}/config".format(activity_base, self.properties.gid)
        self.activity_topics["end"] = "{}/{}/end".format(activity_base, self.properties.gid)
        self.activity_topics["logger"] = "{}/{}/logger".format(activity_base, self.properties.gid)

    def _process_preload_config(self, preload_config):
        self._logger.info("_process_preload_config - start")
        self._logger.debug("_process_preload_config: {}".format(preload_config))

        if "gid" in preload_config:
            self.properties.gid = str(preload_config["gid"])
        if "name" in preload_config:
            self.properties.name = preload_config["name"]
        if "location" in preload_config:
            self.properties.location = preload_config["location"]
        if "room" in preload_config:
            self.properties.room = preload_config["room"]
        if "device" in preload_config:
            self.properties.device = preload_config["device"]
        if "necessity" in preload_config:
            necessity = Necessity.get_enum(preload_config["necessity"])
            if necessity != Necessity.OPTIONAL and necessity != Necessity.REQUIRED:
                msg = "_process_preload_config - unexpected value '{}' for necessity. must " \
                      "be 'required' or 'optional'.",format(preload_config["necessity"])
                self._logger.error(msg)
                raise ValueError(msg)
            self.properties.necessity = necessity
        self._logger.info("_process_preload_config - finished")

    def _init_state_machine(self, predefined):
        self._state_machine, self.states = hippodamia.agentshadow.states.\
            state_machine.create(self.properties.gid, self.service_timings,
                                 self.properties.set_state_health,
                                 self.log_archive.reset_max_level, self._logger, predefined=predefined)
        self.states[state_ids.ONBOARDING].func_send_onboarding_response = self._send_onboarding_response
        self.states[state_ids.ONBOARDING].func_deactivate_recv_messages = self.deactivate_recv_messages
        self.states[state_ids.ONBOARDING].func_activate_recv_messages = self.activate_recv_messages
        self.states[state_ids.STOPPED].func_deactivate_recv_messages = self.deactivate_recv_messages

    def start(self):
        self._state_machine.start()

    def stop(self):
        try:
            # trying to initiate offboarding no matter what the current state is
            self._state_machine.asyncoperate(event_ids.OFFBOARDING)
        except KeyError:
            pass  # not every every state has a link to offboarding
        self._state_machine.stop()

    def prepare_for_archivation(self):
        self._logger.info("prepare for archivation - start")
        self._state_machine.operate(event_ids.ARCHIVE)
        if self.get_state_id() != state_ids.ARCHIVED:
            e = RuntimeError("transition to state 'ARCHIVE' failed. current state: '{}'".
                             format(self.get_state_id().name))
            self._logger.exception(e)
            raise e
        self._state_machine.stop()
        self.deactivate_recv_messages()
        self._logger.info("prepare for archivation - finished")

    def register_state_transistion_event_observer(self, observer):
        self._logger.info("register_state_transistion_event_observer - registering observer '{}'".format(observer))
        self._state_machine.register_state_transistion_event_observer(observer)

    def register_log_event_observer(self, observer):
        self._logger.info("register_log_event_observer - registering observer '{}'".format(observer))
        self.log_archive.register_log_event_observer(observer)

    def process_onboarding_request(self, message, session):
        """
        {
          "uuid": "550e8400-e29b-11d4-a716-446655440000",
          "onboarding-topic": "/hippodamia/550e8400-e29b-11d4-a716-446655440000",
          "protocol-version": 1,
          "timestamp": "1985-04-12T23:20:50.520Z",
          "identifier": {
            "last-gid": 1,
            "type": "DriverManager",
            "module": "copreus.drivermanager",
            "version": "0.3.1",
            "name": "display-driver",
            "location": "flat",
            "room": "living room",
            "device": "thermostat",
            "decription": "lorem ipsum",
            "host-name": "rpi",
            "node-id": "00-07-E9-AB-CD-EF",
            "ips": [
              "192.168.0.1",
              "10.0.1.2",
              "2001:0db8:85a3:08d3:1319:8a2e:0370:7344"
            ],
            "config-hash": "cf23df2207d99a74fbe169e3eba035e633b65d94"
          }
        }
        """
        self._logger.info("process_onboarding_request - start session '{}'".format(session))
        self._logger.debug("process_onboarding_request - message: {}".format(message))

        self.properties.session = session
        self.properties.uuid = message["uuid"]
        self.properties.onboarding_topic = message["onboarding-topic"]
        self.properties.protocol_version = message["protocol-version"]
        self.properties.time = message["timestamp"]

        self.properties.location = message["identifier"]["location"]
        self.properties.room = message["identifier"]["room"]
        self.properties.device = message["identifier"]["device"]

        self.properties.type = message["identifier"]["type"]
        self.properties.module = message["identifier"]["module"]
        self.properties.version = message["identifier"]["version"]
        self.properties.name = message["identifier"]["name"]
        self.properties.description = message["identifier"]["description"]
        self.properties.host_name = message["identifier"]["host-name"]
        self.properties.node_id = message["identifier"]["node-id"]
        self.properties.ips = message["identifier"]["ips"]
        self.properties.config_hash = message["identifier"]["config-hash"]

        self.message_archive.archive_request(message)
        self._logger.info("process_onboarding_request - finished")
        self._state_machine.asyncoperate(event_ids.ONBOARDING_REQUEST)
        
    def _send_onboarding_response(self):
        """
        {
            "uuid": "550e8400-e29b-11d4-a716-446655440000",
            "gid": 1,
            "session": 123,
            "topics-activity": {
                "ping": "/hippodamia/commands",
                "runtime": "/hippodamia/commands",
                "config": "/hippodamia/commands",
                "end": "/hippodamia/commands",
                "logger": "/hippodamia/commands"
            },
            "topics-commands": {
                "end": "/hippodamia/commands",
                "reonboarding": "/hippodamia/commands",
                "ping_on_request": "/hippodamia/commands",
                "config_on_request": "/hippodamia/commands",
                "runtime_on_request": "/hippodamia/commands",
                "heartbeat": "/hippodamia/commands"
            },
            "timings": {
                "send-ping": 60,
                "send-runtime": 500,
                "send-config": 3600,
                "expect-heartbeat": 120
            }
        }
        """
        message = {
            "uuid": self.properties.uuid,
            "gid": self.properties.gid,
            "session": self.properties.session,
            "topics-activity": {
                "ping": self.activity_topics["ping"],
                "runtime": self.activity_topics["runtime"],
                "config": self.activity_topics["config"],
                "end": self.activity_topics["end"],
                "logger": self.activity_topics["logger"],
            },
            "topics-commands": {
                "end": self._basic_topics["command-end"],
                "reonboarding": self._basic_topics["command-reonboarding"],
                "ping_on_request": self._basic_topics["command-ping-on-request"],
                "config_on_request": self._basic_topics["command-config-on-request"],
                "runtime_on_request": self._basic_topics["command-runtime-on-request"],
                "heartbeat": self._basic_topics["heartbeat"],
            },
            "timings": {
                "send-ping": self._agent_timings["send-ping"],
                "send-runtime": self._agent_timings["send-runtime"],
                "send-config": self._agent_timings["send-config"],
                "expect-heartbeat": self._agent_timings["expect-heartbeat"]
            }
        }
        message = json.dumps(message)
        self._logger.debug("_send_onboarding_response - topic: {}, message: {}"
                           .format(self.properties.onboarding_topic, message))
        self._logger.debug(self.properties.get_stats())
        self._mqtt_client.publish(self.properties.onboarding_topic, message)

    def activate_recv_messages(self):
        self._logger.info("activate_recv_messages")

        self._logger.debug("activate_recv_messages - topic ping {}".format(self.activity_topics["ping"]))
        self._mqtt_client.subscribe(self.activity_topics["ping"], self._handler_ping, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic runtime {}".format(self.activity_topics["runtime"]))
        self._mqtt_client.subscribe(self.activity_topics["runtime"], self._handler_runtime, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic config {}".format(self.activity_topics["config"]))
        self._mqtt_client.subscribe(self.activity_topics["config"], self._handler_config, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic end {}".format(self.activity_topics["end"]))
        self._mqtt_client.subscribe(self.activity_topics["end"], self._handler_end, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic logger {}".format(self.activity_topics["logger"]))
        self._mqtt_client.subscribe(self.activity_topics["logger"], self._handler_logger, ignore_duplicate=True)

    def deactivate_recv_messages(self):
        self._logger.info("deactivate_recv_messages")

        self._logger.debug("activate_recv_messages - topic ping {}".format(self.activity_topics["ping"]))
        self._mqtt_client.unsubscribe(self.activity_topics["ping"], self._handler_ping, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic runtime {}".format(self.activity_topics["runtime"]))
        self._mqtt_client.unsubscribe(self.activity_topics["runtime"], self._handler_runtime, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic config {}".format(self.activity_topics["config"]))
        self._mqtt_client.unsubscribe(self.activity_topics["config"], self._handler_config, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic end {}".format(self.activity_topics["end"]))
        self._mqtt_client.unsubscribe(self.activity_topics["end"], self._handler_end, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic logger {}".format(self.activity_topics["logger"]))
        self._mqtt_client.unsubscribe(self.activity_topics["logger"], self._handler_logger, ignore_not_found=True)

    def _check_session(self, message):
        if self.properties.session != message["session"]:
            self._logger.warning("agentshadow.session != message.session ({} != {})"
                                 .format(self.properties.session, message["session"]))
            message = {
                "request": "reonboarding",
                "gid": self.properties.gid
            }
            payload = json.dumps(message)
            self._logger.info("_check_session - sending reonboarding request to gid '{}'".format(self.properties.gid))
            self._mqtt_client.publish(self._topic_cmd_reonboarding, payload)

    def _handler_ping(self, message):
        self._logger.info("_handler_ping - received ping")
        message = json.loads(message.decode("utf8"))
        self._check_session(message)
        self.message_archive.archive_ping(message)
        self.properties.service_uptime = message["service-uptime"]
        self._resettimer_or_regularmessage()

    def _handler_runtime(self, message):
        self._logger.info("_handler_runtime - received runtime")
        message = json.loads(message.decode("utf8"))
        self.message_archive.archive_runtime(message)
        self.properties.service_uptime = message["service-uptime"]
        self._resettimer_or_regularmessage()

    def _handler_config(self, message):
        self._logger.info("_handler_config - received config")
        message = json.loads(message.decode("utf8"))
        self.message_archive.archive_config(message)
        self.properties.service_uptime = message["service-uptime"]
        self._resettimer_or_regularmessage()

    def _handler_logger(self, message):
        self._logger.info("_handler_logger - received logger")
        message = json.loads(message.decode("utf8"))
        self.message_archive.archive_logger(message)
        self.log_archive.add(message)
        self._resettimer_or_regularmessage()

    def _resettimer_or_regularmessage(self):
        active_state = self._state_machine.get_active_state()
        if active_state.id == state_ids.ACTIVE:
            self._logger.info("current state is 'ACTIVE' -> reset timeout timer")
            self._state_machine.restarttimeoutevent()
        else:
            self._logger.info("current state is '{}' -> trigger event REGULAR_MESSAGE".format(active_state.id))
            self._state_machine.asyncoperate(event_ids.REGULAR_MESSAGE)

    def _handler_end(self, message):
        self._logger.info("_handler_end - received end")
        message = json.loads(message.decode("utf8"))
        self.message_archive.archive_end(message)
        self._state_machine.asyncoperate(event_ids.OFFBOARDING)

    def _get_general_stats(self):
        stats = dict()

        stats["micro-service"] = {
            "name": self.properties.name,
            "module": self.properties.module,
            "type": self.properties.type,
            "uptime": self.properties.service_uptime,
            "session": self.properties.session,
            "health": self.properties.health.name
        }

        stats["active-state"] = self._state_machine.get_stats_active_state()

        stats["message-stats"] = {}
        for id, gs in self.message_archive.get_stats().items():
            stats["message-stats"][id] = gs["counter"]

        stats["topics"] = {}
        for id, topic in self.activity_topics.items():
            stats["topics"][id] = topic

        stats["timings"] = {}
        for id, timing in self.service_timings.items():
            stats["timings"][id] = timing

        return stats

    def _get_state_stats(self):
        stats = dict()
        for k, v in self.states.items():
            stats[k.name] = v.get_stats()
        return stats

    def get_stats(self):
        stats = {
            "general": self._get_general_stats(),
            "states": self._get_state_stats(),
            "state_machine": self._state_machine.get_stats(),
            "properties": self.properties.get_stats(),
            "messages": self.message_archive.get_stats(full=False),
            "logger": self.log_archive.get_stats(full=False)
        }

        return stats

    def get_string_stats(self, stat_type):
        stats = self.get_stats()
        output = ""

        if stat_type == StatType.GENERAL or stat_type == StatType.ALL:
            output += "general: \n"
            output += pprint.pformat(stats["general"], indent=4)
            output += "\n\n"

        if stat_type == StatType.STATE_MACHINE or stat_type == StatType.ALL:
            output += "state-machine:\n"
            output += pprint.pformat(stats["state_machine"], indent=4)
            output += "\n\n"

        if stat_type == StatType.PROPERTIES or stat_type == StatType.ALL:
            output += "properties: @{}\n".format(stats["properties"]["time"])
            output += pprint.pformat(stats["properties"]["entries"], indent=4)
            output += "\n\n"

        if stat_type == StatType.LOGGER or stat_type == StatType.ALL:
            output += "logger:\n"
            output += pprint.pformat(stats["logger"], indent=4)
            output += "\n\n"

        if stat_type == StatType.MESSAGES or stat_type == StatType.ALL:
            output += "messages:\n"
            output += pprint.pformat(stats["messages"], indent=4)
            output += "\n\n"

        if output == "":
            output = "get_string_stats: unknown stat type '{}'\n".format(type)

        return output

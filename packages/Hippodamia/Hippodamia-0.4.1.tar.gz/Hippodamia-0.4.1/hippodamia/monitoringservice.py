import threading
import json

from pelops.abstractmicroservice import AbstractMicroservice
import hippodamia
from hippodamia.agentshadow.agentshadowfactory import AgentShadowFactory
from hippodamia.mymongoclient import MyMongoClient
from hippodamia.heartbeat import Heartbeat
from hippodamia.commands import CommandFactory
from hippodamia.schema.monitoringservice import get_schema
from hippodamia.hierarchivalview.hierarchicalview import HierarchicalView
from hippodamia.enums import Enforcement
from hippodamia.onboarding import Onboarding
from hippodamia.flask.server import FlaskServer
from hippodamia.agentshadow.states.state_ids import state_ids
from hippodamia.email.emailnotification import EmailNotification


class Monitoringservice(AbstractMicroservice):
    _version = hippodamia.version

    _protocol_version = 1

    _agentshadows = None
    _agentshadow_archive = None
    _asfactory = None
    _mongo_client = None
    _heartbeat = None
    _hierarchical_view = None
    _onboarding = None
    _flask_server = None
    _email_notification = None

    _enforcement = None

    _topic_onboarding_request = None
    _topic_cmd_ping = None
    _topic_cmd_runtime = None
    _topic_cmd_config = None
    _topic_cmd_reonboarding = None
    _topic_cmd_end = None

    _initial_reonboarding_request = None

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """
        forced_monitoring_agent_publishloglevel = False
        try:
            ll = config["monitoring-agent"]["publish-log-level"]
            if ll.upper() == "DEBUG" or ll.upper() == "INFO":
                config["monitoring-agent"]["publish-log-level"] = "WARNING"
                forced_monitoring_agent_publishloglevel = True
        except KeyError:
            pass

        AbstractMicroservice.__init__(self, config, "monitoringservice", mqtt_client, logger,
                                      logger_name=__class__.__name__, stdout_log_level=stdout_log_level, no_gui=no_gui)

        if forced_monitoring_agent_publishloglevel:
            self._logger.warning("forced 'monitoring-agent.publish-log-level' of monitoring agent to be 'warning' or "
                                 "higher. as every action of a monitoring agent results in corresponding actions in "
                                 "the monitoring service which in this case would trigger logging events in its "
                                 "monitoring agent which would then trigger again an update in the monitoring "
                                 "service ...")
        try:
            self._mongo_client = MyMongoClient(self._config["mongodb"], self._logger)
        except KeyError:
            self._logger.info("no entry 'mongodb' in config -> no mongodb will be used")

        self._heartbeat = Heartbeat(self._config["topics"]["heartbeat"],
                                    self._config["service-timings"]["heartbeat_interval"],
                                    self._mqtt_client, self._logger)

        self._topic_onboarding_request = self._config["topics"]["onboarding-request"]
        self._topic_cmd_ping = self._config["topics"]["command-ping-on-request"]
        self._topic_cmd_runtime = self._config["topics"]["command-runtime-on-request"]
        self._topic_cmd_config = self._config["topics"]["command-config-on-request"]
        self._topic_cmd_reonboarding = self._config["topics"]["command-reonboarding"]
        self._topic_cmd_end = self._config["topics"]["command-end"]

        self._asfactory = AgentShadowFactory(self._config["topics"], self._config["service-timings"],
                                             self._config["agent-timings"],
                                             self._config["expected-services"]["services"],
                                             self._mongo_client, self._mqtt_client, self._logger)
        self._agentshadows = {}
        self._asfactory.add_predefined_shadows(self._agentshadows)
        self._agentshadow_archive = []

        self._hierarchical_view = HierarchicalView(self._agentshadows, self._logger)

        self._enforcement = Enforcement.get_enum(self._config["expected-services"]["enforcement"])
        self._onboarding = Onboarding(self._protocol_version, self._topic_onboarding_request, self._enforcement,
                                      self._agentshadows, self._asfactory, self._mqtt_client, self._logger)

        try:
            self._email_notification = EmailNotification(self._config["email"], self._logger, self._mqtt_client,
                                                         self._agentshadows, self._heartbeat, self._hierarchical_view,
                                                         self._onboarding, self._agentshadow_archive, self._asfactory)
        except KeyError:
            self._logger.info("no entry 'email' in config -> email notification is disabled")

        if "webserver" in self._config:
            self._flask_server = FlaskServer(self._config["webserver"], self._logger, self._agentshadows,
                                             self._agentshadow_archive, self._heartbeat, self._hierarchical_view,
                                             self._onboarding, self.send_cmd_ping, self.send_cmd_runtime,
                                             self.send_cmd_config, self.send_cmd_reonboarding, self.send_cmd_end,
                                             self._full_config, self._mqtt_client, self.archive_agentshadows,
                                             self.purge_agentshadow_archive, self.acknowledge_log,
                                             self._email_notification)
        else:
            self._logger.info("no entry 'webserver' in config -> no webserver will be created")

        factory = CommandFactory(self._version, self._config, self._agentshadows, self._heartbeat,
                                 self._hierarchical_view, self._onboarding, self.send_cmd_ping, self.send_cmd_runtime,
                                 self.send_cmd_config, self.send_cmd_reonboarding, self.send_cmd_end,
                                 self._agentshadow_archive, self._email_notification, self._logger)
        factory.add_commands(self._add_ui_command)

    def _start(self):
        if self._flask_server is not None:
            self._flask_server.start()
        if self._mongo_client is not None:
            self._mongo_client.start()
        self._heartbeat.start()
        for k, v in self._agentshadows.items():
            v.start()
        self._hierarchical_view.start()
        if self._email_notification is not None:
            self._email_notification.start()
        self._onboarding.start()
        self.send_cmd_reonboarding()

    def _stop(self):
        self._heartbeat.stop()
        self._onboarding.stop()
        if self._email_notification is not None:
            self._email_notification.stop()
        self.send_cmd_end(gid=None)  # inform everyone that the service is going down
        self._hierarchical_view.stop()
        for k, v in self._agentshadows.items():
            print("stopping {}".format(k))
            v.stop()
        if self._mongo_client is not None:
            self._mongo_client.stop()
        if self._flask_server is not None:
            self._flask_server.stop()

    def archive_agentshadows(self):
        """remove all agentshadows in state 'ARCHIVECANDIDATE' from agentshadows, deactivate them and move them to
        a seperate list"""

        self._logger.info("archivation of shadows - start")
        self._logger.debug("collect list of to be archived shadows")
        candidates = {}
        for gid, agentshadow in self._agentshadows.items():
            if agentshadow.get_state_id() == state_ids.ARCHIVECANDIDATE:
                candidates[gid] = agentshadow

        self._logger.debug("archive these shadows: {}".format(candidates.keys()))

        for gid, agentshadow in candidates.items():
            agentshadow.prepare_for_archivation()
            del self._agentshadows[gid]
            self._agentshadow_archive.append(agentshadow)

        self._logger.info("archivation of shadows (added: {}) - finished".format(len(candidates)))
        self._asfactory.add_predefined_shadows(self._agentshadows)

        return len(candidates)

    def purge_agentshadow_archive(self):
        counter = len(self._agentshadow_archive)
        self._logger.info("purging of agendshadow archive - removing {} entries".format(counter))
        self._agentshadow_archive.clear()
        return counter

    @classmethod
    def _get_description(cls):
        return "Hippodamia observes the state of all registered microservices (aka watch dog)."

    @classmethod
    def _get_schema(cls):
        return get_schema()

    def runtime_information(self):
        info = {}
        for gid, shadow in self._agentshadows.items():
            entry = {
                "gid": gid,
                "state": shadow.get_state_id().name,
                "health": shadow.properties.health.name,
                "necessity": shadow.properties.necessity.name,
                "properties": shadow.properties.name
            }
            info[gid] = entry
        return info

    def config_information(self):
        return {}

    def acknowledge_log(self, gid=None):
        counter = 0
        if gid is None:
            self._logger.info("acknowledge_log: all agentshadows")
            for g, a in self._agentshadows.items():
                self._logger.debug("acknowledge_log: gid: {}".format(g))
                a.log_archive.reset_max_level()
                counter += 1
        elif not gid in self._agentshadows:
            self._logger.info("acknowledge_log: unknown gid")
        else:
            self._logger.info("acknowledge_log: gid: {}".format(gid))
            self._agentshadows[gid].log_archive.reset_max_level()
            counter += 1
        return counter

    @staticmethod
    def _render_message(request, gid):
        """
        {
            "request": "request",
            "gid": 1
        }
        """
        message = {
            "request": request
        }
        if gid is not None:
            message["gid"] = gid
        return json.dumps(message)

    def send_cmd_ping(self, gid=None):
        if gid is None:
            self._logger.info("send_cmd_ping: send request to all monitored services")
        else:
            self._logger.info("send_cmd_ping: send request to gid: {}".format(gid))
        message = self._render_message("ping", gid)
        self._mqtt_client.publish(self._topic_cmd_ping, message)

    def send_cmd_runtime(self, gid=None):
        if gid is None:
            self._logger.info("send_cmd_runtime: send request to all monitored services")
        else:
            self._logger.info("send_cmd_runtime: send request to gid: {}".format(gid))
        message = self._render_message("runtime", gid)
        self._mqtt_client.publish(self._topic_cmd_runtime, message)

    def send_cmd_config(self, gid=None):
        if gid is None:
            self._logger.info("send_cmd_config: send request to all monitored services")
        else:
            self._logger.info("send_cmd_config: send request to gid: {}".format(gid))
        message = self._render_message("config", gid)
        self._mqtt_client.publish(self._topic_cmd_config, message)

    def send_cmd_reonboarding(self, gid=None):
        if gid is None:
            self._logger.info("send_cmd_reonboarding: send request to all monitored services")
        else:
            self._logger.info("send_cmd_reonboarding: send request to gid: {}".format(gid))
        message = self._render_message("reonboarding", gid)
        self._mqtt_client.publish(self._topic_cmd_reonboarding, message)

    def send_cmd_end(self, gid=None):
        if gid is None:
            self._logger.info("send_cmd_end: send request to all monitored services")
        else:
            self._logger.info("send_cmd_end: send request to gid: {}".format(gid))
        message = self._render_message("end", gid)
        self._mqtt_client.publish(self._topic_cmd_end, message)


def standalone():
    Monitoringservice.standalone()


if __name__ == "__main__":
    Monitoringservice.standalone()

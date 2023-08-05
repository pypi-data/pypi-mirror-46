import datetime
import pprint
from hippodamia.enums import Enforcement
from hippodamia.agentshadow.states.state_ids import state_ids
import json
import pelops.logging.mylogger
from threading import Lock
import collections


class _GIDMapping:
    location = None
    room = None
    device = None
    type = None
    name = None

    def __init__(self, location=None, room=None, device=None, type=None, name=None):
        self.location = location
        self.room = room
        self.device = device
        self.type = type
        self.name = name

    def complete(self):
        return (self.location is not None
                and self.room is not None
                and self.device is not None
                and self.type is not None
                and self.name is not None)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.location == other.location \
               and self.room == other.room \
               and self.device == other.device \
               and self.type == other.type and self.name == other.name


class Onboarding:
    _logger = None
    _mqtt_client = None
    _agentshadows = None
    _asfactory = None
    _lock = None

    enforcement = None
    protocol_version = None
    topic_onboarding_request = None
    counter = 0
    gid_list = None
    last_timestamp = None
    messages = None
    gid_blacklist = None

    def __init__(self, protocol_version, topic_onboarding_request, enforcement, agentshadows, asfactory, mqtt_client, logger):
        self.protocol_version = protocol_version
        self._logger = pelops.logging.mylogger.get_child(logger, __class__.__name__)
        self._mqtt_client = mqtt_client
        self.enforcement = enforcement
        self._agentshadows = agentshadows
        self._asfactory = asfactory
        self.gid_list = {}
        self.gid_blacklist = []
        self.topic_onboarding_request = topic_onboarding_request
        self._lock = Lock()
        self.messages = collections.deque(maxlen=50)
        self._logger.info("__init__ done")

    def start(self):
        self._mqtt_client.subscribe(self.topic_onboarding_request, self._handler_onboarding_request)
        self._logger.info("subscribed to {}".format(self.topic_onboarding_request))

    def stop(self):
        self._mqtt_client.unsubscribe(self.topic_onboarding_request, self._handler_onboarding_request)
        self._logger.info("unsubscribed from {}".format(self.topic_onboarding_request))

    def _generate_unique_id(self, gid_mapping):
        if gid_mapping.type is None or gid_mapping.type == "":
            raise ValueError("value of gid_mapping.type must be set.")
        suffix = 0
        while True:
            new_gid = "{}-{}".format(gid_mapping.type, suffix)
            if new_gid not in self.gid_list.keys():
                return new_gid
            suffix += 1

    def _last_gid_ok(self, last_gid, gid_mapping):
        if last_gid is None or last_gid == "":
            # last_gid is not a valid identifier
            return False
        if last_gid in self.gid_list:
            last_mapping = self.gid_list[last_gid]
            if gid_mapping == last_mapping:
                # last_gid's mapping values are identical to the one from the requesting service
                return True
            else:
                # last_gid in use by a different microservice
                return False
        # last_gid is unknown
        return True

    def _get_gid_for_gidmapping(self, gid_mapping):
        for gid, gm in self.gid_list.items():
            if gm == gid_mapping:
                return gid
        return None

    def _is_known_gid_stopped(self, gid):
        try:
            state_id = self._agentshadows[gid].get_state_id()
            if not(state_id == state_ids.STOPPED or state_id == state_ids.ARCHIVED):
                return False
        except KeyError:
            pass
        return True

    def _same_session_id(self, gid, last_session):
        try:
            session = self._agentshadows[gid].properties.session
            if session is None or session == last_session:
                return True
        except KeyError:
            pass
        return False

    def _get_gid(self, identifier):
        gid_mapping = _GIDMapping(location=identifier["location"], room=identifier["room"], device=identifier["device"],
                                  type=identifier["type"], name=identifier["name"])
        gid = None
        self._logger.debug("_get_gid - gid_mapping: location={}, room={}, device={}, type={}, name={}; complete={}"
                           .format(gid_mapping.location, gid_mapping.room, gid_mapping.device, gid_mapping.type,
                                   gid_mapping.name, gid_mapping.complete()))

        if gid_mapping.complete():
            if self._last_gid_ok(identifier["last-gid"], gid_mapping):
                self._logger.debug("_get_gid - _last_gid_ok('{}') == True".format(identifier["last-gid"]))
                gid = identifier["last-gid"]
            else:
                gid = self._get_gid_for_gidmapping(gid_mapping)
                self._logger.debug("_get_gid - gid for gidmapping={}".format(gid))

        if not self._is_known_gid_stopped(gid) and not self._same_session_id(gid, identifier["last-session"]):
            self._logger.debug("_get_gid - agentshadow for gid {} is active (state: {}) and session ids do not match "
                               "(last-session: {})"
                               .format(gid, self._agentshadows[gid].get_state_id(), identifier["last-session"]))
            gid = None

        if gid in self.gid_blacklist:
            self._logger.debug("_get_gid - gid {} is blacklisted".format(gid))
            gid = None

        if gid is None:
            gid = self._generate_unique_id(gid_mapping)
            self._logger.debug("_get_gid - generated unique id")
            self.gid_list[gid] = gid_mapping

        self._logger.info("_get_gid - gid: {}".format(gid))
        return gid

    def _handler_onboarding_request(self, message):
        """
        {
            "uuid": "550e8400-e29b-11d4-a716-446655440000",
            "onboarding-topic": "/hippodamia/550e8400-e29b-11d4-a716-446655440000",
            "protocol-version": 1,
            "timestamp": "1985-04-12T23:20:50.520Z",
            "identifier": {
                "last-gid": "copreus-1",
                "type": "DriverManager",
                "module": "copreus.drivermanager",
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
        with self._lock:
            message = message.decode("utf8")
            message = json.loads(message)
            self._logger.info("_handler_onboarding_request - received request")
            self._logger.debug("_handler_onboarding_request - message: {}".format(message))

            self.counter += 1
            self.last_timestamp = datetime.datetime.now()
            self.messages.append({"time": self.last_timestamp, "message": message})

            if message["protocol-version"] != self.protocol_version:
                message = "handler_onboarding_request - expected protocol version {}, message: {}"\
                    .format(self.protocol_version, message)
                self._logger.error(message)
            else:
                identifier = message["identifier"]
                self._logger.debug("_handler_onboarding_request - identifier: {}".format(identifier))
                gid = self._get_gid(identifier)

                shadow = None
                if gid not in self._agentshadows:
                    self._logger.debug("_handler_onboarding_request - unknown gid")
                    if self.enforcement == Enforcement.NONE:
                        self._logger.debug("_handler_onboarding_request - Enforcement.NONE")
                        shadow = self._asfactory.new_agentshadow(gid=gid)
                        self._agentshadows[gid] = shadow
                        shadow.start()
                    elif self.enforcement == Enforcement.IGNORE:
                        self._logger.debug("_handler_onboarding_request - Enforcement.IGNORE")
                        return
                    elif self.enforcement == Enforcement.STRICT:
                        self._logger.debug("_handler_onboarding_request - Enforcement.STRICT")
                        self._logger.error("handler_onboarding_request - required is set to strict and incoming is gid "
                                           "not pre-configured. '{}'".format(message))
                        return
                    else:
                        message = "handler_onboarding_request - dont know how to handler required '{}'"\
                            .format(self.enforcement)
                        self._logger.error(message)
                        raise ValueError(message)
                else:
                    self._logger.debug("_handler_onboarding_request - existing gid {}".format(gid))
                    shadow = self._agentshadows[gid]

                self._logger.debug("_handler_onboarding_request - {}".format(shadow))
                shadow.process_onboarding_request(message, session=self.counter)

    def get_stats(self, full=True):
        gid_list = list(self.gid_list.keys())
        gid_list.sort()

        stats = {
            "counter": self.counter,
            "stored": len(self.messages),
            "gid_list": gid_list,
            "enforcement": self.enforcement.name,
            "protocol_version": self.protocol_version,
            "topic_onboarding_request": self.topic_onboarding_request,
            "last_timestamp": self.last_timestamp
        }
        if full:
            stats["messages"] = self.messages
        return stats

    def get_string_stats(self):
        output = ""
        output += "stats:\n{}\n".format(pprint.pformat(self.get_stats(full=False), indent=4))
        try:
            output += "last message:\n{}\n".format(pprint.pformat(self.messages[-1], indent=4))
        except IndexError:
            output += "last message: n/a\n"

        return output

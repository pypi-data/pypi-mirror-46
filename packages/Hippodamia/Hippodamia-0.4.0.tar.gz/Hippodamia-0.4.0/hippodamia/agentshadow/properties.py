from hippodamia.enums import Health, Necessity
import logging


class Properties:
    _logger = None

    gid = None
    necessity = None
    type = None
    module = None
    name = None
    location = None
    room = None
    device = None
    uuid = None
    onboarding_topic = None
    session = None
    protocol_version = None
    version = None
    description = None
    host_name = None
    node_id = None
    ips = None
    config_hash = None
    service_uptime = None
    state_health = None
    log_health = None
    time = None

    def __init__(self, logger):
        self._logger = logger

    def get_stats(self):
        try:
            health = self.health.name
        except AttributeError:
            health = None
        try:
            necessity = self.necessity.name
        except AttributeError:
            necessity = None

        result = {
            "time": self.time,
            "entries": {
                "gid": self.gid,
                "session": self.session,
                "health": {
                    "overall": health,
                    "state": self.state_health.name,
                    "log": self.log_health.name
                },
                "necessity": necessity,
                "uuid": self.uuid,
                "onboarding_topic": self.onboarding_topic,
                "protocol_version": self.protocol_version,
                "type": self.type,
                "module": self.module,
                "version": self.version,
                "name": self.name,
                "location": self.location,
                "room": self.room,
                "device": self.device,
                "description": self.description,
                "host_name": self.host_name,
                "node_id": self.node_id,
                "ips": self.ips,
                "config_hash": self.config_hash,
                "service_uptime": self.service_uptime
            }
        }
        return result

    def _get_health(self):
        try:
            result = max(self.log_health, self.state_health)
        except TypeError:
            try:
                result = max(self.log_health)
            except TypeError:
                try:
                    result = max(self.state_health)
                except TypeError:
                    result = Health.RED
        return result

    health = property(fget=_get_health)

    def set_state_health(self, health):
        if self.necessity == Necessity.REQUIRED:
            self.state_health = health
        else:
            self.state_health = min(Health.YELLOW, health)
        self._logger.debug("set_state_health to {} (original: {})"
                           .format(self.state_health.name, health.name))

    def set_log_health(self, max_level):
        if max_level >= logging.ERROR:
            self.log_health = Health.RED
        else:
            self.log_health = Health.GREEN
        self._logger.debug("set_log_health to {} (level: {})"
                           .format(self.log_health.name, logging.getLevelName(max_level)))

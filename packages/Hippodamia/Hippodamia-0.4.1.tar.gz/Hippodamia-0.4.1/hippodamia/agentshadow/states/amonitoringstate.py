import datetime
from tantamount.astate import AState
import pelops.logging.mylogger


class AMonitoringState(AState):
    logger = None
    counter_on_exit = 0
    counter_on_entry = 0
    timestamp_on_entry = None
    timestamp_on_exit = None
    set_health = None
    health = None
    reset_max_level = None

    def __init__(self, id, set_health, health, reset_max_level, logger, logger_name, group_id):
        AState.__init__(self, id, groupid=group_id)
        self.logger = pelops.logging.mylogger.get_child(logger, logger_name)
        self.logger.debug("__init__ ")
        self.set_health = set_health
        self.health = health
        self.reset_max_level = reset_max_level

    def on_entry(self):
        self.logger.info("on_entry")
        self.counter_on_entry += 1
        self.timestamp_on_exit = None
        self.timestamp_on_entry = datetime.datetime.now()

        self.set_health(self.health)
        next = self._on_entry()

        if next is not None:
            self.logger.debug("on_entry - event: {}".format(next.name))
        return next

    def _on_entry(self):
        return None

    def on_exit(self):
        self.logger.info("on_exit")
        self.counter_on_exit += 1
        self.timestamp_on_exit = datetime.datetime.now()

        self._on_exit()

    def _on_exit(self):
        pass

    def get_stats(self):
        try:
            duration = self.timestamp_on_exit - self.timestamp_on_entry
        except TypeError:
            try:
                duration = datetime.datetime.now() - self.timestamp_on_entry
            except TypeError:
                duration = "-"

        try:
            str_time_on_entry = self.timestamp_on_entry.strftime("%Y-%m-%dT%H:%M:%S")
        except AttributeError:
            str_time_on_entry = None

        try:
            str_time_on_exit = self.timestamp_on_entry.strftime("%Y-%m-%dT%H:%M:%S")
        except AttributeError:
            str_time_on_exit = None

        try:
            float_duration = duration.total_seconds()
        except AttributeError:
            float_duration = None

        stats = {
            "counter_on_entry": self.counter_on_entry,
            "timestamp_on_entry": str_time_on_entry,
            "counter_on_exit": self.counter_on_exit,
            "timestamp_on_exit": str_time_on_exit,
            "duration": float_duration
        }
        return stats

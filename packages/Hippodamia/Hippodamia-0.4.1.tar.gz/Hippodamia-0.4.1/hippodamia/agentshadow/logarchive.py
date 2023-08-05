import collections
import datetime
import pprint
from pelops.logging.mylogger import get_log_level
from pelops.logging.mylogger import get_level_name
import logging


class _ArchiveEntry:
    log = None
    counter = None
    time = None

    def __init__(self, maxlen):
        self.log = collections.deque(maxlen=maxlen)
        self.counter = 0

    def add(self, message):
        self.log.appendleft(message)
        self.counter += 1
        self.time = datetime.datetime.now()

    def get_stats(self):
        try:
            at = self.time.strftime("%Y-%m-%dT%H:%M:%S")
        except AttributeError:
            at = None
        return {
                   "received": self.counter,
                   "stored": len(self.log),
                   "time": at
               }

class LogArchive:
    flat_list = None
    level_dict = None
    max_level = None
    set_health = None
    _observer = None

    def __init__(self, maxlen=50, set_health=None):
        self.set_health = set_health
        self.reset_max_level()
        self.flat_list = _ArchiveEntry(maxlen)
        self.level_dict = collections.defaultdict(lambda: _ArchiveEntry(maxlen))

    def register_log_event_observer(self, observer):
        self._observer = observer

    def add(self, message):
        self.flat_list.add(message)
        level = get_log_level(message["level"])
        self.level_dict[level].add(message)
        self.max_level = max(self.max_level, level)
        self.set_health(self.max_level)
        if self._observer:
            self._observer(message["gid"], message["level"])

    def reset_max_level(self):
        self.max_level = logging.NOTSET
        self.set_health(self.max_level)

    def get_stats(self, full=True):
        stats = {
            "max_level": self.max_level,
            "logs": {
                "flat_list": {
                    "stats": self.flat_list.get_stats(),
                }
            }
        }
        if full:
            stats["logs"]["flat_list"]["entries"] = self.flat_list.log

        levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        for k in levels:
            stats["logs"][get_level_name(k)] = {
                "stats": self.level_dict[k].get_stats()
            }
            if full:
                stats["logs"][get_level_name(k)]["entries"] = self.level_dict[k].log

        return stats

    def get_string_stats(self, key):
        output = ""
        
        if key.lower() == "flat":
            key = "flat_list"
        elif key.lower() == "debug":
            key = get_level_name(logging.DEBUG)
        elif key.lower() == "info":
            key = get_level_name(logging.INFO)
        elif key.lower() == "warning":
            key = get_level_name(logging.WARNING)
        elif key.lower() == "error":
            key = get_level_name(logging.ERROR)
        elif key.lower() == "critical":
            key = get_level_name(logging.CRITICAL)
        else:
            raise ValueError("get_string_stats - unknown argument value '{}'".format(key))

        logs = self.get_stats(full=True)["logs"]

        output += "statistics:\n{}\n\n".format(pprint.pformat(logs[key]["stats"]))
        output += "entries:\n{}\n\n".format(pprint.pformat(logs[key]["entries"]))
        
        return output

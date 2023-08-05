import datetime
import collections
import pprint


class _ArchiveEntry:
    messages = None
    counter = None
    time = None
    _maxlen = None

    def __init__(self, maxlen=10):
        self._maxlen = maxlen
        self.messages = collections.deque(maxlen=self._maxlen)
        self.counter = 0
        self.time = None

    def add(self, message):
        self.messages.append(message)
        self.counter += 1
        self.time = datetime.datetime.now()

    def get_last_message(self):
        try:
            return self.messages[-1]
        except IndexError:
            return None

    def get_stats(self, full):
        try:
            str_time = self.time.strftime("%Y-%m-%dT%H:%M:%S")
        except AttributeError:
            str_time = None

        result = {
            "counter": self.counter,
            "stored": len(self.messages),
            "time": str_time,
            "maxlen": self._maxlen,
            "last_message": self.get_last_message(),
        }
        if full:
            result["messages"] = self.messages
        return result


class MessageArchive:
    logger = None
    request = None
    config = None
    runtime = None
    ping = None
    end = None

    def __init__(self):
        self.logger = _ArchiveEntry(maxlen=1)
        self.request = _ArchiveEntry(maxlen=5)
        self.config = _ArchiveEntry(maxlen=5)
        self.runtime = _ArchiveEntry(maxlen=10)
        self.ping = _ArchiveEntry(maxlen=50)
        self.end = _ArchiveEntry(maxlen=5)

    def archive_ping(self, message):
        self.ping.add(message)

    def archive_config(self, message):
        self.config.add(message)

    def archive_runtime(self, message):
        message["process_time_percent"] = message["process-time"] / message["service-uptime"]
        self.runtime.add(message)

    def archive_end(self, message):
        self.end.add(message)

    def archive_logger(self, message):
        self.logger.add(message)

    def archive_request(self, message):
        self.request.add(message)

    def get_stats(self, full=True):
        result = {
            "request": self.request.get_stats(full),
            "ping": self.ping.get_stats(full),
            "runtime": self.runtime.get_stats(full),
            "config": self.config.get_stats(full),
            "logger": self.logger.get_stats(full),
            "end": self.end.get_stats(full)
        }
        return result

    def get_string_stats(self, key):
        def _generate_output(archive):
            output = "stats:\n"
            output += " - time: {}\n".format(archive["time"])
            output += " - counter: {}\n".format(archive["counter"])
            output += " - stored: {}\n".format(archive["stored"])
            output += " - maxlen: {}\n".format(archive["maxlen"])
            output += "messages:\n"
            for m in archive["messages"]:
                output += "{}\n".format(pprint.pformat(m, indent=4))
            output += "\n"
            return output

        archive = self.get_stats(full=True)
        if key in archive:
            output = _generate_output(archive[key])
        elif key == "all":
            output = ""
            keys = list(archive.keys())
            keys.sort()
            for k in keys:
                output += "'{}':\n".format(k)
                output += _generate_output(archive[k])
                output += "\n"
        else:
            output = "unknown key '{}'\n".format(key)

        return output

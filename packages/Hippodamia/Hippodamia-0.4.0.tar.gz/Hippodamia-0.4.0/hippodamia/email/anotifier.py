from pelops.logging.mylogger import get_child
from asyncscheduler import AsyncScheduler


class ANotifier:
    _counter = None

    _config = None
    _logger = None
    _send_email = None

    _to = None
    _subject = None
    _pre_text = None
    _post_text = None

    _sched = None

    def __init__(self, config, send_email, logger):
        self._config = config
        self._logger = get_child(logger, self.__class__.__name__)
        self._logger.info("__init__")
        self._logger.debug("__init__ - config: {}".format(self._config))

        self._to = self._config["to"]
        self._subject = self._config["subject"]
        try:
            self._pre_text = self._config["pre-text"]
        except KeyError:
            self._pre_text = ""
        try:
            self._post_text = self._config["post-text"]
        except KeyError:
            self._post_text = ""

        self._send_email = send_email
        self._sched = AsyncScheduler()
        self._counter = 0

    def _send_message(self, body):
        self._logger.info("_send_message")
        message = "<html><body><div>{}</div><div>{}</div><div>{}</div><div>{}</div></body></html>"\
            .format(self._pre_text, body, self._post_text, self._message_footer())
        self._logger.debug("_send_message - message: {}".format(message.encode("utf-8")))
        self._send_email(self._subject, message, self._to)
        self._counter += 1

    def _message_footer(self):
        raise NotImplementedError()

    def start(self):
        self._logger.info("start")
        self._sched.start()
        self._start()

    def _start(self):
        raise NotImplementedError()

    def stop(self):
        self._logger.info("stop")
        self._sched.stop(wait=False)
        self._stop()

    def _stop(self):
        raise NotImplementedError()

    def get_stats(self):
        stats = {
            "count": self._counter,
            "to": self._to,
            "scheduled events": len(self._sched.scheduler.queue)
        }
        stats.update(self._get_stats())
        return stats

    def _get_stats(self):
        raise NotImplementedError()


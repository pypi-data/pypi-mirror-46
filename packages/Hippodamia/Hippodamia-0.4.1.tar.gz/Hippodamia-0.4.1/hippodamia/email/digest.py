import datetime
import time
import pprint
from hippodamia.enums import ViewDetails
from hippodamia.enums import StatType
from hippodamia.email.anotifier import ANotifier


class Digest(ANotifier):
    _repeat = None
    _at = None
    _start_day = None
    _send_at_startup = None

    _agentshadows = None
    _heartbeat = None
    _hierarchical_view = None
    _onboarding = None
    _archive = None
    _mqtt_client = None

    def __init__(self, config, send_mail, logger, mqtt_client, agentshadows, heartbeat, hierarchical_view,
                 onboarding, archive):
        ANotifier.__init__(self, config, send_mail, logger)

        self._repeat = self._config["repeat"]
        try:
            temp = self._config["at"].split(":")
            self._at = datetime.time(hour=int(temp[0]), minute=int(temp[1]))
        except KeyError:
            self._at = datetime.datetime.now().time()
        self._logger.debug("__init__ - setting 'at' to {}".format(self._at))
        try:
            weekday = self._config["start-day"]
            weekdays = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
            self._start_day = weekdays.index(weekday)
        except KeyError:
            self._start_day = datetime.datetime.now().weekday()
        self._logger.debug("__init__ - setting 'start-day' to {}".format(self._start_day))
        try:
            self._send_at_startup = self._config["send-at-startup"]
        except:
            self._send_at_startup = False

        if self._send_at_startup and "start-day" not in self._config and "at" not in self._config:
            self._send_at_startup = False
            self._logger.debug("__init__ - forcing 'send-at-startup' to {} - 'start.day' and 'at' are not set -> a "
                               "digest email is sent immediately after startup anyways.".format(self._send_at_startup))
        else:
            self._logger.debug("__init__ - setting 'send-at-startup' to {}".format(self._send_at_startup))

        self._mqtt_client = mqtt_client
        self._agentshadows = agentshadows
        self._heartbeat = heartbeat
        self._hierarchical_view = hierarchical_view
        self._onboarding = onboarding
        self._archive = archive

    def _calc_first_timestamp(self):
        diff = self._start_day - datetime.datetime.now().weekday()
        if diff < 0:
            diff += 7
        days = datetime.timedelta(days=diff)
        target_day = datetime.datetime.now().date() + days
        target_time = self._at
        target = datetime.datetime.combine(target_day, target_time)
        first = time.mktime(target.timetuple())
        self._logger.info("_calc_first_timestamp: at {} seconds (now {} s)".format(first, time.time()))
        return first

    def _calc_interval(self):
        if self._repeat == "HOURLY":
            interval = 3600
        elif self._repeat == "DAILY":
            interval = 3600 * 24
        elif self._repeat == "WEEKLY":
            interval = 3600 * 24 * 7
        else:
            err_message = "_calc_interval - unknown repeat '{}'".format(self._repeat)
            self._logger.error(err_message)
            raise RuntimeError(err_message)

        self._logger.info("_calc_interval: {} seconds".format(interval))
        return interval

    def _digest_send_message(self):
        body = self._render_body()
        self._send_message(body)

    def _start(self):
        self._sched.repeatabs(self._calc_first_timestamp(), self._calc_interval(), 1, self._digest_send_message)
        if self._send_at_startup:
            self._logger.info("sending digest at startup")
            self._digest_send_message()

    def _stop(self):
        pass

    def _render_body(self):
        message  = "<h1>Hierarchical View</h1>"
        message += "<pre>{}</pre>".format(self._hierarchical_view.pformat(details=ViewDetails.FULL))

        message += "<h1>Micro-Service Overview</h1>"
        keys = list(self._agentshadows.keys())
        keys.sort()
        for k in keys:
            microservice = self._agentshadows[k]
            message += "<h2>[{}] {}</h2>".format(microservice.properties.gid, microservice.properties.name)
            message += "<pre>{}</pre>".format(microservice.get_string_stats(StatType.GENERAL))

        message += "<h1>Micro-Service Archive</h1>"
        if len(self._archive) == 0:
            message += "<div>Archive is empty.</div>"
        else:
            message = "<ul>"
            for microservice in self._archive:
                message += " <li>[{}] {}</li>".format(microservice.properties.gid, microservice.properties.name)
            message += "</ul>"

        message += "<h1>Heartbeat</h1>"
        message += "<pre>{}</pre>".format(self._heartbeat.get_string_stats())

        message += "<h1>Onboarding</h1>"
        message += "<pre>{}</pre>".format(self._onboarding.get_string_stats())

        message += "<h1>MQTT</h1>"
        message += "<div>mqtt client connection active: <div>{}</div>".format(self._mqtt_client.is_connected.is_set())
        message += "<h2>active subscriptions</h2>"
        message += "<ul>"
        for sub, func in self._mqtt_client.subscribed_topics().items():
            message += " - {}: [{}]\n".format(sub, func)
        message += "</ul>"
        message += "<h2>send/receive statistics</h2>"
        message += "<pre>{}</pre>".format(pprint.pformat(self._mqtt_client.stats.get_stats(), indent=2))

        return message

    def _message_footer(self):
        message = "<br/>"
        message += "<div style='text-align:right'>Digest generated at {}</div>".format(datetime.datetime.now())
        try:
            ne = self._sched.scheduler.queue[0]
            ne_time = ne.time
            dt = datetime.datetime.fromtimestamp(ne_time)
            next_event = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        except IndexError:
            next_event = "n/a"
        message += "<div style='text-align:right'>Next digest scheduled for {}</div>".format(next_event)
        return message

    def _get_stats(self):
        return {}

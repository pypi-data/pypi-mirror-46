from hippodamia.enums import StatType
from collections import namedtuple
from collections import defaultdict
from collections import deque
from threading import Lock
from hippodamia.email.anotifier import ANotifier
import datetime
from hippodamia.agentshadow.states.state_ids import state_ids


class StateTransition:
    from_state = None
    to_state = None

    def __init__(self, from_state, to_state):
        self.from_state = from_state
        self.to_state = to_state

    def __eq__(self, other):
        if not isinstance(other, StateTransition):
            return NotImplemented
        return self.from_state == other.from_state and self.to_state == other.to_state

    def __hash__(self):
        return hash((self.from_state, self.to_state))

    def __repr__(self):
        return "StateTransition(from_state='{}', to_state='{}')".format(self.from_state, self.to_state)


class Event:
    gid = None
    type = None
    value = None
    time = None

    def __init__(self, gid, value):
        self.gid = gid
        self.value = value
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def to_html(self):
        raise NotImplementedError


class StateEvent(Event):
    def __init__(self, gid, value):
        Event.__init__(self, gid, value)

    def to_html(self):
        html = "<span><b>{}</b> from: {}, to: {}, @{}</span>".format(self.gid, self.value.from_state, self.value.to_state,
                                                                   self.time)
        return html


class LogEvent(Event):
    def __init__(self, gid, value):
        Event.__init__(self, gid, value)

    def to_html(self):
        html = "<span><b>{}</b> log-level: {}, @{}</span>".format(self.gid, self.value, self.time)
        return html


class Spontaneous(ANotifier):
    _state_filter = None
    _event_queue = None
    _event_queue_lock = None
    _delay = None
    _state_transition_names = None
    _agentshadows = None

    def __init__(self, config, send_mail, logger, agentshadows, agentshadowfactory):
        ANotifier.__init__(self, config, send_mail, logger)

        self._agentshadows = agentshadows

        self._delay = self._config["delay"]

        self._state_transition_names = {}
        self._state_filter = []
        for cse in self._config["state_events"]:
            se = StateTransition(cse["from"], cse["to"])
            self._state_filter.append(se)
            se2 = StateTransition(state_ids.INACTIVE.name, state_ids.LOST.name)
            name = "{} -> {}".format(se.from_state, se.to_state)
            self._state_transition_names[se] = name
            self._logger.debug("__init__ - adding state filter '{}'".format(name))

        self._log_level_filter = []
        for l in self._config["log_events"]:
            self._log_level_filter.append(l)
            self._logger.debug("__init__ - adding log level filter '{}'".format(l))

        self._event_queue = deque()
        self._event_queue_lock = Lock()

        agentshadowfactory.register_state_transistion_event_observer(self.state_transition_event, agentshadows)
        agentshadowfactory.register_log_event_observer(self.log_event, agentshadows)

    def _start(self):
        pass

    def _stop(self):
        pass

    def _process_queue(self):
        with self._event_queue_lock:
            if self._event_queue:
                event_mapping = defaultdict(list)
                while self._event_queue:
                    event = self._event_queue.pop()
                    event_mapping[event.gid].append(event)
                body = self._render_body(event_mapping)
                self._send_message(body)

    def _render_body(self, event_mapping):
        text = "<h1>Affected Agent Shadows</h1>"
        text += "<ul>"
        keys = list(event_mapping.keys())
        keys.sort()
        for gid in keys:
            shadow = self._agentshadows[gid]
            text += "<li>[{}] {}</li>".format(gid, shadow.properties.name)
        text += "</ul>"

        for gid, mapping in event_mapping.items():
            shadow = self._agentshadows[gid]
            text += "<h1>[{}] {}</h1>".format(gid, shadow.properties.name)
            text += "<h2>events</h2>"
            text += "<ul>"
            for m in mapping:
                text += "<li>{}</li>".format(m.to_html())
            text += "</ul>"
            text += "<h2>agent shadow details</h2>"
            text += "<pre>{}</pre>".format(shadow.get_string_stats(StatType.ALL))

        return text

    def state_transition_event(self, gid, from_state, to_state):
        st = StateTransition(from_state.name, to_state.name)
        if st in self._state_filter:
            event = StateEvent(gid, st)
            self._put(event)

    def log_event(self, gid, level):
        if level in self._log_level_filter:
            event = LogEvent(gid, level)
            self._put(event)

    def _put(self, event):
        with self._event_queue_lock:
            self._event_queue.appendleft(event)
            self._sched.enter(self._delay, 1, self._process_queue)

    def _message_footer(self):
        message = "<br/>"
        message += "<div style='text-align:right'>Event notification generated at {}</div>".format(datetime.datetime.now())
        return message

    def _get_stats(self):
        return {}

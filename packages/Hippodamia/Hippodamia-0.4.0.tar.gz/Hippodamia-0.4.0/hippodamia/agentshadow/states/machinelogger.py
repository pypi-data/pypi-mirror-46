from tantamount.machine import Machine
import collections
import datetime
import copy


class MachineLogger(Machine):
    logger = None
    history = None
    _observer = None
    _gid = None

    def __init__(self, gid, logger):
        self.logger = logger.getChild(self.__class__.__name__)
        self.history = collections.deque(maxlen=100)
        Machine.__init__(self, ignore_undefined_events=True)
        self.registertransitionhook(self._hook)
        self._gid = gid

    def register_state_transistion_event_observer(self, observer):
        self._observer = observer

    def _hook(self, start_id, transition_id, target_id):
        timestamp = datetime.datetime.now()
        self.history.append({"from": start_id.name, "event": transition_id.name, "to": target_id.name, "time": timestamp})
        if self._observer:
            self._observer(self._gid, start_id, target_id)

    def operate(self, eventid, source_stateid=None, source_activation_counter=None):
        self.logger.debug("operate - eventid: {}".format(eventid))
        try:
            Machine.operate(self, eventid, source_stateid, source_activation_counter)
        except KeyError as err:
            self.logger.info("operate - KeyError: {}".format(err))
        except Exception as e:
            self.logger.error("operate - Exception: {}".format(e))
            raise e

    def asyncoperate(self, eventid, source_stateid=None, source_activation_counter=None):
        self.logger.debug("asyncoperate - eventid: {}".format(eventid))
        Machine.asyncoperate(self, eventid, source_stateid, source_activation_counter)

    def addstate(self, state):
        self.logger.debug("addstate - state: {}, stateid: {}, groupid: {}".format(state, state.id, state.groupid))
        Machine.addstate(self, state)

    def addtimeoutevent(self, stateid, eventid, seconds):
        self.logger.debug("addtimeoutevent - stateid: {}, eventid: {}, seconds: {}".format(stateid, eventid, seconds))
        Machine.addtimeoutevent(self, stateid, eventid, seconds)

    def addtransition(self, startstateid, transitionid, targetstateid, actionFunc=None, actionArgs=None):
        self.logger.debug("addtransition - startstateid: {}, transitionid: {}, targetstateid: {}, actionFunc=None: {}, "
                          "actionArgs: {}".format(startstateid, transitionid, targetstateid, actionFunc, actionArgs))
        Machine.addtransition(self, startstateid, transitionid, targetstateid, actionFunc, actionArgs)

    def start(self):
        self.logger.debug("start - start")
        Machine.start(self)
        self.logger.debug("start - finished")

    def asyncstart(self):
        self.logger.debug("asyncstart - start")
        Machine.asyncstart(self)
        self.logger.debug("asyncstart - finished")

    def get_active_state(self):
        self.logger.debug("get_active_state")
        return Machine.get_active_state(self)

    def restarttimeoutevent(self):
        self.logger.debug("restarttimeoutevent")
        Machine.restarttimeoutevent(self)

    def setstartstate(self, stateid):
        self.logger.debug("setstartstate - stateid: {}".format(stateid))
        Machine.setstartstate(self, stateid)

    def stop(self):
        self.logger.debug("stop - start")
        Machine.stop(self)
        self.logger.debug("stop - finished")

    def updatetimeoutevent(self, stateid, eventid, seconds):
        self.logger.debug("updatetimeoutevent - statid: {}, eventid: {}, seconds: {}".format(stateid, eventid, seconds))
        Machine.updatetimeoutevent(self, stateid, eventid, seconds)

    def _async_worker(self):
        self.logger.debug("_async_worker - start")
        try:
            Machine._async_worker(self)
        except RuntimeError as e:
            self.logger.error("_async_worker exited with: {}".format(e))
            raise e
        self.logger.debug("_asnyc_worker - finished")

    def get_stats_active_state(self):
        since = self._state.timestamp_on_entry
        try:
            duration = datetime.datetime.now() - since
        except TypeError:
            duration = None
        stats = {
            "output": self._state.id.name,
            "since": since,
            "duration": duration
        }
        return stats

    def get_stats(self):
        stats = {
            'active-state': self.get_stats_active_state(),
            'history': []
        }

        for h in self.history:
            entry = copy.deepcopy(h)
            entry["time"] = entry["time"].strftime("%Y-%m-%dT%H:%M:%S")
            stats["history"].append(entry)

        return stats

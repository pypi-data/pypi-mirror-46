from hippodamia.agentshadow.states.machinelogger import MachineLogger
from tantamount.fsm2dot import GetDotNotation

from hippodamia.agentshadow.states.active import Active
from hippodamia.agentshadow.states.inactive import Inactive
from hippodamia.agentshadow.states.onboarding import Onboarding
from hippodamia.agentshadow.states.onboarded import Onboarded
from hippodamia.agentshadow.states.stopped import Stopped
from hippodamia.agentshadow.states.archivecandidate import ArchiveCandidate
from hippodamia.agentshadow.states.archived import Archived
from hippodamia.agentshadow.states.lost import Lost
from hippodamia.agentshadow.states.predefined import Predefined
from hippodamia.agentshadow.states.event_ids import event_ids
from hippodamia.agentshadow.states.state_ids import state_ids

import threading


def create(gid, timings, set_state_health, reset_max_level, logger, predefined=False):
    logger.info("creating state machine - start")

    logger.debug("creating state machine - creating states")
    states = {
        state_ids.ACTIVE: Active(state_ids.ACTIVE, set_state_health,
                                 reset_max_level, logger),
        state_ids.INACTIVE: Inactive(state_ids.INACTIVE, set_state_health,
                                     reset_max_level, logger),
        state_ids.ONBOARDING: Onboarding(state_ids.ONBOARDING, set_state_health,
                                         reset_max_level, logger),
        state_ids.ONBOARDED: Onboarded(state_ids.ONBOARDED, set_state_health,
                                       reset_max_level, logger),
        state_ids.STOPPED: Stopped(state_ids.STOPPED, set_state_health,
                                   reset_max_level, logger),
        state_ids.ARCHIVECANDIDATE: ArchiveCandidate(state_ids.ARCHIVECANDIDATE, set_state_health,
                                                     reset_max_level, logger),
        state_ids.ARCHIVED: Archived(state_ids.ARCHIVED, set_state_health,
                                     reset_max_level, logger),
        state_ids.PREDEFINED: Predefined(state_ids.PREDEFINED, set_state_health,
                                         reset_max_level, logger),
        state_ids.LOST: Lost(state_ids.LOST, set_state_health, reset_max_level, logger),
    }

    machine = MachineLogger(gid, logger)

    logger.debug("creating state machine - adding states")
    for state in states.values():
        machine.addstate(state)

    logger.debug("creating state machine - set start state")
    if predefined:
        logger.debug(" - setting state PREDEFINED as start state")
        machine.setstartstate(state_ids.PREDEFINED)
    else:
        logger.debug(" - setting state STOPPED as start state")
        machine.setstartstate(state_ids.STOPPED)

    logger.debug("creating state machine - adding transitions")
    machine.addtransition(state_ids.ONBOARDING, event_ids.TIMEOUT, state_ids.STOPPED)
    machine.addtransition(state_ids.ONBOARDING, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)
    machine.addtransition(state_ids.ONBOARDING, event_ids.ONBOARDING_RESPONSE, state_ids.ONBOARDED)

    machine.addtransition(state_ids.ONBOARDED, event_ids.TIMEOUT, state_ids.STOPPED)
    machine.addtransition(state_ids.ONBOARDED, event_ids.REGULAR_MESSAGE, state_ids.ACTIVE)
    machine.addtransition(state_ids.ONBOARDED, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)

    machine.addtransition(state_ids.ACTIVE, event_ids.REGULAR_MESSAGE, state_ids.ACTIVE)
    machine.addtransition(state_ids.ACTIVE, event_ids.TIMEOUT, state_ids.INACTIVE)
    machine.addtransition(state_ids.ACTIVE, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)
    machine.addtransition(state_ids.ACTIVE, event_ids.OFFBOARDING, state_ids.STOPPED)

    machine.addtransition(state_ids.INACTIVE, event_ids.TIMEOUT, state_ids.LOST)
    machine.addtransition(state_ids.INACTIVE, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)
    machine.addtransition(state_ids.INACTIVE, event_ids.OFFBOARDING, state_ids.STOPPED)
    machine.addtransition(state_ids.INACTIVE, event_ids.REGULAR_MESSAGE, state_ids.ACTIVE)

    machine.addtransition(state_ids.STOPPED, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)
    machine.addtransition(state_ids.STOPPED, event_ids.TIMEOUT, state_ids.ARCHIVECANDIDATE)

    machine.addtransition(state_ids.ARCHIVECANDIDATE, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)
    machine.addtransition(state_ids.ARCHIVECANDIDATE, event_ids.ARCHIVE, state_ids.ARCHIVED)

    machine.addtransition(state_ids.PREDEFINED, event_ids.ONBOARDING_REQUEST, state_ids.ONBOARDING)

    machine.addtransition(state_ids.LOST, event_ids.LOST, state_ids.STOPPED)

    logger.debug("creating state machine - set timeout events")
    machine.addtimeoutevent(state_ids.ONBOARDED, event_ids.TIMEOUT, timings["onboarding_timeout"])
    machine.addtimeoutevent(state_ids.ONBOARDING, event_ids.TIMEOUT, timings["onboarding_timeout"])
    machine.addtimeoutevent(state_ids.ACTIVE, event_ids.TIMEOUT, timings["wait_for_message_timeout"])
    machine.addtimeoutevent(state_ids.INACTIVE, event_ids.TIMEOUT, timings["deactivation_timeout"])
    machine.addtimeoutevent(state_ids.STOPPED, event_ids.TIMEOUT, timings["archivation_timeout"])
    machine.addtimeoutevent(state_ids.LOST, event_ids.LOST, 0)

    logger.info("creating state machine - done")
    return machine, states


def dot2file(filename):
    class NoLogger:
        def info(self, message):
            pass

        def debug(self, message):
            pass

        def warning(self, message):
            pass

        def error(self, message):
            pass

        def getChild(self, name):
            return self

    logger = NoLogger()
    updateavailable = threading.Event()
    timings = {
        "onboarding_timeout": 60,
        "wait_for_message_timeout": 180,
        "deactivation_timeout": 360,
        "heartbeat_interval": 120,
        "archivation_timeout": 86400
    }
    machine, states = create(updateavailable, timings, None, None, logger)

    gdn = GetDotNotation(machine, graphname="Agentshadow States", getStateId=(lambda x:x.name),
                         getStateName=(lambda x:x.name), getTransitionName=(lambda x:x.name))
    new_dotnotation = gdn.getdotnotation(show_key=False)

    try:
        with open(filename, 'r') as f:
            old_dotnotation = f.read()
    except OSError:
        old_dotnotation = ""

    if new_dotnotation != old_dotnotation:
        print("updating {} to latest version.".format(filename))
        with open(filename, "w") as f:
            f.write(new_dotnotation)

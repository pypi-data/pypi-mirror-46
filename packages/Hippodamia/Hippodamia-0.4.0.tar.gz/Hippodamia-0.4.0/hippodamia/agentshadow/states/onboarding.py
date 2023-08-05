from hippodamia.agentshadow.states.amonitoringstate import AMonitoringState
from hippodamia.agentshadow.states.event_ids import event_ids
from hippodamia.enums import Health


class Onboarding(AMonitoringState):
    func_send_onboarding_response = None
    func_deactivate_recv_messages = None
    func_activate_recv_messages = None

    def __init__(self, id, set_health, reset_max_level, logger, group_id=None):
        AMonitoringState.__init__(self, id, set_health, Health.RED, reset_max_level,
                                  logger, __class__.__name__, group_id=group_id)

    def _on_entry(self):
        self.func_deactivate_recv_messages()
        self.reset_max_level()

        return event_ids.ONBOARDING_RESPONSE

    def _on_exit(self):
        self.func_activate_recv_messages()
        self.func_send_onboarding_response()

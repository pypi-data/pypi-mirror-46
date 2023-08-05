from hippodamia.agentshadow.states.amonitoringstate import AMonitoringState
from hippodamia.enums import Health


class Stopped(AMonitoringState):
    func_deactivate_recv_messages = None

    def __init__(self, id, set_health, reset_max_level, logger, group_id=None):
        AMonitoringState.__init__(self, id, set_health, Health.RED, reset_max_level,
                                  logger, __class__.__name__, group_id=group_id)

    def _on_entry(self):
        self.func_deactivate_recv_messages()
        self.reset_max_level()

        return None

    def _on_exit(self):
        pass

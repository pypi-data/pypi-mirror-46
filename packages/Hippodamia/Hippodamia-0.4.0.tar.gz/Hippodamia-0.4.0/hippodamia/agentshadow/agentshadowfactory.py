from hippodamia.agentshadow.agentshadow import AgentShadow


class AgentShadowFactory:
    _topics = None
    _service_timings = None
    _agent_timings = None
    _mongo_client = None
    _mqtt_client = None
    _logger = None
    _preload_config_list = None
    _observer_state_events = None
    _observer_log_events = None

    def __init__(self, topics, service_timings, agent_timings, preload_config_list, mongo_client,
                 mqtt_client, logger):
        self._topics = topics
        self._service_timings = service_timings
        self._agent_timings = agent_timings
        self._mongo_client = mongo_client
        self._mqtt_client = mqtt_client
        self._logger = logger
        self._preload_config_list = preload_config_list

    def add_predefined_shadows(self, agentshadows):
        def _already_loaded(preload_config):
            for entry in agentshadows.values():
                if (entry.properties.location == preload_config["location"] and
                        entry.properties.room == preload_config["room"] and
                        entry.properties.device == preload_config["device"] and
                        entry.properties.name == preload_config["name"]):
                    return True
            return False

        def _add_entry(preload_config):
            gid = str(preload_config["gid"])
            shadow = self.new_agentshadow(preload_config=preload_config)
            shadow.register_state_transistion_event_observer(self._observer_state_events)
            shadow.register_log_event_observer(self._observer_log_events)
            agentshadows[gid] = shadow

        self._logger.info("adding predefined shadows - start")
        for preload_config in self._preload_config_list:
            if _already_loaded(preload_config):
                self._logger.debug("agentshadow already loaded for {}".format(preload_config))
                continue
            else:
                self._logger.debug("adding preloadconfig for agentshadow {}".format(preload_config))
                _add_entry(preload_config)
        self._logger.info("adding predefined shadows - finished")

    def new_agentshadow(self, preload_config=None, gid=None):
        if preload_config is None and gid is None:
            raise ValueError("AgentShadowFactory.create_agentshadow - preload_config and gid are None")
        shadow = AgentShadow(self._topics, self._service_timings, self._agent_timings,
                             self._mongo_client, self._mqtt_client, self._logger, preload_config=preload_config,
                             gid=gid)
        shadow.register_state_transistion_event_observer(self._observer_state_events)
        shadow.register_log_event_observer(self._observer_log_events)
        return shadow

    @staticmethod
    def get_string_list(agentshadows):
        m = ""
        gids = list(agentshadows.keys())
        gids.sort()
        for gid in gids:
            shadow = agentshadows[gid]
            m += "gid: {}, state: {}, health:{}, necessity: {}, name: {}, type:{}, log-entries: {}\n"\
                .format(gid,
                        shadow.get_state_id().name,
                        shadow.properties.health.name,
                        shadow.properties.necessity.name,
                        shadow.properties.name,
                        shadow.properties.type,
                        shadow.log_archive.flat_list.counter)
        return m

    def register_state_transistion_event_observer(self, observer, agentshadows):
        self._observer_state_events = observer
        for shadow in agentshadows.values():
            shadow.register_state_transistion_event_observer(self._observer_state_events)

    def register_log_event_observer(self, observer, agentshadows):
        self._observer_log_events = observer
        for shadow in agentshadows.values():
            shadow.register_log_event_observer(self._observer_log_events)


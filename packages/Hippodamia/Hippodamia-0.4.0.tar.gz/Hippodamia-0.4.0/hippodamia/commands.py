import pprint
from hippodamia.agentshadow.agentshadowfactory import AgentShadowFactory
import pelops.ui.tools
from hippodamia.enums import StatType
from hippodamia.enums import ViewDetails


class CommandFactory:
    _logger = None
    _shadows = None
    _hierarchical_view = None
    _request_ping = None
    _request_runtime = None
    _request_config = None
    _request_reonboarding = None
    _request_end = None
    _heartbeat = None
    _onboarding = None
    _config = None
    _archive = None
    _notification = None

    def __init__(self, version, config, shadows, heartbeat, health_view, onboarding, request_ping, request_runtime,
                 request_config, request_reonboarding, request_end, archive, notification, logger):
        self._shadows = shadows
        self._config = config
        self._hierarchical_view = health_view
        self._request_ping = request_ping
        self._request_runtime = request_runtime
        self._request_config = request_config
        self._request_reonboarding = request_reonboarding
        self._request_end = request_end
        self._logger = logger
        self._heartbeat = heartbeat
        self._onboarding = onboarding
        self._archive = archive
        self._notification = notification

    def add_commands(self, add_command):
        add_command("request_ping", self.do_request_ping)
        add_command("request_runtime", self.do_request_runtime)
        add_command("request_config", self.do_request_config)
        add_command("request_reonboarding", self.do_request_reonboarding)
        add_command("request_end", self.do_request_end)
        add_command("list", self.do_list)
        add_command("hierarchical", self.do_hierarchical)
        add_command("agentstats", self.do_agentstats)
        add_command("agentlog", self.do_agentlog)
        add_command("agentmessages", self.do_agentmessages)
        add_command("heartbeatstats", self.do_heartbeatstats)
        add_command("onboardingstats", self.do_onboardingstats)
        add_command("notificationstats", self.do_notificationstats)
        add_command("archive", self.do_archive)
        add_command("ad", self.do_ad)  # agentdetails full
        add_command("am", self.do_am)  # agentmessages
        add_command("al", self.do_al)  # agentmessages
        add_command("ag", self.do_ag)  # agentdetails general
        add_command("l", self.do_l)  # list
        add_command("h", self.do_h)  # hierarchical
        add_command("o", self.do_o)  # onboarding stats

    def _check_gid(self, gid):
        if gid not in self._shadows:
            raise KeyError("gid {} not in {}".format(gid, list(self._shadows.keys())))
        return gid

    def _request_extract_gid(self, name, arg):
        args = pelops.ui.tools.parse(arg)

        gid = None
        if len(args) == 1 and str(args[0]).lower() == "all":
            print("Sending {} request to all monitored services\n".format(name))
        elif len(args) == 2 and str(args[0]).lower() == "gid":
            gid = self._check_gid(args[1])
            print("Send {} regest to monitoring service with gid == {}\n".format(name, gid))
        else:
            raise ValueError("Wrong arguments: {}. expected '{} [all|gid gid]'.\n".format(args, name))

        return gid

    def do_exit(self, arg):
        """exit - stops the monitoring service: EXIT"""
        return True

    def do_request_ping(self, arg):
        """request_ping [all|gid gid] - publish ping request either to all monitored services or to a specific one: REQUEST_PING GID 1"""
        try:
            self._request_ping(self._request_extract_gid("ping", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))

    def do_request_runtime(self, arg):
        """request_runtime [all|gid gid] - publish runtime request either to all monitored services or to a specific one: REQUEST_RUNTIME GID 1"""
        try:
            self._request_runtime(self._request_extract_gid("runtime", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_config(self, arg):
        """request_config [all|gid gid] - publish config request either to all monitored services or to a specific one: REQUEST_CONFIG GID 1"""
        try:
            self._request_config(self._request_extract_gid("config", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_reonboarding(self, arg):
        """request_reonboarding [all|gid gid] - publish reonboarding request either to all monitored services or to a specific one: REQUEST_REONBOARDING GID 1"""
        try:
            self._request_reonboarding(self._request_extract_gid("reonboarding", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))
            
    def do_request_end(self, arg):
        """request_end [all|gid gid] - publish end request either to all monitored services or to a specific one: REQUEST_END GID 1"""
        try:
            self._request_end(self._request_extract_gid("end", arg))
        except (KeyError, ValueError) as e:
            print("{}\n".format(e))

    def do_list(self, arg):
        """list - list all known services: LIST"""
        m = AgentShadowFactory.get_string_list(self._shadows)
        pelops.ui.tools.more(m)

    def do_archive(self, arg):
        """archive - list all entries in archive: ARCHIVE"""
        m = "archived agentshadows:\n"
        for a in self._archive:
            m += " - [{}] {}\n".format(a.properties.gid, a.properties.name)
        pelops.ui.tools.more(m)

    def do_hierarchical(self, arg):
        """hierarchical [location location|room room|device device|service service]*
 - show all monitored services: HIERARCHICAL
 - show one location: HIERARCHICAL LOCATION Flat
 - show one specific service: HIERARCHICAL LOCATION Flat ROOM \"Living Room\" DEVICE Thermostat SERVICE \"Thermostat GUI\"
 - show all service that run on devices with the name 'Thermostat': HIERARCHICAL DEVICE Thermostat"""
        syntax = "hierarchical [location location|room room|device device|service service]*"
        arguments = pelops.ui.tools.parse(arg)
        if len(arguments) % 2 == 1:
            print("wrong number of arguments ({}). expected '{}'".format(len(arguments), syntax))
            return
        elif len(arguments) == 0:
            m = self._hierarchical_view.pformat(details=ViewDetails.FULL)
        else:
            filters = {"LOCATION": "", "ROOM": "", "DEVICE": "", "SERVICE": ""}
            pos = 0
            while pos < len(arguments):
                first = arguments[pos].upper()
                second = arguments[pos+1]
                if first in filters:
                    filters[first] = second
                else:
                    print("don't know a parameter/filter named '{}'. expected '{}'".format(first, syntax))
                    return
                pos += 2
            m = self._hierarchical_view.pformat(details=ViewDetails.FULL, filters=filters)
        pelops.ui.tools.more(m)

    def do_agentstats(self, arg):
        """agentstats gid gid [all|general|state_machine|properties|logger|messages]
        show information on one specific monitored service: AGENTSTATS GID 1 PROPERTIES"""
        syntax = "agentstats gid gid [all|general|state_machine|properties|logger|messages]"

        args = pelops.ui.tools.parse(arg)
        if len(args) != 3:
            print("wrong number of arguments: {}. expected '{}'\n".format(args, syntax))
        elif str(args[0]).lower() != "gid":
            print("first argument ({}) must be 'gid'. expected '{}'\n".format(str(args[0]).lower(), syntax))
        elif str(args[2]).upper() not in StatType.get_members():
            print("third argument ({}) must be one of {}. expected '{}'\n".format(str(args[2]).lower(),
                                                                                  StatType.get_members(), syntax))
        else:
            try:
                stat_type = StatType.get_enum(str(args[2]))
                gid = self._check_gid(args[1])
                output = "stats {} for gid {}:\n".format(type, gid)
                output += self._shadows[gid].get_string_stats(stat_type)
                pelops.ui.tools.more(output)
            except (ValueError, KeyError) as e:
                print("{}\n".format(e))

    def do_agentlog(self, arg):
        """agentlog gid gid [FLAT|DEBUG|INFO|WARNING|ERROR|CRITICAL] - view all received log-entries of this
service: AGENTLOG GID 1 FLAT"""
        syntax = "agentlog gid gid [FLAT|DEBUG|INFO|WARNING|ERROR|CRITICAL]"

        args = pelops.ui.tools.parse(arg)
        if len(args) != 3:
            print("wrong number of arguments: {}. expected '{}'\n".format(args, syntax))
        elif str(args[0]).lower() != "gid":
            print("first argument ({}) must be 'gid'. expected '{}'\n".format(str(args[0]).lower(), syntax))
        elif str(args[2].lower()) not in ["flat", "debug", "info", "warning", "error", "critical"]:
            print("unexpected value for third argument '{}'. expected '{}'\n".format(args[2], syntax))
        else:
            try:
                gid = self._check_gid(args[1])
                output = "show {} log for gid: {}\n".format(args[2], gid)
                output += self._shadows[gid].log_archive.get_string_stats(args[2])
                pelops.ui.tools.more(output)
            except KeyError as e:
                print("{}\n".format(e))

    def do_agentmessages(self, arg):
        """agentmessages gid gid [ALL|CONFIG|END|LOGGER|PING|REQUEST|RUNTIME] - view all received messages of this
service: AGENTMESSAGES GID 1 PING"""
        syntax = "agentmessages gid gid [ALL|CONFIG|END|LOGGER|PING|REQUEST|RUNTIME]"

        args = pelops.ui.tools.parse(arg)
        if len(args) != 3:
            print("wrong number of arguments: {}. expected '{}'\n".format(args, syntax))
        elif str(args[0]).lower() != "gid":
            print("first argument ({}) must be 'gid'. expected '{}'\n".format(str(args[0]).lower(), syntax))
        elif str(args[2].lower()) not in ["all", "config", "end", "logger", "ping", "request", "runtime"]:
            print("unexpected value for third argument '{}'. expected '{}'\n".format(args[2], syntax))
        else:
            try:
                gid = self._check_gid(args[1])
                key = args[2].lower()
                output = "show {} messages for gid: {}\n".format(key, gid)
                output += self._shadows[gid].message_archive.get_string_stats(key)
                pelops.ui.tools.more(output)
            except KeyError as e:
                print("{}\n".format(e))

    def do_heartbeatstats(self, arg):
        """heartbeatstats - stats on the heartbeat signal of the monitoring agent: HEARTBEATSTATS"""
        output = "heartbeat: \n"
        output += self._heartbeat.get_string_stats()
        pelops.ui.tools.more(output)

    def do_onboardingstats(self, arg):
        """onboardingstats - stats on the overall onboarding process: ONBOARDINGSTATS"""
        output = "onboarding: \n"
        output += self._onboarding.get_string_stats()
        pelops.ui.tools.more(output)

    def do_notificationstats(self, arg):
        """notificationstats - stats on the email notifcation subsystem: NOTIFICATIONSTATS"""
        output = "email notification: \n"
        output += self._notification.get_string_stats()
        pelops.ui.tools.more(output)

    def do_config(self, arg):
        """config - show the current config: CONFIG"""
        output = pprint.pformat(self._config, indent=2)
        pelops.ui.tools.more(output)

    def _get_default_gid(self):
        gid = "Monitoringservice-0"
        try:
            gid = self._check_gid(gid)
            return gid
        except KeyError:
            raise KeyError("unknown gid '{}'".format(gid))

    def do_ad(self, arg):
        # """shortcut for 'agentdetails gid Monitoringservice-0 all'"""
        args = "gid Monitoringservice-0 all"
        self.do_agentstats(args)

    def do_ag(self, arg):
        # """shortcut for 'agentdetails gid Monitoringservice-0 general'"""
        args = "gid Monitoringservice-0 general"
        self.do_agentstats(args)

    def do_am(self, arg):
        # """shortcut for 'agentmessages gid Monitoringservice-0 all'"""
        args = "gid Monitoringservice-0 all"
        self.do_agentmessages(args)

    def do_al(self, arg):
        # """shortcut for 'stats gid Monitoringservice-0 all'"""
        args = "gid Monitoringservice-0 flat"
        self.do_agentlog(args)

    def do_h(self, arg):
        # """shortcut for 'hierarchical'"""
        self.do_hierarchical(arg)

    def do_l(self, arg):
        # """shortcut for 'list'"""
        self.do_list(arg)

    def do_o(self, arg):
        # """ shortcut for 'onboardingstats'"""
        self.do_onboardingstats(arg)

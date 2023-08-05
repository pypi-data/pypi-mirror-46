import pprint
import json
from hippodamia.flask.serverthread import ServerThread
from flask import Flask, render_template, url_for, flash
from flask_basicauth import BasicAuth
from flask.helpers import locked_cached_property
import logging
from pelops.logging.mylogger import get_child
from pelops.myconfigtools import mask_entries, dict_deepcopy_lowercase
import datetime


class LoggerFlask(Flask):
    _logger = None

    @staticmethod
    def _extract_handlers(logger):
        if logger.parent:
            handlers = LoggerFlask._extract_handlers(logger.parent)
        else:
            handlers = []
        handlers.extend(logger.handlers)
        return handlers

    def __init__(self, import_name, logger):
        self._logger = get_child(logger, "Flask")
        self._logger.setLevel(logger.level)
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(self._logger.level)
        Flask.__init__(self, import_name)

    @locked_cached_property
    def logger(self):
        return self._logger


class FlaskServer:
    _app = None
    _config = None
    _basic_auth = None
    _server_thread = None
    _port = None
    _logger = None

    _shadows = None
    _archive = None
    _hierarchical_view = None
    _heartbeat = None
    _onboarding = None
    _full_config = None
    _mqtt_client = None
    _request_ping = None
    _request_runtime = None
    _request_config = None
    _request_reonboarding = None
    _request_end = None
    _acknowledge_log = None
    _notification = None

    _archive_agentshadows = None
    _purge_agentshadowarchive = None

    _SECRET_KEY = '\xad\xb5\xac\xe1\x99\x1e\r\x9a\x8c\xc8\x07\x11\x06q\xe5\xbe\t\x19Na\xac\xd8\xa9\xe3'

    def __init__(self, config, logger, shadows, archive, heartbeat, hierarchical_view, onboarding, request_ping,
                 request_runtime, request_config, request_reonboarding, request_end, full_config, mqtt_client,
                 archive_agentshadows, purge_agentshadowarchive, acknowledge_log, notification):
        self._config = config
        self._logger = get_child(logger, self.__class__.__name__, self._config)
#        self._logger.addHandler(default_handler)
        self._logger.info("__init__ - start")
        self._logger.debug("__init__ - config: {}".format(self._config))

        self._shadows = shadows
        self._archive = archive

        self._hierarchical_view = hierarchical_view
        self._heartbeat = heartbeat
        self._onboarding = onboarding
        self._request_ping = request_ping
        self._request_runtime = request_runtime
        self._request_config = request_config
        self._request_reonboarding = request_reonboarding
        self._request_end = request_end
        self._acknowledge_log = acknowledge_log
        self._archive_agentshadows = archive_agentshadows
        self._purge_agentshadowarchive = purge_agentshadowarchive
        self._notification = notification

        self._full_config = full_config
        self._mqtt_client = mqtt_client

        self._port = self._config["port"]

        self._init_flask()

        self._logger.info("__init__ - finished")

    def _init_flask(self):
        self._app = LoggerFlask(__name__, self._logger)
        self._app.secret_key = self._SECRET_KEY
        self._basic_auth = self._create_basic_auth()
        self._add_routes()
        self._add_pprint_filter()
        self._add_psorteddict_filter()

    def _add_pprint_filter(self):
        self._logger.debug("add_pprint_filter to jinja")

        def to_pprint(value):
            if value is not None:
                return pprint.pformat(value, indent=2)
            return ""

        self._app.jinja_env.filters['pprint'] = to_pprint

    def _add_psorteddict_filter(self):
        self._logger.debug("add_psorted_filter to jinja")

        def to_psorted(value):
            text = ""
            if value is not None:
                if isinstance(value, dict):
                    keys = list(value.keys())
                    keys.sort()
                    for k in keys:
                        v = value[k]
                        text += "  '{}': {},\n".format(k, pprint.pformat(v, indent=4))
                    if len(text) == 0:
                        text = "{}"
                    else:
                        text = "{"+text[1:-2]+"}"
                elif isinstance(value, list):
                    value.sort()
                    text = pprint.pformat(value, indent=2)
                else:
                    text = str(value)
            return text

        self._app.jinja_env.filters["psorted"] = to_psorted

    def _create_basic_auth(self):
        if "webserver-user" in self._config and "webserver-password" in self._config:
            self._logger.info("_create_basic_auth - adding basic_auth")
            self._app.config['BASIC_AUTH_USERNAME'] = self._config["webserver-user"]
            self._app.config['BASIC_AUTH_PASSWORD'] = self._config["webserver-password"]
            self._app.config['BASIC_AUTH_FORCE'] = True
            return BasicAuth(self._app)
        else:
            self._logger.info("_create_basic_auth - skipping")
            return None

    def _run_server(self):
        self._logger.debug("app.run")
        self._app.run(port=self._port)

    def start(self):
        self._logger.info("starting flask server in process")
        self._server_thread = ServerThread(self._app, self._port)
        self._server_thread.start()
        self._logger.info("flask server started")

    def stop(self):
        self._logger.info("terminating flask server process")
        self._server_thread.stop()
        self._server_thread.join()
        self._logger.info("flask server stopped")

    def _add_routes(self):
        self._logger.debug("adding routes")
        self._app.add_url_rule('/', view_func=self.route_index)
        self._app.add_url_rule('/hierarchical', view_func=self.route_service_hierarchical)
        self._app.add_url_rule('/hierarchical/data', view_func=self.route_service_hierarchical_data)
        self._app.add_url_rule('/list', view_func=self.route_service_list)
        self._app.add_url_rule('/list/data', view_func=self.route_service_list_data)
        self._app.add_url_rule('/service/<gid>/commands', view_func=self.route_service_commands)
        self._app.add_url_rule('/service/<gid>/commands/<cmd>', view_func=self.execute_commands)
        self._app.add_url_rule('/service/<gid>/details', view_func=self.route_service_details)
        self._app.add_url_rule('/service/<gid>/messages', view_func=self.route_service_messages)
        self._app.add_url_rule('/service/<gid>/logs', view_func=self.route_service_logs)
        self._app.add_url_rule('/heartbeatstats', view_func=self.route_heartbeatstats)
        self._app.add_url_rule('/onboardingstats', view_func=self.route_onboardingstats)
        self._app.add_url_rule('/mqtt_stats', view_func=self.route_mqtt_stats)
        self._app.add_url_rule('/notificationstats', view_func=self.route_notificationstats)
        self._app.add_url_rule('/show_config', view_func=self.route_show_config)
        self._app.add_url_rule('/archive', view_func=self.route_archive_list)
        self._app.add_url_rule('/archive/data', view_func=self.route_archive_list_data)
        self._app.add_url_rule('/archive/<gid>/details', view_func=self.route_archive_details)
        self._app.add_url_rule('/archive/<gid>/messages', view_func=self.route_archive_messages)
        self._app.add_url_rule('/archive/<gid>/logs', view_func=self.route_archive_logs)
        self._app.add_url_rule('/group_commands', view_func=self.route_group_commands)
        self._app.add_url_rule('/group_commands/<cmd>', view_func=self.execute_group_commands)
        self._app.add_url_rule('/general_health', view_func=self.route_general_health)
        self._app.add_url_rule('/general_health_data', view_func=self.route_general_health_data)

    def route_index(self):
        return render_template('index.html', name="Monitoring Service")

    def route_general_health(self):
        return render_template('general_health.html')

    def route_general_health_data(self):
        health = self._hierarchical_view.to_dict()
        data = {
            "health": health["health"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        return json.dumps(data)

    def route_service_hierarchical(self):
        # output = self._hierarchical_view.pformat(details=ViewDetails.FULL)
        # title = "Hierarchical View"
        # return render_template('pre.html', title=title, content=output)
        title = "Hierarchical View"
        return render_template('hierarchical_view.html', title=title)

    def route_service_hierarchical_data(self):
        health = self._hierarchical_view.to_dict()
        for location in health["children"]:
            for room in location["children"]:
                for device in room["children"]:
                    for service in device["children"]:
                        gid = service["gid"]
                        service["route_service_details"] = url_for('route_service_details', gid=gid)
                        service["route_service_logs"] = url_for('route_service_logs', gid=gid)
                        service["route_service_commands"] = url_for('route_service_commands', gid=gid)
        data = {
            "health": health,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        return json.dumps(data)

    def route_service_list(self):
        return render_template('service_list.html', title="Active Services",
                               update_route=url_for("route_service_list_data"))

    def route_service_list_data(self):
        data = {
            "entries": [],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        for gid, shadow in self._shadows.items():
            entry = {
                "gid": gid,
                "name": shadow.properties.name,
                "type": shadow.properties.type,
                "state": shadow.get_state_id().name,
                "health": shadow.properties.health.name,
                "necessity": shadow.properties.necessity.name,
                "log_count": shadow.log_archive.flat_list.counter,
                "details": url_for('route_service_details', gid=gid),
                "messages": url_for('route_service_messages', gid=gid),
                "logs": url_for('route_service_logs', gid=gid),
                "commands": url_for('route_service_commands', gid=gid)
            }
            data["entries"].append(entry)
        return json.dumps(data)

    def route_service_commands(self, gid):
        if gid not in self._shadows:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_service_list_data"))

        return render_template('service_commands.html', title="Commands for '{}'".format(gid), gid=gid)

    def execute_commands(self, cmd, gid):
        if gid not in self._shadows:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_service_list_data"))

        message = "executed command '{}'".format(cmd)
        cmd = cmd.lower()
        if cmd == "request_ping":
            self._request_ping(gid)
        elif cmd == "request_runtime":
            self._request_runtime(gid)
        elif cmd == "request_config":
            self._request_config(gid)
        elif cmd == "request_reonboarding":
            self._request_reonboarding(gid)
        elif cmd == "request_end":
            self._request_end(gid)
        elif cmd == "acknowledge_log":
            counter = self._acknowledge_log(gid)
            if counter == 0:
                flash("acknowledge_log for gid '{}' failed.".format(gid))
            else:
                flash("acknowledge_log for gid '{}' success.".format(gid))
        else:
            message = "unknown command '{}'".format(cmd)

        return render_template('service_commands.html', title="Commands for '{}'".format(gid), gid=gid, message=message)

    def route_service_details(self, gid):
        try:
            stats = self._shadows[gid].get_stats()
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_service_list_data"))

        return render_template('service_details.html', title="Details for '{}'".format(gid), gid=gid, stats=stats)

    def route_service_logs(self, gid):
        try:
            log_entries = self._shadows[gid].log_archive.get_stats()["logs"]
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_service_list_data"))

        log_ids = ["flat_list", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        logs = {}
        for k, shadow_logger in log_entries.items():
            logs[k] = {
                "counter_received": shadow_logger["stats"]["received"],
                "counter_stored": shadow_logger["stats"]["stored"],
                "counter_removed": shadow_logger["stats"]["received"] - shadow_logger["stats"]["stored"],
                "entries": shadow_logger["entries"],
            }

        return render_template('service_logs.html', title="Logs for '{}'".
                               format(gid), gid=gid, log_ids=log_ids, logs=logs)

    def route_service_messages(self, gid):
        try:
            messages = self._shadows[gid].message_archive.get_stats()
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_service_list_data"))

        message_types = list(messages.keys())
        message_types.sort()

        return render_template('service_messages.html', title="Messages for '{}'".
                               format(gid), gid=gid, messages=messages, message_types=message_types)

    def route_mqtt_stats(self):
        mqtt_stats = self._mqtt_client.get_stats()
        title = "MQTT Statistics"
        sorted_active_topics = list(mqtt_stats["subscribed_topics"])
        sorted_active_topics.sort()
        sorted_sendrecv_topics = list(mqtt_stats["mqtt_stats"]["topics"])
        sorted_sendrecv_topics.sort()
        return render_template('mqtt_stats.html', title=title, mqtt_stats=mqtt_stats,
                               sorted_active_topics=sorted_active_topics,
                               sorted_sendrecv_topics=sorted_sendrecv_topics)

    def route_heartbeatstats(self):
        stats = self._heartbeat.get_stats()
        title = "Heartbeat Statistics"
        return render_template('heartbeat.html', title=title, stats=stats)

    def route_onboardingstats(self):
        stats = self._onboarding.get_stats()
        title = "Onboarding Statistics"
        return render_template('onboarding.html', title=title, stats=stats)

    def route_notificationstats(self):
        if self._notification:
            stats = pprint.pformat(self._notification.get_stats(), indent=2)
        else:
            stats = ""
        title = "E-Mail Notification Statistics"
        return render_template('notification.html', title=title, stats=stats)

    def route_show_config(self):
        title = "Config"
        config = dict_deepcopy_lowercase(self._full_config)
        mask_entries(config)
        return render_template('config.html', title=title, config=config)

    def route_archive_list(self):
        return render_template('service_list.html', title="Service Archive",
                               update_route=url_for("route_archive_list_data"), archive=True)

    def route_archive_list_data(self):
        data = {
            "entries": [],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        for shadow in self._archive:
            gid = shadow.properties.gid
            entry = {
                "gid": gid,
                "name": shadow.properties.name,
                "type": shadow.properties.type,
                "state": shadow.get_state_id().name,
                "health": shadow.properties.health.name,
                "necessity": shadow.properties.necessity.name,
                "log_count": shadow.log_archive.flat_list.counter,
                "details": url_for('route_archive_details', gid=gid),
                "messages": url_for('route_archive_messages', gid=gid),
                "logs": url_for('route_archive_logs', gid=gid),
                "commands": ""
            }
            data["entries"].append(entry)
        return json.dumps(data)

    def _get_archive_entry(self, gid):
        for entry in self._archive:
            if entry.properties.gid == gid:
                return entry
        raise KeyError("gid '{}' not found archive of agentshadows")

    def route_archive_details(self, gid):
        try:
            stats = self._get_archive_entry(gid).get_stats()
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_archive_list_data"))

        return render_template('service_details.html', title="Details for '{}'".format(gid), gid=gid, stats=stats,
                               archive=True)

    def route_archive_logs(self, gid):
        try:
            log_entries = self._get_archive_entry(gid).log_archive.get_stats()["log_entries"]
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_archive_list_data"))

        log_ids = ["flat_list", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        logs = {}
        for k, shadow_logger in log_entries.items():
            logs[k] = {
                "counter_received": shadow_logger.counter,
                "counter_stored": len(shadow_logger.log),
                "counter_removed": shadow_logger.counter - len(shadow_logger.log),
                "entries": shadow_logger.log,
            }

        return render_template('service_logs.html', title="Logs for '{}'".
                               format(gid), gid=gid, log_ids=log_ids, logs=logs, archive=True)

    def route_archive_messages(self, gid):
        try:
            messages = self._get_archive_entry(gid).message_archive.get_stats()
        except KeyError:
            flash("unknown gid '{}'".format(gid))
            return render_template('service_list.html', title="Active Services",
                                   update_route=url_for("route_archive_list_data"))

        message_types = list(messages.keys())
        message_types.sort()

        return render_template('service_messages.html', title="Messages for '{}'".
                               format(gid), gid=gid, messages=messages, message_types=message_types, archive=True)

    def route_group_commands(self):
        return render_template('group_commands.html')

    def execute_group_commands(self, cmd):
        message = "executed group command '{}'".format(cmd)
        cmd = cmd.lower()
        if cmd == "request_ping":
            self._request_ping()
        elif cmd == "request_runtime":
            self._request_runtime()
        elif cmd == "request_config":
            self._request_config()
        elif cmd == "request_reonboarding":
            self._request_reonboarding()
        elif cmd == "request_end":
            self._request_end()
        elif cmd == "archive_agentshadows":
            result = self._archive_agentshadows()
            flash("archived {} agent shadows".format(result))
        elif cmd == "purge_agentshadowarchive":
            result = self._purge_agentshadowarchive()
            flash("purged {} from the agent shadow archive".format(result))
        elif cmd == "acknowledge_log":
            result = self._acknowledge_log()
            flash("acknowledged logs in {} agent shadows".format(result))
        else:
            message = "unknown command '{}'".format(cmd)

        return render_template('group_commands.html', message=message)



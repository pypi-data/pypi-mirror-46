from hippodamia.agentshadow.states.state_ids import state_ids


def get_schema():
    schema = {
            "description": "Email notification service for hippodamia. At least 'digest' or 'spontaneous' must be "
                           "present to be operational.",
            "type": "object",
            "properties": {
                "config": _config_schema(),
                "digest": _digest_schema(),
                "spontaneous": _spontaneous_schema(),
            },
            "required": ["config"],
            "additionalProperties": False
        }
    return schema


def _config_schema():
    schema = {
        "description": "Smtp server configuration",
        "type": "object",
        "properties": {
            "address": {
                "description": "url",
                "type": "string"
            },
            "port": {
                "description": "port (e.g.: 587)",
                "type": "integer",
                "minimum": 0,
                "maximum": 65535
            },
            "credentials-file": {
                "description": "File containing the credentials (optional).",
                "type": "string"
            },
            "username": {
                "description": "username for smtp server",
                "type": "string"
            },
            "password": {
                "description": "password for smtp server",
                "type": "string"
            },
            "from": {
                "description": "sender e-mail address",
                "type": "string"
            }
        },
        "required": ["address", "port", "username", "password", "from"],
        "additionalProperties": False
    }
    return schema


def _digest_schema():
    schema = {
        "description": "Regularly send a digest notification with the most important data. At least 'at' or 'start-day'"
                       " must be given to be operational.",
        "type": "object",
        "properties": {
            "subject": {
                "description": "subject of the email notification",
                "type": "string"
            },
            "pre-text": {
                "description": "text to be added before the auto-generated content",
                "type": "string"
            },
            "post-text": {
                "description": "text to be added after the auto-generated content",
                "type": "string"
            },
            "to": {
                "description": "receiver e-mail address",
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                ]
            },
            "repeat": {
                "description": "'...' repeat send digest",
                "type": "string",
                "enum": ["HOURLY", "DAILY", "WEEKLY"]
            },
            "at": {
                "description": "send digest notification at this time. in case of repeat=='HOURLY', delay until this "
                               "time. if omited, use time at startup.",
                "type": "string",
                "pattern": "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
                "example": "12:34"
            },
            "start-day": {
                "description": "similar to 'at'. send digest notification on this day. in case of repeat=='HOURLY' or"
                               " repeat=='DAILY', delay until this day. if omitted, use day at startup.",
                "type": "string",
                "enum": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
            },
            "send-at-startup": {
                "description": "send a digest immediately after startup - optional (default: False)",
                "type": "boolean"
            }
        },
        "required": ["subject", "to", "repeat"],
        "additionalProperties": False
    }
    return schema


def _spontaneous_schema():
    state_names = [e.name for e in state_ids]

    schema = {
        "description": "Send a notification upon an event. Events can either be a state change or reception of a "
                       "log entry with a given log-level.",
        "type": "object",
        "properties": {
            "subject": {
                "description": "subject of the email notification",
                "type": "string"
            },
            "pre-text": {
                "description": "text to be added before the auto-generated content",
                "type": "string"
            },
            "post-text": {
                "description": "text to be added after the auto-generated content",
                "type": "string"
            },
            "to": {
                "description": "receiver e-mail address",
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                ]
            },
            "delay": {
                "description": "Delay generation of notification by n-seconds. This avoids generation of alarm showers "
                               "for events that have the same root-cause.",
                "type": "number",
                "minimum": 0
            },
            "state_events": {
                "description": "Set of state transition events.",
                "type": "array",
                "items": {
                    "description": "The transition from state 'A' to state 'B' will trigger a notification event.",
                    "type": "object",
                    "properties": {
                        "from": {
                            "description": "start state",
                            "type": "string",
                            "enum": state_names
                        },
                        "to": {
                            "description": "target state",
                            "type": "string",
                            "enum": state_names
                        }
                    },
                    "required": ["from", "to"],
                    "additionalProperties": False
                }

            },
            "log_events": {
                "description": "A log message with the given log-level will trigger a notification event.",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                }
            }
        },
        "required": ["subject", "to", "delay"],
        "additionalProperties": False
    }
    return schema


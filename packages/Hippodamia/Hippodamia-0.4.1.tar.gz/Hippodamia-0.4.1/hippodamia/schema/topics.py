def get_schema():
    schema = {
        "type": "object",
        "description": "all topics for the monitoring services",
        "properties": {
            "onboarding-request": {
                "type": "string",
                "example": "/test/hippodamia/onboarding/request",
                "description": "hippodamia listens on this topic for new onboarding request"
            },
            "activity-base": {
                "type": "string",
                "example": "/test/hippodamia/incoming/",
                "description": "this topic will be used as base for each registered service. e.g .../incoming/1/ping"
            },
            "command-end": {
                "type": "string",
                "example": "/test/hippodamia/command/end",
                "description": "end command messages are published to this topic"
            },
            "command-reonboarding": {
                "type": "string",
                "example": "/test/hippodamia/command/reonboarding",
                "description": "reonboarding request are published to this topic"
            },
            "command-ping-on-request": {
                "type": "string",
                "example": "/test/hippodamia/command/ping_on_request",
                "description": "spontaneous ping messages are requested via this topic"
            },
            "command-config-on-request": {
                "type": "string",
                "example": "/test/hippodamia/command/command/config_on_request",
                "description": "spontaneous config messages are requested via this topic"
            },
            "command-runtime-on-request": {
                "type": "string",
                "example": "/test/hippodamia/command/command/runtime_on_request",
                "description": "spontaneous runtime messages are requested via this topic"
            },
            "heartbeat": {
                "type": "string",
                "example": "/test/hippodamia/heartbeat",
                "description": "heartbeat is published via this topic"
            }
        },
        "required": ["onboarding-request", "activity-base", "command-end", "command-reonboarding", "command-ping-on-request",
                     "command-config-on-request", "command-runtime-on-request", "heartbeat"],
        "additionalProperties": False
    }
    return schema

def get_schema():
    schema = {
        "type": "object",
        "description": "all timings for the monitoring service",
        "properties": {
            "onboarding_timeout": {
                "type": "integer",
                "example": "60",
                "description": "seconds * 2 to be waited until an onboarding request should have been processed and a response been recevied"
            },
            "wait_for_message_timeout": {
                "type": "integer",
                "example": "180",
                "description": "seconds - if no message has been received for this period, the service is considered to be inactive"
            },
            "deactivation_timeout": {
                "type": "integer",
                "example": "360",
                "description": "seconds - an inactive service becomes a stopped service after this time span"
            },
            "heartbeat_interval": {
                "type": "integer",
                "example": "60",
                "description": "seconds - send heartbeat to all connected services"
            },
            "archivation_timeout": {
                "type": "integer",
                "example": "86400",
                "description": "seconds - a stopped service is archived after this time span."
            }
        },
        "required": ["onboarding_timeout", "wait_for_message_timeout", "deactivation_timeout",
                     "heartbeat_interval", "archivation_timeout"],
        "additionalProperties": False
    }
    return schema

def get_schema():
    schema = {
        "type": "object",
        "description": "pre-configure which services are expected to be onboarded",
        "properties": {
            "enforcement": {
                "type": "string",
                "example": "none",
                "description": "spontaneously appearing services are either [none]-accepted, [ignore]-ignored, "
                               "[strict]-leads to a error log entry",
                "enum": ["none", "ignore", "strict"]
            },
            "services": {
                "type": "array",
                "description": "list of expected services",
                "items": {
                    "type": "object",
                    "properties": {
                        "gid": {
                            "type": ["string", "integer"],
                            "example": "1",
                            "description": "gid of the service"
                        },
                        "name": {
                            "type": "string",
                            "example": "Thermostat GUI",
                            "description": "name of the service (optional)"
                        },
                        "location": {
                            "type": "string",
                            "example": "vienna",
                            "description": "location of the service (optional)"
                        },
                        "room": {
                            "type": "string",
                            "example": "living room",
                            "description": "room of the service (optional)"
                        },
                        "device": {
                            "type": "string",
                            "example": "thermostat",
                            "description": "device the service is running on (optional)"
                        },
                        "necessity": {
                            "type": "string",
                            "example": "required",
                            "description": "configure if the expected service is [required] or [optional]",
                            "enum": ["required", "optional"]
                        }
                    },
                    "required": ["gid", "necessity"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["enforcement", "services"],
        "additionalProperties": False
    }
    return schema
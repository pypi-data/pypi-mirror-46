def get_schema():
    schema = {
        "type": "object",
        "description": "persistance database",
        "properties": {
            "credentials-file": {
                "type": "string",
                "example": "~/credentials.yaml",
                "description": "credentials for mongodb"
            },
            "mongodb-address": {
                "type": "string",
                "example": "localhost",
                "description": "host name"
            },
            "mongodb-port": {
                "type": "integer",
                "example": 21017,
                "description": "port"
            },
            "database": {
                "type": "string",
                "example": "hippodamia",
                "description": "database name"
            },
            "mongodb-user": {
                "description": "User name for mongodb",
                "type": "string"
            },
            "mongodb-password": {
                "description": "Password for mongodb",
                "type": "string"
            },
            "log-level": {
                "type": "string",
                "example": "DEBUG",
                "description": "log level for mongodb client related messages",
                "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            }
        },
        "required": ["mongodb-address", "mongodb-port", "database", "log-level"],
        "additionalProperties": False
    }
    return schema
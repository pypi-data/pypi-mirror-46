def get_schema():
    schema = {
        "type": "object",
        "description": "web page to view the state of the services",
        "properties": {
            "port": {
                "type": "integer",
                "example": "6060",
                "description": "web server port"
            },
            "webserver-user": {
                "description": "User name for webserver",
                "type": "string"
            },
            "webserver-password": {
                "description": "Password for webserver",
                "type": "string"
            },
            "credentials-file": {
                "type": "string",
                "example": "~/credentials.yaml",
                "description": "if credentials are set, website is password protected"
            },
            "log-level": {
                "type": "string",
                "example": "DEBUG",
                "description": "log level for mongodb client related messages",
                "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            }
        },
        "required": ["port", "log-level"],
        "additionalProperties": False
    }
    return schema
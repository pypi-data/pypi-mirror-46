def get_schema():
    schema = {
                "type": "object",
                "description": "intervals in seconds for different tasks of the monitoring agent - transmitted in the "
                               "onboarding response message",
                "properties": {
                    "send-ping": {
                        "description": "interval in seconds for the scheduler to send a ping message to the "
                                       "monitoring service. 0 deactivates the scheduler. example: 60 seconds.",
                        "type": "integer"
                    },
                    "send-runtime": {
                        "description": "interval in seconds for the scheduler to send a runtime message to the "
                                       "monitoring service. 0 deactivates the scheduler. example: 500 seconds.",
                        "type": "integer"
                    },
                    "send-config": {
                        "description": "interval in seconds for the scheduler to send a config message to the "
                                       "monitoring service. 0 deactivates the scheduler. example: 3600 seconds.",
                        "type": "integer"
                    },
                    "expect-heartbeat": {
                        "description": "maximum interval in seconds until a heartbeat message from the monitoring"
                                       "service should be received. If violated, the agent start the re-onboarding"
                                       "procedures. 0 deactivates this feature. example: 500 seconds.",
                        "type": "integer"
                    },
                },
                "required": ["send-ping", "send-runtime", "send-config", "expect-heartbeat"]
            }
    return schema

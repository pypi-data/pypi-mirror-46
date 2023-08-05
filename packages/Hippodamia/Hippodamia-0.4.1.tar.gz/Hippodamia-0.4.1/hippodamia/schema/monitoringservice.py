import hippodamia.schema.topics as topics
import hippodamia.schema.service_timings as service_timings
import hippodamia.schema.agent_timings as agent_timings
import hippodamia.schema.expected_services as expected_services
import hippodamia.schema.mongodb as mongodb
import hippodamia.schema.webserver as webserver
import hippodamia.schema.email as email


def get_schema():
    schema = {
        "monitoringservice": {
            "description": "Hippodamia observes the state of all registered microservices (aka watch dog).",
            "type": "object",
            "properties": {
                "topics": topics.get_schema(),
                "service-timings": service_timings.get_schema(),
                "agent-timings": agent_timings.get_schema(),
                "expected-services": expected_services.get_schema(),
                "mongodb": mongodb.get_schema(),
                "webserver": webserver.get_schema(),
                "email": email.get_schema()
            },
            "required": ["topics", "agent-timings", "service-timings", "expected-services"],
            "additionalProperties": False
        }
    }
    return schema


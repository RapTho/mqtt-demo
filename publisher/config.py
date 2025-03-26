class Config:
    BROKER_ADDRESS = "localhost"
    USERNAME = "student1"
    PASSWORD = "password1"
    TOPIC = "student1/topic"
    PORT = 1883
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
        },
        "required": ["id", "message"]
    }

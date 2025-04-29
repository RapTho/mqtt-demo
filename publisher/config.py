class Config:
    BROKER_ADDRESS = "127.0.0.1"
    # BROKER_ADDRESS = "mosquitto-raphael.1thahhsghj4d.eu-de.codeengine.appdomain.cloud"
    # BROKER_ADDRESS = "10.243.0.83"
    USERNAME = "student1"
    PASSWORD = "password1"
    TOPIC = "student1/topic"
    PORT = 1883
    # PORT = 8083
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
        },
        "required": ["id", "message"]
    }

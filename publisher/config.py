import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "localhost")
    USERNAME = os.getenv("USERNAME", "student1")
    PASSWORD = os.getenv("PASSWORD", "password1")
    TOPIC = os.getenv("TOPIC", "student1/topic")
    PORT = int(os.getenv("PORT", 1883))
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
        },
        "required": ["id", "message"]
    }

import os
import json
from dotenv import load_dotenv

try:
    load_dotenv()
except FileNotFoundError:
    print("No .env file found")

class Config:
    DEFAULT_SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
        },
        "required": ["id", "message"]
    }
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "localhost").strip('"\'')
    USERNAME = os.getenv("USERNAME", "student1").strip('"\'')
    PASSWORD = os.getenv("PASSWORD", "password1").strip('"\'')
    TOPIC = os.getenv("TOPIC", "student1/topic").strip('"\'')
    PORT = int(os.getenv("PORT", 1883))
    SCHEMA = json.loads(os.getenv("SCHEMA", json.dumps(DEFAULT_SCHEMA)).strip('"\''))
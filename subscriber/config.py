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
    CLOUDANT_USERNAME = os.getenv("CLOUDANT_USERNAME", "apikey-v2-XXX").strip('"\'')
    CLOUDANT_PASSWORD = os.getenv("CLOUDANT_PASSWORD", "myCloudantPassword").strip('"\'')
    CLOUDANT_DB_NAME = os.getenv("CLOUDANT_DB_NAME", "raphael-test").strip('"\'')
    CLOUDANT_URL = os.getenv("CLOUDANT_URL", "https://e11b279a-7332-4e48-846e-886a31a1b101-bluemix.cloudantnosqldb.appdomain.cloud").strip('"\'')
    SCHEMA = json.loads(os.getenv("SCHEMA", json.dumps(DEFAULT_SCHEMA)).strip('"\''))
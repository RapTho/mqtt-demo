class Config:
    BROKER_ADDRESS = "localhost"
    USERNAME = "student1"
    PASSWORD = "password1"
    TOPIC = "student1/topic"
    PORT = 1883
    CLOUDANT_USERNAME = "apikey-v2-XXX"
    CLOUDANT_PASSWORD = "myPassword"
    CLOUDANT_DB_NAME = "raphael-test"
    CLOUDANT_URL = "https://e11b279a-7332-4e48-846e-886a31a1b101-bluemix.cloudantnosqldb.appdomain.cloud"
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
        },
        "required": ["id", "message"]
    }
import requests
from datetime import datetime
from config import Config

class CloudantForwarder:
    def forward_message(self, message):
        try:
            url = f"{Config.CLOUDANT_HOST}/{Config.CLOUDANT_DB_NAME}"
            auth = (Config.CLOUDANT_USERNAME, Config.CLOUDANT_PASSWORD)
            headers = {"Content-Type": "application/json"}
            data = {"message": message}
            response = requests.post(url, auth=auth, headers=headers, json=data)
            if response.status_code == 201:
                print(f"[{datetime.now()}] Message forwarded to Cloudant database successfully.")
            else:
                print(f"[{datetime.now()}] Failed to forward message to Cloudant database. Status code: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Error while forwarding message to Cloudant database: {e}")

import requests
from datetime import datetime
from config import Config

class CloudantForwarder:
    def forward_message(self, message):
        try:
            # First attempt with current token
            response = self._send_message(message)
            
            # If unauthorized (401), refresh token and retry once
            if response.status_code == 401:
                print(f"[{datetime.now()}] Received 401 Unauthorized. Token may have expired, refreshing...")
                success, result = Config.exchange_api_key_for_token()
                
                if success:
                    print(f"[{datetime.now()}] Token refreshed successfully, retrying request...")
                    response = self._send_message(message)
                    
                    if response.status_code == 201:
                        print(f"[{datetime.now()}] Message forwarded to Cloudant database successfully after token refresh.")
                    else:
                        print(f"[{datetime.now()}] Failed to forward message after token refresh. Status code: {response.status_code}")
                        print(f"[{datetime.now()}] Response: {response.text}")
                else:
                    print(f"[{datetime.now()}] ERROR: Failed to refresh token: {result}")
                    print(f"[{datetime.now()}] Message could not be forwarded to Cloudant database")
            elif response.status_code == 201:
                print(f"[{datetime.now()}] Message forwarded to Cloudant database successfully.")
            else:
                print(f"[{datetime.now()}] Failed to forward message to Cloudant database. Status code: {response.status_code}")
                print(f"[{datetime.now()}] Response: {response.text}")
                
        except Exception as e:
            print(f"[{datetime.now()}] Error while forwarding message to Cloudant database: {e}")
    
    def _send_message(self, message):
        """Helper method to send message to Cloudant with current token"""
        url = f"{Config.CLOUDANT_HOST}/{Config.CLOUDANT_DB_NAME}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.CLOUDANT_BEARER_TOKEN}"
        }
        data = {"message": message}
        return requests.post(url, headers=headers, json=data)

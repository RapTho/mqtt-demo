import os
import json
import requests
from datetime import datetime
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
    CLOUDANT_API_KEY = os.getenv("CLOUDANT_API_KEY", "").strip('"\'')
    CLOUDANT_DB_NAME = os.getenv("CLOUDANT_DB_NAME", "raphael-test").strip('"\'')
    CLOUDANT_HOST = os.getenv("CLOUDANT_HOST", "https://e11b279a-7332-4e48-846e-886a31a1b101-bluemix.cloudantnosqldb.appdomain.cloud").strip('"\'')
    SCHEMA = json.loads(os.getenv("SCHEMA", json.dumps(DEFAULT_SCHEMA)).strip('"\''))
    
    # IAM token will be set after exchange
    CLOUDANT_BEARER_TOKEN = None
    
    @staticmethod
    def exchange_api_key_for_token():
        """
        Exchange IBM Cloud API key for IAM Bearer token.
        Returns tuple: (success: bool, token_or_error_message: str)
        """
        if not Config.CLOUDANT_API_KEY:
            return False, "CLOUDANT_API_KEY environment variable is not set"
        
        try:
            print(f"[{datetime.now()}] Exchanging API key for IAM Bearer token...")
            
            url = "https://iam.cloud.ibm.com/identity/token"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": Config.CLOUDANT_API_KEY
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                Config.CLOUDANT_BEARER_TOKEN = token_data.get("access_token")
                
                if Config.CLOUDANT_BEARER_TOKEN:
                    print(f"[{datetime.now()}] Successfully obtained IAM Bearer token")
                    return True, Config.CLOUDANT_BEARER_TOKEN
                else:
                    return False, "No access_token in response"
            else:
                error_msg = f"Token exchange failed with status code {response.status_code}"
                try:
                    error_detail = response.json()
                    if "errorMessage" in error_detail:
                        error_msg += f": {error_detail['errorMessage']}"
                    elif "error_description" in error_detail:
                        error_msg += f": {error_detail['error_description']}"
                except:
                    error_msg += f": {response.text}"
                return False, error_msg
                
        except requests.exceptions.Timeout:
            return False, "Token exchange request timed out"
        except requests.exceptions.ConnectionError:
            return False, "Failed to connect to IAM service"
        except Exception as e:
            return False, f"Unexpected error during token exchange: {str(e)}"
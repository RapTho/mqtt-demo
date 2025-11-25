from mqtt_subscriber import MqttSubscriber
from config import Config
from datetime import datetime
import time
import sys

def main():
    # Exchange API key for Bearer token on bootup
    print(f"[{datetime.now()}] Starting subscriber application...")
    success, result = Config.exchange_api_key_for_token()
    
    if not success:
        print(f"[{datetime.now()}] ERROR: Failed to obtain IAM Bearer token")
        print(f"[{datetime.now()}] Reason: {result}")
        print(f"[{datetime.now()}] Please check your CLOUDANT_API_KEY environment variable")
        sys.exit(1)
    
    print(f"[{datetime.now()}] IAM authentication successful, starting MQTT subscriber...")
    
    subscriber = MqttSubscriber()
    try:
        subscriber.start()
        while not subscriber.connected:
            if subscriber.error:
                print(f"Error: {subscriber.error}")
                sys.exit(1)
            time.sleep(0.1)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
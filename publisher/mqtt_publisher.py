import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import signal
import json
from jsonschema import validate, ValidationError
from config import Config

class MqttPublisher:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(Config.USERNAME, Config.PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[{datetime.now()}] Connected successfully with result code {rc}")
            try:
                message = self.create_message(1, "Hello from student1!")
                result = client.publish(Config.TOPIC, payload=json.dumps(message), qos=1)
                result_code = result.rc
                if result_code != mqtt.MQTT_ERR_SUCCESS:
                    print(f"[{datetime.now()}] Failed to publish message '{message}' to topic '{Config.TOPIC}'. Result code: {result_code}")
                else:
                    print(f"[{datetime.now()}] Message '{message}' sent to topic '{Config.TOPIC}' successfully.")
            except Exception as e:
                print(f"[{datetime.now()}] Error while publishing message: {e}")
                sys.exit(1)
        else:
            print(f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}")
            sys.exit(1)

    def create_message(self, id, message):
        return {
            "id": id,
            "message": message
        }

    def validate_message(self, message):
        try:
            validate(instance=message, schema=Config.SCHEMA)
            return True
        except ValidationError as e:
            print(f"[{datetime.now()}] Message is invalid. Error: {e}")
            return False

    def on_log(self, client, userdata, level, buf):
        print(f"[{datetime.now()}] MQTT Log: {buf}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"[{datetime.now()}] Unexpected disconnection. Result code: {rc}")
            sys.exit(1)

    def handle_sigterm(self, signal_number, frame):
        print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
        self.client.disconnect()
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self.handle_sigterm)
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        try:
            print(f"[{datetime.now()}] Starting publisher...")
            self.client.connect(Config.BROKER_ADDRESS, Config.PORT)
            self.client.loop_forever()
        except Exception as e:
            print(f"[{datetime.now()}] Failed to start publisher: {e}")
            sys.exit(1)

if __name__ == "__main__":
    MqttPublisher().start()

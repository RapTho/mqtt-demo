import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import signal
import json
from jsonschema import validate, ValidationError
from config import Config

class MqttSubscriber:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(Config.USERNAME, Config.PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[{datetime.now()}] Connected successfully with result code {rc}")
            try:
                client.subscribe(Config.TOPIC, qos=1)
                print(f"[{datetime.now()}] Subscribed to topic: {Config.TOPIC}")
                print(f"[{datetime.now()}] Now listening on port {Config.PORT}...")
            except Exception as e:
                print(f"[{datetime.now()}] Error while subscribing to topic '{Config.TOPIC}': {e}")
                sys.exit(1)
        else:
            print(f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}")
            sys.exit(1)

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            print(f"[{datetime.now()}] Received message: {message} on topic {msg.topic}")
            # Validate message against schema
            self.validate_message(message)
        except Exception as e:
            print(f"[{datetime.now()}] Error while processing received message: {e}")

    def validate_message(self, message):
        try:
            # Load JSON message
            json_message = json.loads(message)
            validate(instance=json_message, schema=Config.SCHEMA)
            from cloudant_forwarder import CloudantForwarder
            CloudantForwarder().forward_message(message)
        except json.JSONDecodeError as e:
            print(f"[{datetime.now()}] Error parsing JSON message: {e}")
        except ValidationError as e:
            print(f"[{datetime.now()}] Message is invalid. Error: {e}")

    def on_log(self, client, userdata, level, buf):
        print(f"[{datetime.now()}] MQTT Log: {buf}")

    def on_disconnect(self, client, userdata, rc, properties, reason_code):
        if rc != 0:
            print(f"[{datetime.now()}] Unexpected disconnection. Result code: {rc}, reason code: {reason_code}")
            sys.exit(1)
        else:
            print(f"[{datetime.now()}] Disconnected successfully.")

    def start(self):
        signal.signal(signal.SIGINT, self.handle_sigterm)
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        try:
            print(f"[{datetime.now()}] Starting subscriber...")
            self.client.connect(Config.BROKER_ADDRESS, Config.PORT)
            self.client.loop_forever()
        except Exception as e:
            print(f"[{datetime.now()}] Failed to start subscriber: {e}")
            sys.exit(1)

    def handle_sigterm(self, signal_number, frame):
        print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
        self.client.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    MqttSubscriber().start()

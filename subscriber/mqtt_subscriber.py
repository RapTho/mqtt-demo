import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import ssl
import signal
import json
import time
from jsonschema import validate, ValidationError
from config import Config

class MqttSubscriber:
    def __init__(self):
        self.running = False
        self.connected = False
        self.error = None
        if Config.PORT == 8083:
            self.client = mqtt.Client(transport="websockets")
        elif Config.PORT == 443:
            self.client = mqtt.Client(transport="websockets")
            self.client.tls_set(None, cert_reqs=ssl.CERT_NONE) # Ignore TLS verification
        else:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(Config.USERNAME, Config.PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log


    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print(f"[{datetime.now()}] Connected successfully with result code {rc}")
            try:
                client.subscribe(Config.TOPIC, qos=1)
                print(f"[{datetime.now()}] Subscribed to topic: {Config.TOPIC}")
            except Exception as e:
                self.error = f"[{datetime.now()}] Error while subscribing to topic '{Config.TOPIC}': {e}"
        elif rc == 5:
            self.error = f"[{datetime.now()}] Connection failed! Unauthorized - please check your username / password"
        else:
            self.error = f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}"

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            print(f"[{datetime.now()}] Received message: {message} on topic {msg.topic}")
            self.validate_message(message)
        except Exception as e:
            print(f"[{datetime.now()}] Error while processing received message: {e}")

    def validate_message(self, message):
        try:
            json_message = json.loads(message)
            validate(instance=json_message, schema=Config.SCHEMA)
            from cloudant_forwarder import CloudantForwarder
            CloudantForwarder().forward_message(message)
        except json.JSONDecodeError as e:
            print(f"[{datetime.now()}] Error parsing JSON message: {e}")
        except ValidationError as e:
            print(f"[{datetime.now()}] Message is invalid. Error: {e}")
        except Exception as e:
            print(f"[{datetime.now()}] Error validating message: {e}")


    def on_log(self, client, userdata, level, buf):
        print(f"[{datetime.now()}] MQTT Log: {buf}")

    def on_disconnect(self, client, userdata, reason, properties=None, *args):
        self.client.loop_stop()
        self.connected = False
        self.running = False
        if reason != 0 and not self.error:
            self.error = f"[{datetime.now()}] Unexpected disconnection. Result code: {reason}"
        else:
            print(f"[{datetime.now()}] Disconnected")

    def handle_sigterm(self, signal_number, frame):
        print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
        self.stop()
        sys.exit(0)

    def start(self):
        if not self.running:
            signal.signal(signal.SIGINT, self.handle_sigterm)
            signal.signal(signal.SIGTERM, self.handle_sigterm)
            try:
                print(f"[{datetime.now()}] Starting subscriber...")
                self.client.connect(Config.BROKER_ADDRESS, Config.PORT)
                self.client.loop_start()
                self.running = True
                print(f"[{datetime.now()}] Started subscriber")
                
                # Instead of using signal.pause(), which doesn't work on Windows.
                while self.running:
                    time.sleep(0.5)
                    
            except ConnectionRefusedError:
                raise Exception(f"[{datetime.now()}] Connection refused")
            except TimeoutError:
                raise Exception(f"[{datetime.now()}] Connection timed out")
            except Exception as e:
                raise Exception(f"[{datetime.now()}] Failed to start subscriber: {e}")

    def stop(self):
        if self.running:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            self.running = False
            print(f"[{datetime.now()}] Stopped subscriber")
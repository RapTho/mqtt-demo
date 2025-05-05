import json
import ssl
import signal
import paho.mqtt.client as mqtt
from datetime import datetime
from jsonschema import validate, ValidationError
from config import Config

class MqttPublisher:
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
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print(f"[{datetime.now()}] Connected successfully with result code {rc}")
        elif rc == 5:
            self.error = f"[{datetime.now()}] Connection failed! Unauthorized - please check your username / password"
        else:
            self.error = f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}"


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

    def handle_sigterm(self, signal_number, frame):
        print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
        self.stop()

    def start(self):
        if not self.running:
            signal.signal(signal.SIGINT, self.handle_sigterm)
            signal.signal(signal.SIGTERM, self.handle_sigterm)
            try:
                print(f"Trying to connect to {Config.BROKER_ADDRESS}:{Config.PORT}")
                self.client.connect(Config.BROKER_ADDRESS, Config.PORT)
                self.client.loop_start()
                self.running = True
                print(f"[{datetime.now()}] Started publisher")
            except ConnectionRefusedError:
                raise Exception(f"[{datetime.now()}] Connection refused")
            except TimeoutError:
                raise Exception(f"[{datetime.now()}] Connection timed out")
            except Exception as e:
                raise Exception(f"[{datetime.now()}] Failed to start publisher - {e}")

    def stop(self):
        if self.running:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            self.running = False
            print(f"[{datetime.now()}] Stopped publisher")

    def send_message(self, message):
        if self.running:
            try:
                result = self.client.publish(Config.TOPIC, payload=json.dumps(message), qos=1)
                result_code = result.rc
                if result_code != mqtt.MQTT_ERR_SUCCESS:
                    raise Exception(f"[{datetime.now()}] Failed to publish message '{message}' to topic '{Config.TOPIC}'. Result code: {result_code}")
                else:
                    print(f"[{datetime.now()}] Message '{message}' sent to topic '{Config.TOPIC}' successfully.")
            except Exception as e:
                raise Exception(f"[{datetime.now()}] Error while publishing message: {e}")
        else:
            raise Exception(f"[{datetime.now()}] Publisher is not running.")
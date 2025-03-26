import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import signal

broker_address = "localhost"
username = "student1"
password = "password1"
topic = "student1/topic"
port = 1883

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{datetime.now()}] Connected successfully with result code {rc}")
        try:
            message = "Hello from student1!"
            result = client.publish(topic, payload=message, qos=1)
            result_code = result.rc
            if result_code != mqtt.MQTT_ERR_SUCCESS:
                print(f"[{datetime.now()}] Failed to publish message '{message}' to topic '{topic}'. Result code: {result_code}")
            else:
                print(f"[{datetime.now()}] Message '{message}' sent to topic '{topic}' successfully.")
        except Exception as e:
            print(f"[{datetime.now()}] Error while publishing message: {e}")
            sys.exit(1)
    else:
        print(f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}")
        sys.exit(1)

def on_log(client, userdata, level, buf):
    print(f"[{datetime.now()}] MQTT Log: {buf}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[{datetime.now()}] Unexpected disconnection. Result code: {rc}")
        sys.exit(1)

def handle_sigterm(signal_number, frame):
    print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log

try:
    print(f"[{datetime.now()}] Starting publisher...")
    client.connect(broker_address, port)
    client.loop_forever()
except Exception as e:
    print(f"[{datetime.now()}] Failed to start publisher: {e}")
    sys.exit(1)

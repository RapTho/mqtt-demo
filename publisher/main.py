import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import signal

# Define MQTT broker details
broker_address = "localhost"
username = "student1"
password = "password1"
topic = "student1/topic"
port = 1883

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{datetime.now()}] Connected successfully with result code {rc}")
        try:
            # Publish a message after connecting
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

# Callback for logging internal MQTT events
def on_log(client, userdata, level, buf):
    print(f"[{datetime.now()}] MQTT Log: {buf}")

# Callback for when there is a disconnect
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[{datetime.now()}] Unexpected disconnection. Result code: {rc}")
        sys.exit(1)

# Signal handler to gracefully shut down the publisher
def handle_sigterm(signal_number, frame):
    print(f"[{datetime.now()}] Received termination signal. Disconnecting...")
    client.disconnect()
    sys.exit(0)

# Attach signal handlers for SIGINT and SIGTERM
signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

# Create an MQTT client (explicitly specifying protocol MQTTv5)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set username and password for authentication
client.username_pw_set(username, password)

# Assign the callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log

# Connect to the broker
try:
    print(f"[{datetime.now()}] Starting publisher...")
    client.connect(broker_address, port)
    client.loop_forever()
except Exception as e:
    print(f"[{datetime.now()}] Failed to start publisher: {e}")
    sys.exit(1)

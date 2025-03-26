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
            # Subscribe to the topic after connecting
            client.subscribe(topic, qos=1)
            print(f"[{datetime.now()}] Subscribed to topic: {topic}")
            print(f"[{datetime.now()}] Now listening on port {port}...")
        except Exception as e:
            print(f"[{datetime.now()}] Error while subscribing to topic '{topic}': {e}")
            sys.exit(1)
    else:
        print(f"[{datetime.now()}] Failed to connect to broker. Result code: {rc}")
        sys.exit(1)

# Callback for when a message is received
def on_message(client, userdata, msg):
    try:
        print(f"[{datetime.now()}] Received message: {msg.payload.decode()} on topic {msg.topic}")
    except Exception as e:
        print(f"[{datetime.now()}] Error while processing received message: {e}")

# Callback for logging internal MQTT events
def on_log(client, userdata, level, buf):
    print(f"[{datetime.now()}] MQTT Log: {buf}")

# Corrected callback for when there is a disconnect
def on_disconnect(client, userdata, rc, properties, reason_code):
    if rc != 0:
        print(f"[{datetime.now()}] Unexpected disconnection. Result code: {rc}, reason code: {reason_code}")
        sys.exit(1)
    else:
        print(f"[{datetime.now()}] Disconnected successfully.")

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
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_log = on_log

# Connect to the broker
try:
    print(f"[{datetime.now()}] Starting subscriber...")
    client.connect(broker_address, port)
    client.loop_forever()
except Exception as e:
    print(f"[{datetime.now()}] Failed to start subscriber: {e}")
    sys.exit(1)
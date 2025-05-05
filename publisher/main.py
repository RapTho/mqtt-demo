import sys
import time
from mqtt_publisher import MqttPublisher

def main():
    publisher = MqttPublisher()
    try:
        publisher.start()
        while not publisher.connected:
            if publisher.error:
                print(f"{publisher.error}")
                sys.exit(1)
            time.sleep(0.1)
        message = publisher.create_message(1, "Hello from student1!")
        publisher.send_message(message)
        time.sleep(1) 
        publisher.stop()
        sys.exit(0)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

from mqtt_subscriber import MqttSubscriber
import time
import sys

def main():
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
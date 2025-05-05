# MQTT Publisher App

## Introduction

This is a Python application that publishes messages to an MQTT broker. It uses the Paho MQTT library to connect to the broker and publish messages to a specified topic.

## Installation

To install the required libraries, create a virtual environment and install the requirements using pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

To configure the app, create a .env file in the root of the project with the following variables:

- BROKER_ADDRESS: the address of the MQTT broker
- USERNAME: the username to use when connecting to the broker
- PASSWORD: the password to use when connecting to the broker
- PORT: the port to use when connecting to the broker
- TOPIC: the topic to publish messages to
- SCHEMA: the message's schema

Example .env file:

```
BROKER_ADDRESS=localhost
USERNAME=student1
PASSWORD=password1
PORT=1883
TOPIC=student1/topic
SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "message": {"type": "string"},
    },
    "required": ["id", "message"]
}
```

## Send a message

To send a message, run the app by executing the main.py file:

```bash
python main.py
```

# MQTT Subscriber App

## Introduction

This is a Python application that subscribes to messages from an MQTT broker. It uses the Paho MQTT library to connect to the broker and forwards messages to a Cloudant database on IBM Cloud.

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
- CLOUDANT_USERNAME: the username to use when connecting to the Cloudant database
- CLOUDANT_PASSWORD: the password to use when connecting to the Cloudant database
- CLOUDANT_DB_NAME: the name of the Cloudant database
- CLOUDANT_URL: the host of the Cloudant database
- SCHEMA: the message's schema

Example .env file:

```
BROKER_ADDRESS="localhost"
USERNAME="student1"
PASSWORD="password1"
TOPIC="student1/topic"
PORT=8083
CLOUDANT_USERNAME="apikey-v2-xxxx"
CLOUDANT_PASSWORD="myCloudantPassword"
CLOUDANT_DB_NAME="raphael-test"
CLOUDANT_URL="https://e11b279a-7332-4e48-846e-886a31a1b101-bluemix.cloudantnosqldb.appdomain.cloud"
SCHEMA={"type": "object", "properties": {"id": {"type": "integer"}, "message": {"type": "string"}}, "required": ["id", "message"]}


```

## Start the subscriber app

To start the subscriber, run the main.py file:

```bash
python main.py
```

## Build and deploy app

To build the container image and deploy it on IBM Code Engine, you can refer to the instructions in the [mosquitto folder](../mosquitto/).

The steps will be similar but another [Containerfile](./Containerfile) is provided

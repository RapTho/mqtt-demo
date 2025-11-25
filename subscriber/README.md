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
- CLOUDANT_API_KEY: the IBM Cloud API key for Cloudant authentication (will be exchanged for a Bearer token)
- CLOUDANT_DB_NAME: the name of the Cloudant database
- CLOUDANT_HOST: the host of the Cloudant database
- SCHEMA: the message's schema

Example .env file:

```
BROKER_ADDRESS="localhost"
USERNAME="student1"
PASSWORD="password1"
TOPIC="student1/topic"
PORT=8083
CLOUDANT_API_KEY="your-ibm-cloud-api-key-here"
CLOUDANT_DB_NAME="raphael-test"
CLOUDANT_HOST="https://e11b279a-7332-4e48-846e-886a31a1b101-bluemix.cloudantnosqldb.appdomain.cloud"
SCHEMA={"type": "object", "properties": {"id": {"type": "integer"}, "message": {"type": "string"}}, "required": ["id", "message"]}
```

## Authentication

The application uses IBM Cloud IAM (Identity and Access Management) for Cloudant authentication:

1. On startup, the application exchanges the `CLOUDANT_API_KEY` for a Bearer token using the IBM Cloud IAM token service
2. The Bearer token is then used to authenticate all requests to the Cloudant database
3. If the token exchange fails, the application will exit gracefully with an error message

## Start the subscriber app

To start the subscriber, run the main.py file:

```bash
python main.py
```

## Build and deploy app

To build the container image and deploy it on IBM Code Engine. The process is extensively documented in the [mosquitto folder](../mosquitto/).

The steps will be similar but another [Containerfile](./Containerfile) is provided

Set new environment variables for the deployment process

```bash
export RESOURCE_GROUP=iot-digital-engineering
export CR_NAMESPACE=hslu-iot-digital-engineering
export IMAGE_NAME=subscriber-raphael
export IMAGE_TAG=1.0
```

Use secret and configmap from the kubernetes/subscriber folder to create new configuration for the subscriber. <br />

After building and pushing your container image, you can deploy it. This time we will deploy the subscriber as a `job` of type `daemon`, as the subscriber doesn't expose any endpoint.

Create the daemon job

```bash
ibmcloud ce job create --mode daemon --name subscriber-${USER} --image de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG} --registry-secret ibm-container-registry-${USER} --env-from-configmap subscriber-conf-${USER} --env-from-secret subscriber-secret-${USER} --cpu 0.25 --memory 0.5G
```

Run an instance of the daemon job

```bash
ibmcloud ce jobrun submit --name subscriber-run-${USER} --job subscriber-${USER}
```

## Troubleshooting

### Connect to IBM Code Engine's Kubernetes-API

To use `kubectl` with IBM Code Engine, you can set the context as documented [here](https://cloud.ibm.com/docs/codeengine?topic=codeengine-kubernetes)

```bash
ibmcloud ce project select -n iot-digital-engineering --kubecfg
```

Now you can do everything you're authorized to :)

### Get Pods

```bash
kubectl get pods
```

### Check logs of a specific pod

Replace `myPodName` with the name of your pod. You can also use the `-f` option to subscribe to incoming logs

```bash
kubectl logs pod/myPodName
```

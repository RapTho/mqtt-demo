# mqtt-demo

Demo of using the Mosquitto MQTT broker and a subscriber application to forward messages to IBM Cloudant

## Pre-requisites

#### ibmcloud CLI

Install the Command Line Interface tool to interact with IBM Cloud:<br />
[https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli](https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli)

Optionally, you can also enable the autocompletion:<br />
[https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete](https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete)

Install the Code Engine and Container Registry plugin

```
ibmcloud plugin install code-engine container-registry
```

Login

```
ibmcloud login --sso
```

Set environment variables

```
export RESOURCE_GROUP=iot-digital-engineering
export CR_NAMESPACE=hslu-iot-digital-engineering
export IMAGE_NAME=mosquitto-custom
export IMAGE_TAG=1.0
```

Select resource group

```
ibmcloud target -g ${RESOURCE_GROUP}
```

Select IBM Code Engine project

```
ibmcloud ce project select --name myProjectName
```

#### Container engine

Install podman: [https://podman.io/docs/installation](https://podman.io/docs/installation)

## Build the mosquitto container image

Adjust the [acl](./mosquitto/acl.txt) and [passwords](./mosquitto/generatePasswordFile.py) to add/modify/remove access and topics

```
mosquitto
├── Containerfile
├── acl.txt
├── entrypoint.sh
├── generatePasswordFile.py
├── mosquitto.conf
```

Execute the password.txt generation script

```
python generatePasswordFile.py
```

The final folder structure should be like this

```
mosquitto
├── Containerfile
├── acl.txt
├── entrypoint.sh
├── generatePasswordFile.py
├── mosquitto.conf
├── passwords.txt
```

Build the container image

```

podman build -t ${IMAGE_NAME}:${IMAGE_TAG} --layers=false /path/to/Containerfile
```

#### For ARM users

If you build on a machine with a CPU architecture other than `amd64`, you need to build for `amd64` architecture

```
podman build -t ${IMAGE_NAME}:${IMAGE_TAG} --layers=false --arch=amd64 /path/to/Containerfile
```

#### OPTIONAL: Test locally

Start the container locally and test its connection

```
podman run -d -e MOSQUITTO_CONF="$(cat mosquitto.conf)" \
              -e ACL="$(cat acl.txt)" \
              -e PASSWORDS="$(cat passwords.txt)" \
              -p 1883:1883 -p 9001:9001 --name mosquitto ${IMAGE_NAME}:${IMAGE_TAG}
```

Run the publisher and subscriber apps in two different terminal sessions to test the connection

```
python /path/to/subscriber/main.py
```

```
python /path/to/publisher/main.py
```

## Publish image to IBM Container Registry

```
ibmcloud cr region-set eu-central
ibmcloud cr login --client podman
ibmcloud cr namespace-add ${CR_NAMESPACE}
podman tag mosquitto-custom:1.0 de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
podman push de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
```

Set image retention policy to 2.

```
ibmcloud cr retention-policy-set --images 2 ${CR_NAMESPACE}
```

Create an API Key. `TAKE A NOTE OF THE KEY`

```
ibmcloud iam api-key-create mosquitto-deploy-key-${USER} -d "API Key for to deploy mosquitto on IBM Code Engine"
```

Export the key

```
export API_KEY="myGeneratedAPIKey"
```

Create a pull secret for IBM Code Engine to access the IBM Container Registry

```
ibmcloud ce registry create --name ibm-container-registry-${USER} --server de.icr.io --username iamapikey --password ${API_KEY}
```

## Upload mosquitto configuration, acl and passwords to IBM Code Engine

```
ibmcloud ce configmap create --name conf-${USER} --from-file MOSQUITTO_CONF=mosquitto/mosquitto.conf
ibmcloud ce configmap create --name acl-${USER} --from-file ACL=mosquitto/acl.txt
ibmcloud ce secret create --name passwords-${USER} --from-file PASSWORDS=mosquitto/passwords.txt
```

## Deploy the mosquitto MQTT broker

```
ibmcloud ce app create --name mosquitto-${USER} --image de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG} --registry-secret ibm-container-registry-${USER} --env-from-secret passwords-${USER} --env-from-configmap conf-${USER} --env-from-configmap acl-${USER} --port 1883 --min-scale 1 --max-scale 1 --cpu 0.25 --memory 0.5G
```

# mqtt-demo

Demo of using the Mosquitto MQTT broker and a subscriber application to forward messages to IBM Cloudant

## Pre-requisites

#### ibmcloud CLI

Install the Command Line Interface tool to interact with IBM Cloud:<br />
[https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli](https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli)

Optionally, you can also enable the autocompletion:<br />
[https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete](https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete)

Install the Code Engine plugin

```
ibmcloud plugin install code-engine
```

Select resource group

```
ibmcloud target -g iot-digital-engineering
```

Select IBM Code Engine project

```
ibmcloud ce project select --name myProjectName
```

#### Container engine

Install podman: [https://podman.io/docs/installation](https://podman.io/docs/installation)

## Deploy mosquitto

#### Adjust config

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

#### Run locally

Build the container image

```
podman build -t mosquitto-custom:1.0 .
```

Start the container locally and test its connection

```
podman run -d -e MOSQUITTO_CONF="$(cat mosquitto.conf)" \
              -e ACL="$(cat acl.txt)" \
              -e PASSWORDS="$(cat passwords.txt)" \
              -p 1883:1883 -p 9001:9001 --name mosquitto mosquitto-custom:1.0
```

Run the publisher and subscriber apps in two different terminal sessions to test the connection

```
python subscriber/main.py
```

```
python publisher/main.py
```

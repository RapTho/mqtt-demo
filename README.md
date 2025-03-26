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

Adjust the [acl](./mosquitto/acl.txt) and [passwords](./mosquitto/passwords.txt) file to add/modify/remove access and topics

```
mosquitto
├── Containerfile
├── acl.txt
├── entrypoint.sh
├── mosquitto.conf
└── passwords.txt
```

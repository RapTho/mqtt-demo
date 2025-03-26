#!/bin/bash
# Define paths for configuration files
MOSQUITTO_CONF_PATH="/home/mosquitto/config/mosquitto.conf"
ACL_FILE_PATH="/home/mosquitto/config/acl.txt"
PASSWORD_FILE_PATH="/home/mosquitto/config/passwords.txt"

# Write the Mosquitto configuration file
if [ -n "$MOSQUITTO_CONF" ]; then
  echo "Writing mosquitto.conf..."
  echo "$MOSQUITTO_CONF" > "$MOSQUITTO_CONF_PATH"
else
  echo "No MOSQUITTO_CONF environment variable found. Using default configuration."
fi

# Write the ACL file
if [ -n "$ACL" ]; then
  echo "Writing ACL file..."
  echo "$ACL" > "$ACL_FILE_PATH"
  chmod 700 "$ACL_FILE_PATH"

else
  echo "No ACL environment variable found. Skipping ACL configuration."
fi

# Write the password file
if [ -n "$PASSWORDS" ]; then
  echo "Writing password file..."
  echo "$PASSWORDS" > "$PASSWORD_FILE_PATH"
  chmod 700 "$PASSWORD_FILE_PATH"
else
  echo "No PASSWORDS environment variable found. Skipping password configuration."
fi

# Start Mosquitto with the generated configuration
echo "Starting Mosquitto..."
exec /usr/sbin/mosquitto -c "$MOSQUITTO_CONF_PATH"

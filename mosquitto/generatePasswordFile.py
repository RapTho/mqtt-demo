import subprocess
import os

try:
    subprocess.run(["mosquitto_passwd", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
except FileNotFoundError:
    print("Error: 'mosquitto_passwd' is not installed or not found in PATH.")
    exit(1)

PASSWORD_FILE = "passwords.txt"

users_and_passwords = {
    "student1": "password1",
    "student2": "password2",
    "student3": "password3",
    "student4": "password4",
    "student5": "password5",
    "student6": "password6",
    "student7": "password7",
    "student8": "password8",
    "student9": "password9",
    "student10": "password10",
}

with open(PASSWORD_FILE, "w") as f:
    pass  # Just create an empty file or overwrite if it already exists

for user, password in users_and_passwords.items():
    try:
        subprocess.run(
            ["mosquitto_passwd", "-b", PASSWORD_FILE, user, password],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while adding user '{user}': {e.stderr.decode().strip()}")
        exit(1)

os.chmod(PASSWORD_FILE, 0o700)

print(f"Password file '{PASSWORD_FILE}' created with permissions set to 700.")

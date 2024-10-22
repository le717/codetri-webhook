#!/usr/bin/env bash
# Make sure the virtualenv package is installed
apt install python3-venv -y

# Create the virutalenv
python3 -m venv venv

# Install the app deps
venv/bin/python -m pip install pip --upgrade
venv/bin/python ./scripts/get-requirements.py
venv/bin/pip install -r ./requirements.txt

# Make the scripts executable
chmod u+x ./scripts/start.sh ./scripts/stop.sh ./scripts/run-app.sh

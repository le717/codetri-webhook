#!/usr/bin/env bash
# Make sure the virtualenv package is installed
apt install python3-venv -y

# Create the virutalenv
python3 -m venv venv

# Install the app deps
venv/bin/python -m pip install pip --upgrade
venv/bin/python ./get-requirements.py
venv/bin/pip install -r ./requirements.txt

# Make the scripts executable
chmod u+x ./start.sh ./stop.sh ./run-app.sh

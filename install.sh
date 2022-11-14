#!/usr/bin/env bash
# Create the virutalenv
python -m virtualenv venv

# Install the app deps
venv/bin/python -m pip install pip --upgrade
venv/bin/pip install toml --upgrade
venv/bin/python ./get-requirements.py
venv/bin/pip install -r ./requirements.txt

# Make the scripts executable
chmod u+x ./start.sh ./stop.sh ./run-app.sh

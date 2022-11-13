#!/usr/bin/env bash
python -m virtualenv venv
venv/bin/python -m pip install pip --upgrade
venv/bin/pip install toml --upgrade
venv/bin/python ./get-requirements.py
venv/bin/pip install -r ./requirements.txt

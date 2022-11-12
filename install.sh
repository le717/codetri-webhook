#!/usr/bin/env bash
python -m virtualenv env
env/bin/python -m pip install pip --upgrade
env/bin/pip install toml --upgrade
env/bin/python ./get-requirements.py
env/bin/pip install -r ./requirements.txt

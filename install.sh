#!/usr/bin/env bash
virtualenv env
env/bin/pip install toml --upgrade
env/bin/python ./get-requirements.py
env/bin/pip install -r ./requirements.txt

#!/usr/bin/env bash

# Stop the supervisord process
# TODO: Do this!

# Stop the gunicorn processes
lsof -t -i:$port | xargs kill -9

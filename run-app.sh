#!/usr/bin/env bash
env/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 --log-level error --access-logfile ./log/gunicorn.access.log --error-logfile ./log/gunicorn.error.log wsgi:app

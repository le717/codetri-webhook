#!/usr/bin/env bash
gunicorn --bind 127.0.0.1:6000 --workers 2 --log-level error --access-logfile ./log/access.log --error-logfile ./log/error.log wsgi:app

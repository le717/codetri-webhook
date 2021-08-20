#!/usr/bin/env bash
gunicorn --bind 127.0.0.1:6000 --workers 2 --log-level error --access-logfile /var/log/webhook.access.log --error-logfile /var/log/webhook.error.log wsgi:app

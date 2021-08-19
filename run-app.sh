#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /var/log/webhook.access.log --error-logfile /var/log/webhook.error.log wsgi:app

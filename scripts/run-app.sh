#!/usr/bin/env bash
trim() {
    # https://stackoverflow.com/a/3352015
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}

# Get the bind port
webhook_bind_port="$(< ./secrets/BIND_PORT)"
webhook_bind_port="$(trim ${webhook_bind_port})"

# Start the app
venv/bin/gunicorn --bind 127.0.0.1:${webhook_bind_port} --workers 2 --log-level error --access-logfile ./log/gunicorn/access.log --error-logfile ./log/gunicorn/error.log wsgi:app

# Commands to help with debugging
# lsof -i :6000
# ps -ef | grep venv/bin/supervisord
# ps -ef | grep venv/bin/gunicorn

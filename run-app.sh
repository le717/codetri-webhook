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
port="$(< ./secrets/BIND_PORT)"
port="$(trim ${port})"

# Start the app
venv/bin/gunicorn --bind 127.0.0.1:${port} --workers 2 --log-level error --access-logfile ./log/access.log --error-logfile ./log/error.log wsgi:app

# Commands to help with debugging
# sudo lsof -i :6000
# ps -ef | grep supervisord
# ps -ef | grep gunicorn

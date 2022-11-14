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
webhook_bind_port="$(trim ${port})"

# Stop the supervisord process
# TODO: Do this!

# Stop the gunicorn processes
lsof -t -i :$webhook_bind_port | xargs kill -9

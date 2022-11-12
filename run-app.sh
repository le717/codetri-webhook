#!/usr/bin/env bash
# https://stackoverflow.com/a/3352015
trim() {
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}

port=$(< ./secrets/BIND_PORT)"
port="$(trim ${port})"
env/bin/gunicorn --bind 127.0.0.1:${port} --workers 2 --log-level error --access-logfile ./log/gunicorn.access.log --error-logfile ./log/gunicorn.error.log wsgi:app

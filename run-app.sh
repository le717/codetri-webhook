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

# export SYS_VARS_PATH="./secrets"
# export FLASK_ENV="development"

port="$(< ./secrets/BIND_PORT)"
port="$(trim ${port})"

echo $SYS_VARS_PATH
echo $FLASK_ENV

venv/bin/gunicorn --bind 127.0.0.1:${port} --workers 2 --log-level error --access-logfile ./log/access.log --error-logfile ./log/error.log wsgi:app

# sudo lsof -i :6000
# ps -ef | grep supervisord
# ps -ef | grep gunicorn

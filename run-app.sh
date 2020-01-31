#!/usr/bin/env bash
gunicorn --bind 127.0.0.1:5006 --workers 2 wsgi:app

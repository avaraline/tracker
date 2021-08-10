#!/bin/sh

set -e

python /app/manage.py migrate
python /app/manage.py bootstrap

exec "$@"

#!/bin/bash
set -e

python manage.py migrate --noinput &&
python manage.py collectstatic --noinput &&
uwsgi --ini /home/docker/eesti_ldap/uwsgi.ini

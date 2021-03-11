#!/bin/bash
set -e

python manage.py migrate --noinput &&
python manage.py loaddata eesti_ldap/fixtures/auth_user.json &&
python manage.py runserver 0.0.0.0:8000

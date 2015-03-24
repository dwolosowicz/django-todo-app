#!/bin/bash

#
# The installation script assumes a few things:
# - the web server responsible for serving the app is properly configured for TODOApp
# - the environment is python ready (means, python, pip and virtualenv are avaiable in PATH variable)
# - the code repository has been successfully cloned into specific directory from which this script will run
#

ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@example.com"

echo "[#1] Creating Virtual Environment"
virtualenv env

source env/bin/activate
echo "[#2] Virtual Environment created and activated"

echo "[#3] Installing dependencies..."
pip install -r requirements.txt

echo "[#4] Executing migrations, collecting static files"
python project/manage.py migrate
python project/manage.py collectstatic --noinput

echo "[#5] Creating superuser with default username: $ADMIN_USERNAME and email: $ADMIN_EMAIL"
python project/manage.py createsuperuser --username=$ADMIN_USERNAME --email=$ADMIN_EMAIL

#!/bin/bash

#
# The installation script assumes a few things:
# - the web server responsible for serving the app is properly configured for TODOApp
# - the environment is python ready (means, python, pip and virtualenv are avaiable in PATH variable)
# - the code repository has been successfully cloned into specific directory from which this script will run
#

COLOR_LIGHTGREEN="\033[0;32m"
COLOR_NONE="\033[0;0m"

ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@example.com"

echo "$COLOR_LIGHTGREEN[#1] Creating Virtual Environment"
echo $COLOR_NONE$
virtualenv env

source env/bin/activate
echo "$COLOR_LIGHTGREEN[#2] Virtual Environment created and activated"
echo $COLOR_NONE$

echo "$COLOR_LIGHTGREEN[#3] Installing dependencies..."
echo $COLOR_NONE
pip install -r requirements.txt

echo "$COLOR_LIGHTGREEN[#4] Executing migrations, collecting static files"
echo $COLOR_NONE
python project/manage.py migrate
python project/manage.py collectstatic --noinput

echo "$COLOR_LIGHGREEN[#5] Creating superuser with default username: $ADMIN_USERNAME and email: $ADMIN_EMAIL"
echo $COLOR_NONE
python project/manage.py createsuperuser --username=$ADMIN_USERNAME --email=$ADMIN_EMAIL

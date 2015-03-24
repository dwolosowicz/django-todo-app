#!/bin/bash

#
# The installation script assumes a few things:
# - the web server responsible for serving the app is properly configured for TODOApp
# - the environment is python ready (means, python, pip and virtualenv are avaiable in PATH variable)
# - the code repository has been successfully cloned into specific directory from which this script will run
#

virtualenv env
source env/bin/activate
pip install -r requirements.txt
python project/manage.py migrate
python project/manage.py collectstatic --noinput

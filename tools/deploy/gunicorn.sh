#!/bin/bash

set -e
test -d $LOGDIR || mkdir -p $LOGDIR

cd /var/chemistry/code
. VENV/bin/activate

gunicorn wsgi:application -c appserver_config.py 

#!/bin/bash

set -e
LOGFILE=/var/chemistry/log/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=4
SOCK_FILE=/tmp/chemistry_appserver.sock

# user/group to run as
USER=est863
GROUP=est863
test -d $LOGDIR || mkdir -p $LOGDIR

cd /var/chemistry/code
. VENV/bin/activate

gunicorn wsgi:application -w $NUM_WORKERS \
    --bind=unix:$SOCK_FILE \
    --worker-class=sync \
    --worker-connection=1000 \
    --timeout=30 \
    --graceful-timeout=30 \
    --name=chemistry-appserver \
    --user=$USER --group=$GROUP \
    --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE \
    

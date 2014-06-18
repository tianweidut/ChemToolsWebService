#!/bin/bash
set -e

ROOT=/var/chemistry
CODE_DIR=$ROOT/code
LOG_DIR=$ROOT/log
TMP_DIR=$ROOT/tmp


echo '--------ensure dirs----------------'
sudo test -d $ROOT || mkdir -p $ROOT 
sudo chown est863 $ROOT
sudo chgrp est863 $ROOT
test -d $CODE_DIR || mkdir -p $CODE_DIR
test -d $LOG_DIR || mkdir -p $LOG_DIR
test -d $TMP_DIR || mkdir -p $TMP_DIR

echo 'Please copy chemistry code into:', $CODE_DIR

echo '-------install other softwares(no include calcore softwares)'
sudo apt-get install python-openbabel -y
sudo apt-get install openbabel -y
sudo apt-get install ia32-libs -y

echo '--------build virtual env environment----------'
sudo apt-get install python-virtualenv -y
cd $CODE_DIR
virtualenv --system-site-packages VENV
. VENV/bin/activate
pip install -r requirements.txt

echo '--------initialize database---------------'
cd $CODE_DIR
sh tools/build_env.sh setup_database

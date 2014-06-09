#!/bin/bash

set -e

if [[ $1 == 'dev' ]]; then
    setup_dev_env
elif [[ $1 == 'production' ]]; then 
    setup_production_env


function build_virtualenv()
{
    virtualenv venv --system-site-packages
    source venv/bin/activate
}

function init_database()
{
    echo '------init database-------------'
    cd tools/data/
    tar -zxvf init_data_for_dev.sql.tar.gz init_data_for_dev.sql
    mysql -ueye -psauron "create database Chemistry CHARACTER SET utf8;" 
    mysql -ueye -psauron Chemistry < init_data_for_dev.sql
    rm -rf init_data_for_dev.sql
    cd -
}

function install_deps_for_calculate()
{
    echo '------install deps for calculate----------'
    sudo apt-get install python-openbabel bkchem -y
    sudo apt-get install python-tk idle python-pmw python-imaging -y
}

function setup_dev_env() 
{
    build_virtualenv

    echo "-------install deps-------------"
    pip install --allow-unverified pyPdf pyPdf
    pip install -r requirements.txt

    init_database
}

function setup_production_env() 
{
    echo '--'
}

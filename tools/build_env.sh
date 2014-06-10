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


function setup_dragon6()
{
    sudo cp -r ~/dragon6 /usr/share/
    ifconfig eth0 down
    ifconfig eth0 hw ether 00:E0:81:C9:29:18
    ifconfig eth0 up``
    sudo ln -s /usr/share/dragon6/dragon6shell /usr/bin/dragon6shell
    sudo cp /usr/share/dragon6/drg6_LI_XUEHUA_academic.txt /usr/share/dragon6/drg_license.txt
    dragon6shell -l
}

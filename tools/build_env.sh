#!/bin/bash

set -e

if [[ $1 == 'dev' ]]; then
    setup_dev_env
elif [[ $1 == 'production' ]]; then 
    setup_production_env
elif [[ $1 == 'setup_database' ]]; then 
    init_database 


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

function dump_database()
{
    echo '------dump database-------------'
    cd tools/data/
    mysqldump -ueye -psauron Chemistry > init_data_for_dev.sql
    tar -zcvf init_data_for_dev.sql.tar.gz init_data_for_dev.sql
    rm -rf init_data_for_dev.sql
    cd -
}

function install_deps_for_calculate()
{
    echo '------install deps for calculate----------'
    sudo apt-get install python-openbabel bkchem -y
    sudo apt-get install python-tk idle python-pmw python-imaging -y
    sudo apt-get install ia32-libs-gtk ia32-libs -y
    sudo apt-get install ia32-libs-multiarch -y
    sudo apt-get install libc6:i386 libgcc1:i386 gcc-4.6-base:i386 libstdc++5:i386 libstdc++6:i386 -y
    sudo apt-get install apt-file -y
    sudo apt-get install build-essential libc6-dev-i386 gfortran csh -y
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

function setup_gaussian()
{
   echo "需要注意的是，每台机器需要重新解压g09.tar.bz2，重新install，并且保证csh已经安装"
   bzip2 -d g09.tar.bz2
   tar -xvf g09.tar
   mkdir g09/scratch

   echo "in ~/.zshrc or ~/.bashrc"
   echo "g09root=/home/vagrant/tianwei/calcore_software/Gaussian"
   echo "GAUSS_SCRDIR=/home/vagrant/tianwei/calcore_software/Gaussian/g09/scratch"
   echo "export g09root GAUSS_SCRDIR"
   echo "source $g09root/g09/bsd/g09.profile"

   source ~/.zshrc
   . g09/bsd/install
   echo "test--"
   echo "g09 g09/tests/com/test001.com"
   echo "cat g09/tests/com/test001.log"
}

function setup_mopac()
{
    echo "下载最新的mopac软件，拷贝原来的密码文件"
    wget http://openmopac.net/MOPAC2012_for_Linux_64_bit.zip
    unzip MOPAC2012_for_Linux_64_bit.zip
    mv password_for_mopac2012 MOPAC2012_for_Linux_64_bit/
    echo "in ~/.zshrc or ~/.bashrc"
    echo 'export MOPAC_LICENSE=/home/vagrant/tianwei/calcore_software/mopac'
    echo 'alias mopac="/home/vagrant/tianwei/calcore_software/mopac/MOPAC2012.exe"'
    source ~/.zshrc
    echo "test--"
    echo "mopac Example\ data\ set.mop"
}

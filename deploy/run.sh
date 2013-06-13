#!/bin/bash

loadini_func(){
    echo "load all ini files"
    dir="/etc/uwsgi/apps-available"
    filelist=`ls $dir/*.ini`
    for filename in $filelist;do
        echo $filename
        sudo uwsgi --ini $filename
    done
    echo "Finish the uwsgi operation!"
}

restart_server(){
    sudo killall -9 uwsgi 
    sudo killall -9 nginx 
    loadini_func 
    sudo /etc/init.d/nginx restart
    echo "*_* Restart uwsgi and nginx [OK] *_* "
}

update_worker_core(){
    ssh $1
    cd ~/mysites/ChemToolService/
    git checkout production
    git pull origin production
    echo "finish this worker"$1
    exit
}

update_worker(){
    task1 = "task1@task1"
    task2 = "task2@task2"
    task3 = "task3@task3"

    update_worker_core task1
    update_worker_core task2
    update_worker_core task3
}

#start scripts for provincemanagement
echo "************************************"
echo "welcome to use server deploy scripts"
echo "For Chemistry Tool Service website version"
echo "************************************"

if [ $1 = 'start' ];then
    echo "prepare for start uwsgi"
    psid=$(ps aux|grep "uwsgi"|grep -v "grep"|wc -l)
    echo "[debug]current process is":$psid
    if [ "$psid" -gt "2" ];then
        echo "uwsgi is running now!"
    else
        echo "execute uwsgi command..."
        loadini_func 
    fi

    psid=$(ps aux|grep "nginx"|grep -v "grep"|wc -l)
    if [ "$psid" -gt "1" ];then
        echo "nginx is runnging now!"
    else
        echo "execute nginx command..."
        sudo /etc/init.d/nginx start
    fi

    echo "*_* Start uwsgi service[OK] *_* "

elif [ $1 = 'stop' ];then
    sudo killall -9 uwsgi
    sudo killall -9 nginx
    echo "*_* Stop uwsgi and nginx [OK] *_* "

elif [ $1 = 'restart' ];then
    restart_server

elif [ $1 = 'deploy' ];then
    sudo cp chemistry_server /etc/nginx/sites-available/chemistry_server
    sudo ln -s /etc/nginx/sites-available/chemistry_server /etc/nginx/sites-enabled/chemistry_server
    sudo cp chemistry.ini /etc/uwsgi/apps-available/
    sudo chmod 777 /var/run/nginx.pid
    echo "*_* Deploy and copy scipts *_*"

elif [ $1 = 'update' ];then
    echo "update production source code and update static files"
    cd $(cd "$(dirname "$0")"; pwd)/../
    echo "check branch to production"
    git checkout production
    echo "update code repo"
    git pull origin production
    echo "update static folder"
    python manage.py collectstatic
    cd -
    echo "*_* update codebase *_*"
    echo "update worker"
    update_worker

else
    echo "Usages: sh run.sh [start|restart|stop|deploy|update]"
fi

echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

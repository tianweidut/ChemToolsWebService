# Introduction:

 * Chemistry Service
 * Web: Bootstrap + Django + Piston
 * Client: WPF
 * Calculate Service: some specific software, dragon, mopac etc.

# Requirements:
 * please run '''sudo pip install -r requirements.txt'''

# Server Host:
 * Inorder to adapt different computers and different network environment,
 we will use hosts trick.
 * You should add some host name in /etc/hosts.
   * developmentServer -> mysql server for development environment
   * redisDevelopmentServer -> redis server and message queue broker for development environment
   * productionServer -> mysql server for production environment
   * redisProductionServer -> redis server for production environment
   * sentryServer -> sentry monitoring server in production environment

# Installation:
 * web tools:
  * sudo pip install -r requirements.txt
 
 * Mysql:
  * create database Chemistry CHARACTER SET utf8;
  * python manage.py syncdb

 * Calculated software
  * sudo apt-get install python-openbabel -y
  * some other software should be installed manually
  * sudo apt-get install ia32-libs -y  #32-bit lib for 64-bit machine

 * Cache
  * Now, our website is very small, so we use database cache for cache,
  later we may use memcache.
  * please run: python manage.py createcachetable cachedatabasetable


 * python manage.py runserver IP:PORT
 * go web browser, visit: IP:PORT

# License
 GPLv3, see LICENSE file
 test

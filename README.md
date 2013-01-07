# Introduction:

 * Chemistry Service
 * Web: Bootstrap + Django + Piston
 * Client: WPF
 * Calculate Service: some specific software, dragon, mopac etc.

# Requirements:
 * web tools:
  * sudo pip install python-django    # Django
  * sudo pip install lbforum          # Lbforum(论坛)
  * sudo pip install django-debug-toolbar   # debug tools
  * sudo apt-get install python-piston -y   # Piston, a RESTFul API 
 
 * Mysql:
  * create database Chemistry CHARACTER SET utf8;
  * python manage.py syncdb
  * python manage.py migrate
  * python manage.py syncdb

 * Calculated software
  * sudo apt-get install python-openbabel -y
  * some other software should be installed manually
  * sudo apt-get install ia32-libs -y  #32-bit lib for 64-bit machine

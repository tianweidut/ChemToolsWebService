# Introduction:

 * Chemistry Service
 * Web: Bootstrap + Django + Piston
 * Client: WPF
 * Calculate Service: some specific software, dragon, mopac etc.

# Requirements:
 * web tools:
  * sudo pip install python-django    # Django > 1.4, maybe you should download it by yourself.
  * sudo pip install lbforum          # Lbforum(论坛)
  * sudo pip install django-debug-toolbar   # debug tools
  * hg clone https://bitbucket.org/jespern/django-piston   # Piston, a RESTFul API 
     * sudo python django-piston/setup.py build
     * sudo python django-piston/setup.py install
 
 * Mysql:
  * create database Chemistry CHARACTER SET utf8;
  * python manage.py syncdb
  * python manage.py migrate
  * python manage.py syncdb

 * Calculated software
  * sudo apt-get install python-openbabel -y
  * some other software should be installed manually
  * sudo apt-get install ia32-libs -y  #32-bit lib for 64-bit machine

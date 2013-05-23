# Introduction:

 * Chemistry Service
 * Web: Bootstrap + Django + Piston
 * Client: WPF
 * Calculate Service: some specific software, dragon, mopac etc.

# Requirements:
 * Django 1.4 +
 * lbforum 
 * django-debug-toolbar
 * django-tinymce


# Installation:
 * web tools:
  * sudo pip install -r requirements.txt
  * hg clone https://bitbucket.org/jespern/django-piston   # Piston, a RESTFul API 
     * sudo python django-piston/setup.py build
     * sudo python django-piston/setup.py install
 
 * Mysql:
  * create database Chemistry CHARACTER SET utf8;
  * python manage.py syncdb

 * Calculated software
  * sudo apt-get install python-openbabel -y
  * some other software should be installed manually
  * sudo apt-get install ia32-libs -y  #32-bit lib for 64-bit machine


 * python manage.py runserver IP:PORT
 * go web browser, visit: IP:PORT

# License
 GPLv3, see LICENSE file
 test

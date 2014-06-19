#coding: utf-8

bind = 'unix:/tmp/chemistry_appserver.sock'
workers = 6
worker_class = 'sync'


timeout = 90
graceful_timeout = 20
keepalive = 2

debug = False

worker_connections = 1000
user = 'est863'
group = 'est863'

proc_name = 'chemistry-appserver'

loglevel = 'debug'
logfile = '/var/chemistry/log/gunicorn.log'
accesslog = '-'

"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: Django setting for daily development
    Created: 2013-4-12
"""
from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'Chemistry',             # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'root',                   # Not used with sqlite3.
        'HOST': 'developmentServer',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}


BROKER_URL = "redis://:root@redisDevelopmentServer:6379/0"
BROKER_BACKEND = "redis"

REDIS_HOST = "redisDevelopmentServer"
REDIS_PORT = 6379
REDIS_DB = 0
REDIT_PASSWORD = ""
REDIS_CONNECT_RETRY = True

CELERY_SEND_EVENTS = True
CELERY_CONNECT_RETRY = True
CELERY_RESULT_BACKEND = 'redis://:root@redisDevelopmentServer:6379/0'
CELERY_RESULT_PORT = 6379
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

#celery task queue
import djcelery
djcelery.setup_loader()

"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: Django setting for daily development
    Created: 2013-4-12
"""

from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PRODUCTION_FLAG = "Technical Preview!" 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'Chemistry',             # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'root',                   # Not used with sqlite3.
        'HOST': 'production-server',          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}

# Set your DSN value
RAVEN_CONFIG = {
        'dsn':'http://a98c9c1f6b9740e1b424a073e610751e:7e006e2a5787459f8aff0fd8ebb91652@202.118.73.59:19000/2',
    }

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
        )
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    )

#celery task queue
BROKER_URL = "redis://:root@redis-dev-server:6379/0"
BROKER_BACKEND = "redis"

REDIS_HOST = "redis-dev-server"
REDIS_PORT = 6379
REDIS_DB = 0
REDIT_PASSWORD = ""
REDIS_CONNECT_RETRY = True

CELERY_SEND_EVENTS = True
CELERY_CONNECT_RETRY = True
CELERY_RESULT_BACKEND = 'redis://:root@redis-dev-server:6379/0'
CELERY_RESULT_PORT = 6379
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

import djcelery
djcelery.setup_loader()

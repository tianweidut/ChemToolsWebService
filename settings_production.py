#coding: utf-8
from settings import *

TEMPLATE_DEBUG = DEBUG = False

PRODUCTION_FLAG = "预览版"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Chemistry',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

#celery task queue
BROKER_URL = "redis://redis-production-server:6379/0"
BROKER_BACKEND = "redis"
BROKER_PORT = 6379

REDIS_DB = 0
REDIS_CONNECT_RETRY = True

CELERY_REDIS_PORT = 6379
CELERY_RESULT_BACKEND = 'redis'
CELERY_RESULT_PORT = 6379
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


import djcelery
djcelery.setup_loader()

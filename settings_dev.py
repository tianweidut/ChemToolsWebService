# coding: utf-8
from settings import *

TEMPLATE_DEBUG = DEBUG = True

PRODUCTION_FLAG = "开发版!"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Chemistry',
        'USER': 'eye',
        'PASSWORD': 'sauron',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


BROKER_URL = "redis://127.0.0.1:6379/0"
BROKER_BACKEND = "redis"
BROKER_PORT = 6379

REDIS_DB = 0
REDIS_CONNECT_RETRY = True

CELERY_REDIS_PORT = 6379
CELERY_RESULT_BACKEND = 'redis'
CELERY_RESULT_PORT = 6379
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# celery task queue
import djcelery
djcelery.setup_loader()

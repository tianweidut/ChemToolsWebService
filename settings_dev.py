#coding: utf-8
from settings import *

TEMPLATE_DEBUG = DEBUG = True

PRODUCTION_FLAG = "开发版!"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Chemistry',
        'USER': 'eye',
        'PASSWORD': 'sauron',
        'HOST': 'dev-server',
        'PORT': '3306',
    }
}


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
CELERYD_HIJACK_ROOT_LOGGER = False

#celery task queue
import djcelery
djcelery.setup_loader()

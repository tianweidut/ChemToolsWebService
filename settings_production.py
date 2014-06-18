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

# Set your DSN value
SENTRY_AUTO_LOG_STACKS = True
RAVEN_CONFIG = {
    'dsn': 'http://a98c9c1f6b9740e1b424a073e610751e:7e006e2a5787459f8aff0fd8ebb91652@202.118.73.59:19000/2',
    }

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat')

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    )

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

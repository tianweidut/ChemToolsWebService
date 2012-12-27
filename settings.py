# Django settings for Rest project.

import os
import sys
import logging
from os.path import join

SETTINGS_ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'Chemistry',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(SETTINGS_ROOT,'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    MEDIA_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '((8!_-pdeoo5ewkh#hm2(f^0y=ncx2)$^=#t+a$k2^&amp;7dqunc='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
    #LbForum
    'pagination.middleware.PaginationMiddleware',
    'onlineuser.middleware.OnlineUserMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(SETTINGS_ROOT,'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'context.application_settings',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    
    "djangohelper.context_processors.ctx_config",

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #Project
    'gui',
    'api',
    'registration',
    'users',
    'calcore',
    #Add-on
    'debug_toolbar',
    'tinymce',
    #LBForum
    'pagination',
    'south',
    'lbforum',
    'simpleavatar',
    'djangohelper',
    'onlineuser',
    'attachments',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOG_FILENAME = 'askbot.log'

logging.basicConfig( filename=os.path.join(os.path.dirname(__file__), 'log', LOG_FILENAME),
                   level=logging.CRITICAL,
                   format='%(pathname)s TIME: %(asctime)s MSG:%(filename)s:%(funcName)s:%(lineno)d %(message)s',
                   )

#Add support  to user profile
AUTH_PROFILE_MODULE = 'users.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 30
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST = 'mail'
EMAIL_HOST_USER = 'liutianweidlut@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'gmailusername@gmail.com'
#EMAIL_HOST_PASSWORD = 'xxxxxxx'
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'liutianweidlut@gmail.com'
SERVER_EMAIL = 'liutianweidlut@gmail.com'

#########################
# File Transfer settings
PREPARE_UPLOAD_BACKEND = 'filetransfers.backends.delegate.prepare_upload'
#PRIVATE_PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
#PUBLIC_PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
#SERVE_FILE_BACKEND = 'djangoappengine.storage.serve_file'
PUBLIC_DOWNLOAD_URL_BACKEND = 'filetransfers.backends.base_url.public_download_url'
PUBLIC_DOWNLOADS_URL_BASE = '/data/'

TMP_FILE_PATH = join(SETTINGS_ROOT,'tmp/')

#APPEND_SLASH=False

#Debug 
INTERNAL_IPS = ('127.0.0.1', '192.168.2.64','192.168.2.7','localhost',) 

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

LOGGING_OUTPUT_ENABLED = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

#LBforum Settings
AUTO_GENERATE_AVATAR_SIZES = (80, 48, )

ROOT_URL = '/'
LOGIN_REDIRECT_URL = ROOT_URL
LOGIN_URL = "%saccounts/login/" % ROOT_URL
LOGOUT_URL = "%saccounts/logout/" % ROOT_URL
REGISTER_URL = '%saccounts/register/' % ROOT_URL#registration_register
CHANGE_PSWD_URL = '%saccounts/password/change/' % ROOT_URL#registration_register

CTX_CONFIG = {
        'LBFORUM_TITLE': 'Chemistry Tools Forum',
        'LBFORUM_SUB_TITLE': 'A forum for Chemistry Tools, enjoy...',
        'FORUM_PAGE_SIZE': 50,
        'TOPIC_PAGE_SIZE': 20,

        #URLS....
        'LOGIN_URL': LOGIN_URL,
        'LOGOUT_URL': LOGOUT_URL,
        'REGISTER_URL': REGISTER_URL,
        'CHANGE_PSWD_URL': CHANGE_PSWD_URL,
        }

BBCODE_AUTO_URLS = True

#HTML safe filter
HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []
"""
#default html safe settings 
acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
      'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
      'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
      'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 
      'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol', 
      'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
      'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
      'thead', 'tr', 'tt', 'u', 'ul', 'var']

acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
  'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
  'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
  'colspan', 'color', 'compact', 'coords', 'datetime', 'dir', 
  'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
  'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
  'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 
  'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
  'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
  'usemap', 'valign', 'value', 'vspace', 'width', 'style']
"""

"""
Base Skin Settings
"""
USE_LOCAL_FONTS = True

"""
FILE Upload
"""
FILE_UPLOAD_TEMP_DIR  = os.path.join(os.path.dirname(__file__),"tmp").replace("\\",'/')
FILE_UPLOAD_HANDLERS = (
            'django.core.files.uploadhandler.MemoryFileUploadHandler',
            'django.core.files.uploadhandler.TemporaryFileUploadHandler',
                )

ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png','.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

"""
TINY MCE Editor
"""
TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, 'js/tinymce/')

TINYMCE_URL = MEDIA_URL + 'js/tinymce/'
TINYMCE_DEFAULT_CONFIG = {
            'plugins': 'askbot_imageuploader,askbot_attachment',
            'convert_urls': False,
            'theme': 'advanced',
            'force_br_newlines': True,
            'force_p_newlines': False,
            'forced_root_block': '',
            'mode': 'textareas',
            'oninit': "function(){ tinyMCE.activeEditor.setContent(askbot['data']['editorContent'] || ''); }",
            'theme_advanced_toolbar_location': 'top',
            'theme_advanced_toolbar_align': 'left',
            'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
            'theme_advanced_buttons2': '',
            'theme_advanced_buttons3': '',
            'theme_advanced_path': False,
            'theme_advanced_resizing': True,
            'theme_advanced_resize_horizontal': False,
            'theme_advanced_statusbar_location': 'bottom',
            'height': '250'
}

"""
Other settings from askbot
"""
MAX_COMMENT_LENGTH  = 300
EDITOR_TYPE = "tinymce"

MAX_TAG_LENGTH = 20
MIN_TITLE_LENGTH = 10
TAGS_ARE_REQUIRED = False
ENABLE_TAG_MODERATION = False
MAX_TAGS_PER_POST = 5

SHOW_LOGO = True

USE_LICENSE = True
LICENSE_USE_URL = True
LICENSE_USE_LOGO = True
LICENSE_ACRONYM = 'cc-by-sa'
LICENSE_TITLE = 'Creative Commons Attribution Share Alike 3.0'
LICENSE_URL = 'http://creativecommons.org/licenses/by-sa/3.0/legalcode'
LICENSE_LOGO_URL = 'images/cc-by-sa.png'

APP_COPYRIGHT = 'Copyright Chemistry Tools, 2012-2013.'

LOGOUT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SITE_LOGO_URL = "images/logo.gif"

APP_TITLE = "Chemistry Tools"

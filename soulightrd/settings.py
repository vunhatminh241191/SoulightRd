"""Common settings and globals."""
import os

from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from os import environ
from sys import path

from django.utils.translation import ugettext_lazy as _

from djcelery import setup_loader

ROOT_PATH = os.path.dirname(__file__)
path.append(ROOT_PATH)

SITE_NAME = os.path.basename(ROOT_PATH)
SITE_DOMAIN = SITE_NAME + ".com"


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Dang Nguyen', 'dangnguyen_1712@yahoo.com'),
)

ADMINS_USERNAME = (
    "dtn29",
    "dtn1712",
)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

MANDRILL_API_KEY = environ.get("MANDRILL_API_KEY") 
SERVER_EMAIL=environ.get('SERVER_EMAIL')

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587
EMAIL_USE_TLS = True

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Los_Angeles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(ROOT_PATH, 'assets/media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = 'staticfiles'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'assets/static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "chbrc3p7q%g9e80a(&bm$ci6ygdc_ak99q6ep90!#evq7yc@@@"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    os.path.join(ROOT_PATH, 'fixtures'),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django_mobile.context_processors.flavour',
    'allauth.account.context_processors.account',
    "allauth.socialaccount.context_processors.socialaccount",
    "soulightrd.apps.main.context_processors.site_data",
    "soulightrd.apps.main.context_processors.global_data",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    "django_mobile.loader.Loader",
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'assets/templates'),
    os.path.join(ROOT_PATH, 'assets/templates/sites'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/non_responsive'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/non_responsive/apps'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/non_responsive/apps/auth'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/responsive'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/responsive/apps'),
    os.path.join(ROOT_PATH, 'assets/templates/sites/responsive/apps/auth'),
)
########## END TEMPLATE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    
    # Database migration helpers:
    'south',

    # Static file management:
    'compressor',

    # Asynchronous task queue:
    'djcelery',

    # Search
    "haystack",
    
    # Others
    "dajaxice",
    'django_mobile',
    "cities_light",
    "djmoney",
    'profiler',
    "djrill",
    'sorl.thumbnail'
)

LOCAL_APPS = (
    "soulightrd.apps.about",
    "soulightrd.apps.auth",
    "soulightrd.apps.discover",
    "soulightrd.apps.mailer",
    "soulightrd.apps.main",
    "soulightrd.apps.member",
    "soulightrd.apps.message",
    "soulightrd.apps.notification",
    "soulightrd.apps.organization",
    "soulightrd.apps.payment",
    "soulightrd.apps.project",
    "soulightrd.apps.search",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile_soulightrd': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "logs/soulightrd.log"),
        }, 
        'logfile_dajaxice': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "logs/dajaxice.log"),
        }, 
        'logfile_facebook': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "logs/django_facebook.log"),
        },

    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'dajaxice': {
            'handlers': ['logfile_dajaxice'],
            'level': 'ERROR',
        },
        'django_facebook':{
            'handlers': ['logfile_facebook'],
            'level': 'DEBUG',
        },
        'soulightrd': {
            'handlers': ['logfile_soulightrd'],
            'level': 'ERROR',
        },
    }, 
}


########## CELERY CONFIGURATION
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://docs.celeryproject.org/en/master/configuration.html#std:setting-CELERY_CHORD_PROPAGATES
CELERY_CHORD_PROPAGATES = True

# See: http://celery.github.com/celery/django/
setup_loader()
########## END CELERY CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# See: http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_HASHING_METHOD
COMPRESS_CSS_HASHING_METHOD = 'content'

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]
########## END COMPRESSION CONFIGURATION



AUTH_PROFILE_MODULE = 'main.UserProfile'

SERIALIZATION_MODULES = {
    'json': "django.core.serializers.json",
}

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend', 
)

ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 4
ACCOUNT_EMAIL_VERIFICATION = "optional"

#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
#HAYSTACK_DEFAULT_OPERATOR = 'OR'

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/?action=confirm_email&result=success"

ACCOUNT_USERNAME_BLACKLIST = [
    'admin','signup','login','password',"accounts"
    'logout','confirm_email','search','settings',
    'buzz','messages',"about",'api','asset','photo',
    'feeds','friends'
]

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[SoulightRd]"
ACCOUNT_ADAPTER = "soulightrd.apps.auth.adapters.CustomAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream',"user_about_me","user_birthday","user_location","user_events","user_friends","read_friendlists"],
        'METHOD': 'js_sdk',
        'VERIFIED_EMAIL': False
    }
}


GEOIP_PATH = os.path.join(ROOT_PATH, "db/geolocation")  ### path for geoip dat

GEOIP_DATABASE = os.path.join(ROOT_PATH, "db/geolocation/GeoLiteCity.dat")

CITIES_FILES = {
    'city': {
       'filename': 'cities1000.zip',
       'urls':     ['http://download.geonames.org/export/dump/'+'{filename}']
    },
}

SOCIALACCOUNT_ADAPTER = "soulightrd.apps.auth.adapters.CustomSocialAccountAdapter"

SOCIAL_FRIENDS_USING_ALLAUTH = True

MAX_MANDRILL_EMAIL_ALLOW = 12000

OW_LY_API_KEY = "6sv891CJpDcuiz8eyRHfy"

FACEBOOK_PROVIDER = "facebook"
FACEBOOK_APP_NAME = "SoulightRd Facebook App"



STAGE = "dev"

DEBUG = True

TEMPLATE_DEBUG = DEBUG

WEBSITE_HOMEPAGE = "http://localhost:8000/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_PATH, 'db/dev/soulightrd.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = True

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
########## END CELERY CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(ROOT_PATH, 'db/dev/whoosh_index'),
        'INCLUDE_SPELLING': False,
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
########## END TOOLBAR CONFIGURATION

STATIC_URL = '/static/'


MIDDLEWARE_CLASSES = (
    # Use GZip compression to reduce bandwidth.
    'django.middleware.gzip.GZipMiddleware',

    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "profiler.middleware.ProfileMiddleware",
    
)

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

FACEBOOK_APP_ID = '1449654595310684'
FACEBOOK_APP_SECRET = 'b78767a5b624cb510f0f1996be62d24b'



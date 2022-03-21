"""
Django settings for auth project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from dj_database_url import parse as db_url
from decouple import config
import os
import datetime

from django.core.management.utils import get_random_secret_key


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=1, cast=bool)
# DEBUG = False

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom
    'api',
    'users.apps.UsersConfig',
    'authnotifications',


    # rest
    'rest_framework_jwt',
    'rest_framework_jwt.blacklist',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_results',

    # extra
    'corsheaders',
    'django_extensions',
    'django.contrib.sites',

]

APPEND_SLASH=True

X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # extra
]

CSRF_COOKIE_NAME = config("ENV", default="dev")+'-csrftoken'

ROOT_URLCONF = 'auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'dashboard/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI_APPLICATION = 'auth.wsgi.application'


ASGI_APPLICATION = 'auth.asgi.application'


AUTH_USER_MODEL = 'users.User'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if os.environ.get("AUTH_DATABASE_URL"):
    
    import dj_database_url
    DB_URL = os.environ.get("AUTH_DATABASE_URL")
    
    DATABASES = {}

    DATABASES['default'] = dj_database_url.config(default=DB_URL, conn_max_age=600, ssl_require=False)
    
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get("REDIS_URL", default="redis://localhost:6379")],
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Dar_es_Salaam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files

MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_URL = "/media/"

# drf
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}


# JWT settings
JWT_EXPIRATION_DELTA_DEFAULT = 2.628e+6  # 1 month in seconds
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(
        seconds=config(
            'DJANGO_JWT_EXPIRATION_DELTA',
            default=JWT_EXPIRATION_DELTA_DEFAULT,
            cast=int
        )
    ),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_GET_USER_SECRET_KEY': lambda user: user.secret_key,
    'JWT_ENCODE_HANDLER':'utils.selectors.jwt_encode_payload',
    'JWT_DECODE_HANDLER':'utils.selectors.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.selectors.jwt_response_payload_handler',
    'JWT_AUTH_COOKIE': 'jwt_token',
    'JWT_AUTH_COOKIE_SAMESITE': 'None'
}

# Login settings

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


# CELERY
# Celery Configuration Options
CELERY_BROKER_URL = "redis://localhost:6379//"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Africa/Dar_es_Salaam'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT=["json"]
CELERY_TASK_SERIALIZER='json'


# TWILIO settings

TWILIO = {
    'TWILIO_ACCOUNT_SID': config('TWILIO_ACCOUNT_SID'),
    'TWILIO_AUTH_TOKEN': config('TWILIO_AUTH_TOKEN'),
    'SERVICE_ID': config('SERVICE_ID')
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True


# dynamic emailing
EMAIL_BACKEND = 'utils.email_backend.ConfiguredEmailBackend'

# verification email
EMAIL_TOKEN_LIFE = 60 * 60
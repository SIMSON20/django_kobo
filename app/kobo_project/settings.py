"""
Django settings for kobo_project project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from decouple import config
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = [config('SERVER_URL'), config('SERVER_IP')]


# Application definition

INSTALLED_APPS = [
    'kobo.apps.KoboConfig',
    'bns.apps.BnsConfig',
    'nrgt.apps.NRGTConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'import_export',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'social_django',
    'custom_auth.apps.CustomAuthConfig',
    'tags.apps.TagConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #'bns.middleware.AuthRequiredMiddleware',
]

ROOT_URLCONF = 'kobo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'kobo_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL'),
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': config('LOG_LEVEL'),
            'propagate': True,
        },
    },
}
        # Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'custom_auth.portal.PortalOAuth2',
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)

# Set the default language for your site.
LANGUAGE_CODE = 'en'


# Tell Django where the project's translation files should be.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

FORCE_SCRIPT_NAME='/' + config('URI_PREFIX')

STATIC_ROOT = "/home/docker/code/app/static/"
STATIC_URL = ('/' + config('URI_PREFIX') + '/static/').replace('//', '/')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so' #os.environ["GDAL_LIBRARY_PATH"]

LOGIN_URL = ('/' + config('URI_PREFIX') + '/oauth/login/portal').replace('//', '/')
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/' + config('URI_PREFIX')

IMPORT_EXPORT_USE_TRANSACTIONS = True

#Social Login settings
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PORTAL_KEY = config('PORTAL_KEY')
SOCIAL_AUTH_PORTAL_SECRET = config('PORTAL_SECRET')
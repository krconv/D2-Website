"""
Django settings for D2 Webiste project.
"""

import os
import pymysql
pymysql.install_as_MySQLdb()

WEBSITE_TITLE = "Daniels Website"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aoft5+zs(8opr_jmc%!7dpqgssoygh#iog+ue@m0t+cm7&900&'

DEBUG = False

ALLOWED_HOSTS = ['wpi.edu']

# Settings for reporting errors via email
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'd2@wpi.edu'
ADMINS = MANAGERS = (("Kodey Converse", 'krconverse@wpi.edu'))

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'submission.wpi.edu'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'd2'
EMAIL_HOST_PASSWORD = 'D2istheb0mb'
EMAIL_SUBJECT_PREFIX = "[%s]" % WEBSITE_TITLE
EMAIL_USE_TLS = True


# Application definition
INSTALLED_APPS = [
    'pages',
    'django_cas_ng',
    #'django_ajax',
    'django_cron',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'd2.middleware.IPAuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

ROOT_URLCONF = 'd2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'd2.wsgi.application'

# CAS Authentication Settings
# https://github.com/castlabs/django-cas
#CAS_SERVER_URL = 'https://cas.wpi.edu/cas/'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql.wpi.edu',
        'NAME': 'd2',
        'USER': 'd2',
        'PASSWORD': 'YXLfYu',
    }
}

# Cron Jobs
# 
CRON_CLASSES = [
    "tools.cron.UpdateDutyScheduleJob",
    "tools.cron.UpdateServerStatusJob",
]

# Minecraft Server Settings
MINECRAFT_SERVER_HOST = 'steve.dyn.wpi.edu'
MINECRAFT_SERVER_DOWNTIME_ALERT = 10

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# FastCGI Configuration from http://support.hostgator.com/articles/django-with-fastcgi
FORCE_SCRIPT_NAME = '/~d2/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = FORCE_SCRIPT_NAME + 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



"""
Common Django settings for Daniels Website.
"""
import os
import simplejson as json

# -- General Settings --
WEBSITE_TITLE = "Daniels Hall"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Secret Information
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "secrets.json"), "r") as file:
    SECRETS = json.load(file)    

SECRET_KEY = SECRETS['key']
ADMINS = MANAGERS = SECRETS['admins']

# -- Email Settings --
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str(SECRETS['email']['host'])
EMAIL_PORT = str(SECRETS['email']['port'])
EMAIL_USE_TLS = True
EMAIL_HOST_USER = SECRETS['email']['user']
EMAIL_HOST_PASSWORD = SECRETS['email']['password']
EMAIL_SUBJECT_PREFIX = "[%s] " % WEBSITE_TITLE

# Error Reporting
DEFAULT_FROM_EMAIL = SERVER_EMAIL = SECRETS['email']['server_email']


# -- Application Settings --
INSTALLED_APPS = [
    'pages',
    'django_ajax',
    'django_cron',
    'django_cas_ng',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
]

# -- Middleware Settings --
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
]

# -- Authentication Settings --
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'Daniels_Website.backends.CustomCASBackend',
]

# Password validation
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

# reCAPTCHA Settings
# https://www.google.com/recaptcha/admin
RECAPTCHA_VERIFY_URL = SECRETS['recaptcha']['url']
RECAPTCHA_SITE_KEY = SECRETS['recaptcha']['site_key']
RECAPTCHA_SECRET_KEY = SECRETS['recaptcha']['secret_key']

# -- URL Settings --
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

ROOT_URLCONF = 'Daniels_Website.urls'

# -- Static File Settings --
STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# -- Template Settings --
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

# -- CAS Authentication Settings --
CAS_SERVER_URL = 'https://cas.wpi.edu/cas/'

# -- WSGI Settings --
WSGI_APPLICATION = 'Daniels_Website.wsgi.application'

# -- Database Settings --
import pymysql
pymysql.install_as_MySQLdb()


# -- CRON Settings --
CRON_CLASSES = [
    "tools.cron.UpdateDutyScheduleJob",
    "tools.cron.UpdateServerStatusJob",
]

# -- Minecraft Settings --
MINECRAFT_SERVER_HOST = SECRETS['minecraft']['host']
MINECRAFT_SERVER_DOWNTIME_ALERT = 10

# -- Internationalization Settings --
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
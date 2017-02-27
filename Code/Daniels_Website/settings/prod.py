"""
Production Django settings for Daniels Website.
"""
from .common import *

# -- General Settings --
ALLOWED_HOSTS = ['danielshall.wpi.edu']
DEBUG = False

# -- Application Settings --

# -- Middleware Settings --
MIDDLEWARE_CLASSES.append('django_cas_ng.middleware.CASMiddleware')

# -- Authentication Settings --
AUTHENTICATION_BACKENDS.append('django_cas_ng.backends.CASBackend')

# CAS Authentication Settings
# https://github.com/castlabs/django-cas
CAS_SERVER_URL = 'https://cas.wpi.edu/cas/'

# -- Database Settings --
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': SECRETS['db']['prod']['host'],
        'NAME': SECRETS['db']['prod']['database'],
        'USER': SECRETS['db']['prod']['user'],
        'PASSWORD': SECRETS['db']['prod']['password']
    }
}
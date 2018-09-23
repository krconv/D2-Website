"""
Production Django settings for Daniels Website.
"""
from .common import *

# -- General Settings --
ALLOWED_HOSTS = ['danielshall.wpi.edu']
DEBUG = False

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
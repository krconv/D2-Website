"""
Development Django settings for Daniels Website.
"""
from .common import *

# -- General Settings --
ALLOWED_HOSTS = ['localhost', '.wpi.edu']
DEBUG = True

# -- Database Settings --
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': SECRETS['db']['dev']['host'],
        'NAME': SECRETS['db']['dev']['database'],
        'USER': SECRETS['db']['dev']['user'],
        'PASSWORD': SECRETS['db']['dev']['password']
    }
}
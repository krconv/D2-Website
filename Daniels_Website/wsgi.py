"""
WSGI config for Daniels Website.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'Daniels_Website.settings.prod'

application = get_wsgi_application()

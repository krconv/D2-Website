from django.conf import settings

from django.contrib.auth import login
from django.contrib.auth.models import User

class IPAuthenticationMiddleware(object):
    """
    Middleware to authenticate WPI users as an anonymous user using their WAN IP Address.
    """
    def process_request(self, request):
        'Checks the IP address of the user and authenticates as a WPI user if from the WPI subnet'
        if not request.user.is_authenticated():
            ip = request.META['REMOTE_ADDR']
            if (ip.startswith('130.215')): # WPI user
                user = User.objects.get(username='wpi_anonymous')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
        return
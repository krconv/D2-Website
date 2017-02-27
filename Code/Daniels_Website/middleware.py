from dns.resolver import query

from django.contrib.auth import login
from django.contrib.auth.models import User

class IPAuthenticationMiddleware(object):
    """
    Middleware to authenticate WPI users as an anonymous user using their WAN IP Address.
    """
    def process_request(self, request):
        """
        Authenticates any non-authenticated user that is on the WPI Subnet.
        """
        if not request.user.is_authenticated():
            user_ip = request.META['REMOTE_ADDR']
            subnet_prefix = str(query('wpi.edu')[0]).rsplit('.', 2)[0]
            if user_ip.startswith(subnet_prefix): # WPI user
                user = User.objects.get(username='wpi_anonymous')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
        return
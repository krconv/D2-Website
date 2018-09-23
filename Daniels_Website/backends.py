from django_cas_ng.backends import CASBackend

class CustomCASBackend(CASBackend):
    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        return user
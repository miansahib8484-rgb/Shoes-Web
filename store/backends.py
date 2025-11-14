from django.contrib.auth.backends import ModelBackend

class CanLoginBackend(ModelBackend):
    def user_can_authenticate(self, user):
        can_auth = super().user_can_authenticate(user)
        if hasattr(user, 'userprofile'):
            return can_auth and user.userprofile.can_login
        return can_auth

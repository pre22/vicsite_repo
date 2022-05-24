from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AuthenticationBackend:
    def authenticate(self, request, username, password, **kwargs):
        if kwargs.get('email', None) is not None:
            username = kwargs['email']
        if not username and password:
            return None
        try:
            user = User.objects.get_by_email_or_username(username)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
                user.save(update_fields=['last_login'])
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
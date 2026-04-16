from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """Аутентификация по email вместо username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username в данном случае — это email, который ввёл пользователь
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
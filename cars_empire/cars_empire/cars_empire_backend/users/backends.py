from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username:
            # Try email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # Try phone
                try:
                    user = User.objects.get(phone=username)
                except User.DoesNotExist:
                    return None
        if user and user.check_password(password):
            return user
        return None 
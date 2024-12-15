from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.forms import ValidationError

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username = None, password =None, **kwargs):
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            try:
                user = get_user_model().objects.get(email=username)
            except get_user_model().DoesNotExist:
                raise ValidationError({'username': 'Не знайдено користувача з таким логіном/поштою'})
        if user.check_password(password):
            return user
        raise ValidationError({'password': 'Вказано неправильний пароль'})
        
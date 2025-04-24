from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from backend.custom.functions import check_validate_password, check_validate_username


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_('Email cần được thiết lập'))
        username = check_validate_username(username)
        password = check_validate_password(password)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser phải có is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser phải có is_superuser=True'))
        return self.create_user(email, username, password, **extra_fields)
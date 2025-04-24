from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators

from backend.custom.model import BaseModel
from backend.custom.functions import upload_to
from .managers import CustomUserManager

# Create your models here.

GENDER = [
    ('1', 'Male'),
    ('2', 'Female'),
    ('3', 'Other'),
]

class User(AbstractUser, BaseModel):
    username_validator = UnicodeUsernameValidator
    username = models.CharField(max_length=100, unique=True, validators=[username_validator], verbose_name='Tên người dùng')
    email_validator = validators.validate_email
    email = models.EmailField(unique=True, validators=[email_validator], verbose_name='Email')

    first_name = models.CharField(max_length=100, verbose_name="Họ")
    last_name = models.CharField(max_length=100, verbose_name='Tên')
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True, verbose_name='Giới tính')
    birthday = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Địa chỉ')
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name='Ảnh đại diện')
    bio = models.TextField(null=True, blank=True, verbose_name='Giới thiệu')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'


    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'auth_user'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

class APIKey(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên')
    permission = models.ManyToManyField(Permission, blank=True, verbose_name='Quyền')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_apikey'
        verbose_name = 'APIKey'
        verbose_name_plural = 'APIKey'

    def key(self):
        return self.id


from django.apps import AppConfig


class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_user'
    verbose_name = 'Quản lý người dùng'

    # def ready(self):
    #     from auditlog.registry import auditlog
    #     from django.contrib.auth.models import User, Group

    #     auditlog.register(User)
    #     auditlog.register(Group)

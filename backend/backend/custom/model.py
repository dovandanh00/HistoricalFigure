from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings


user_model = settings.AUTH_USER_MODEL

class IsActivatedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active = True, is_deleted=False)

class IsNotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    
class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["order", "created_at"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order = models.IntegerField(null=True, blank=True, verbose_name=_("Thứ tự hiển thị"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Ngày khởi tạo"))
    created_by = models.ForeignKey(
        user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
        verbose_name=_("Người khởi tạo")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Ngày cập nhật"))
    updated_by = models.ForeignKey(
        to=user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
        verbose_name=_("Người cập nhật")
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_("Xóa"))
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Ngày xóa")
    )
    deleted_by = models.ForeignKey(
        to=user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleted",
        on_delete=models.SET_NULL,
        verbose_name=_("Người xóa")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Hoạt động"))

    objects = IsNotDeletedManager()
    objects_active = IsActivatedManager()
    objects_all = models.Manager()

    def restore(self): # Định nghĩa hàm restore dùng để khôi phục dữ liệu bị xóa mềm
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

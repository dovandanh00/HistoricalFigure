from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from django.contrib.admin.models import LogEntry

from .models import User, APIKey
from backend.custom.admin import BaseAdmin

# Register your models here.

class UserCustomAdmin(BaseAdmin, UserAdmin):
    list_display = ['username', 'email', 'avatar_column', 'first_name', 'last_name'] + BaseAdmin.base_list_display
    list_display_links = ['username', 'email', 'first_name', 'last_name'] + BaseAdmin.base_list_display_links
    list_filter = ['is_staff', 'is_superuser'] + BaseAdmin.base_list_filter
    search_fields = ['username', 'last_name']

    readonly_fields = ['avatar_preview'] + BaseAdmin.base_readonly_fields
    # fields = ['flag', 'flag_preview', 'name', 'des', 'short_name', 'arena', 'pop', 'link'] + BaseAdmin.base_fields
    fieldsets = [('Thông tin chung', {'fields': ('username', 'password', 'last_login', 'email', 'first_name', 'last_name')}),
                 ('Thông tin chi tiết', {'fields': ('order', 'gender', 'birthday', 'address', 'avatar', 'avatar_preview', 'bio')}),
                 ('Quyền', {'fields': ('is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions')})]
    add_fieldsets = [('Tạo tài khoản', {'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')}),
                 ]

    @admin.display(description='Ảnh đại diện')
    def avatar_column(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src={obj.avatar.url} style="with:100px;height:100px;object=fit:contain"/>')
        else:
            return ''
        
    @admin.display(description='')
    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src={obj.avatar.url} style="with:100px;height:100px;object=fit:contain"/>')
        else:
            return ''

class APIKeyAdmin(BaseAdmin):
    list_display = ['id', 'key', 'name'] + BaseAdmin.base_list_display
    list_display_links = ['id', 'key', 'name'] + BaseAdmin.base_list_display_links
    list_filter = ['name'] + BaseAdmin.base_list_filter
    search_fields = ['name']

    readonly_fields = ['id', 'key'] + BaseAdmin.base_readonly_fields
    fields = ['id', 'key', 'name', 'permission'] + BaseAdmin.base_fields


admin.site.register(User, UserCustomAdmin)
admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(LogEntry)
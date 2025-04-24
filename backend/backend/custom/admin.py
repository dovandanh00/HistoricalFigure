from django.contrib import admin
from django.utils import timezone


class BaseAdmin(admin.ModelAdmin):
    base_readonly_fields = ["created_by", "created_at", "updated_by", "updated_at", "is_deleted", "deleted_by", "deleted_at"]
    base_fields = ["order", "is_active"]
    base_list_display = ["order", "is_active"]
    base_list_display_links = ["order"]
    base_list_filter = ["is_active"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted:
                obj.delete()
            else:
                obj.is_deleted = True
                obj.deleted_by = request.user
                obj.deleted_at = timezone.now()
                obj.save()
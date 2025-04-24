from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ExhibitionArea, ExhibitionContent, Artifact
from backend.custom.admin import BaseAdmin

# Register your models here.

class ExhibitionAreaAdmin(BaseAdmin):
    list_display = ['name', 'description', 'location'] + BaseAdmin.base_list_display
    list_display_links = ['name'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['name']

    readonly_fields = BaseAdmin.base_readonly_fields
    fields = ['name', 'description', 'location'] + BaseAdmin.base_fields
    
class ExhibitionContentAdmin(BaseAdmin):
    list_display = ['exhibition_area_link', 'title', 'description', 'content_type', 'artifact_link', 'image_column', 'video_column', 'file_column'] + BaseAdmin.base_list_display
    list_display_links = ['exhibition_area_link', 'title', 'artifact_link', 'image_column', 'video_column', 'file_column'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['title', 'content_type']

    readonly_fields = ['image_preview', 'video_preview', 'file_preview'] + BaseAdmin.base_readonly_fields
    fields = ['exhibition_area', 'title', 'description', 'content_type', 'image', 'image_preview', 'video', 'video_preview', 'file', 'file_preview'] + BaseAdmin.base_fields
    
    @admin.display(description='Khu vực trưng bày')
    def exhibition_area_link(self, obj):
        return mark_safe(f'<a href="/admin/app_exhibition_visit/exhibitionarea/{obj.exhibition_area.id}/change/">{obj.exhibition_area.name}</a>')

    @admin.display(description="Hiện vật")
    def artifact_link(self, obj):
        if obj.content_type == 'artifact':  # Kiểm tra xem có hiện vật không
            return mark_safe(
                f'<a href="/admin/app_exhibition_visit/artifact/{obj.exhibition_content_artifact.id}/change/">{obj.exhibition_content_artifact.exhibition_content.title}</a>'
            )
        return ''
    
    @admin.display(description="Hình ảnh nội dung")
    def image_column(self, obj):
        if obj.image:  # Kiểm tra nếu có hình ảnh
            return mark_safe(
                f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return None
    
    @admin.display(description='')
    def image_preview(self, obj):
        if obj.image:  # Kiểm tra nếu có hình ảnh
            return mark_safe(
                f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return ''
    
    @admin.display(description="Video nội dung")
    def video_column(self, obj):
        if obj.video:  # Kiểm tra nếu có video
            return mark_safe(
                f'<video width="70" controls><source src="{obj.video.url}" type="video/mp4"></video>'
            )
        return None
    
    @admin.display(description='')
    def video_preview(self, obj):
        if obj.video:  # Kiểm tra nếu có video
            return mark_safe(
                f'<video width="70" controls><source src="{obj.video.url}" type="video/mp4"></video>'
            )
        return ''
    
    @admin.display(description="Tệp nội dung")
    def file_column(self, obj):
        if obj.file:  # Kiểm tra nếu có file
            return mark_safe(
                f'<a href="{obj.file.url}" target="_blank">Tải xuống để xem</a>'
            )
        return None
    @admin.display(description="")
    def file_preview(self, obj):
        if obj.file:  # Kiểm tra nếu có file
            return mark_safe(
                f'<a href="{obj.file.url}" target="_blank">Tải xuống để xem</a>'
            )
        return ''

class ArtifactAdmin(BaseAdmin):
    list_display = ['exhibition_content_link', 'origin', 'material', 'year'] + BaseAdmin.base_list_display
    list_display_links = ['exhibition_content_link'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['exhibition_content']

    readonly_fields = BaseAdmin.base_readonly_fields
    fields = ['exhibition_content', 'origin', 'material', 'year'] + BaseAdmin.base_fields

    @admin.display(description='Nội dung trưng bày')
    def exhibition_content_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_exhibition_visit/exhibitioncontent/{obj.exhibition_content.id}/change/">'
            f'{obj.exhibition_content.title} - {obj.exhibition_content.exhibition_area.name}</a>'
        )



admin.site.register(ExhibitionArea, ExhibitionAreaAdmin)
admin.site.register(ExhibitionContent, ExhibitionContentAdmin)
admin.site.register(Artifact, ArtifactAdmin)
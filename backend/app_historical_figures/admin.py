from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import HistoricalFigure, ImageFolder, HistoricalImage, HistoricalFilm, HistoricalDocument
from backend.custom.admin import BaseAdmin

# Register your models here.

class HistoricalFigureAdmin(BaseAdmin):
    list_display = ['name', 'avatar_column', 'birth_date', 'death_date', 'description', 'category', 'is_approve'] + BaseAdmin.base_list_display
    list_display_links = ['name'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['name']

    readonly_fields = ['avatar_preview'] + BaseAdmin.base_readonly_fields
    fields = ['name', 'avatar', 'avatar_preview', 'birth_date', 'death_date', 'description', 'category', 'is_approve'] + BaseAdmin.base_fields

    @admin.display(description='Ảnh danh nhân')
    def avatar_column(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return None
    
    @admin.display(description='')
    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return ''

class ImageFolderAdmin(BaseAdmin):
    list_display = ['historical_figure_link', 'name', 'description'] + BaseAdmin.base_list_display
    list_display_links = ['historical_figure_link', 'name'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['historical_figure', 'name']

    readonly_fields = BaseAdmin.base_readonly_fields
    fields = ['historical_figure', 'name', 'description'] + BaseAdmin.base_fields

    @admin.display(description='Danh nhân lịch sử')
    def historical_figure_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_historical_figures/historicalfigure/{obj.historical_figure.id}/change/">{obj.historical_figure.name}</a>'
        )
    
class HistoricalImageAdmin(BaseAdmin):
    list_display = ['historical_figure_link', 'folder_link', 'image_column', 'description'] + BaseAdmin.base_list_display
    list_display_links = ['historical_figure_link', 'folder_link', 'image_column'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['historical_figure', 'folder']

    readonly_fields = ['image_preview'] + BaseAdmin.base_readonly_fields
    fields = ['historical_figure', 'folder', 'image', 'image_preview', 'description'] + BaseAdmin.base_fields

    @admin.display(description='Hình ảnh danh nhân')
    def image_column(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
        )
    
    @admin.display(description='')
    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
        )
    
    @admin.display(description='Danh nhân lịch sử')
    def historical_figure_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_historical_figures/historicalfigure/{obj.historical_figure.id}/change/">{obj.historical_figure.name}</a>'
        )
    
    @admin.display(description='Thư mục hình ảnh')
    def folder_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_historical_figures/imagefolder/{obj.folder.id}/change/">{obj.folder.name}</a>'
        )
    
class HistoricalFilmAdmin(BaseAdmin):
    list_display = ['historical_figure_link', 'title', 'video_column', 'description', 'director', 'release_year', 'is_approve'] + BaseAdmin.base_list_display
    list_display_links = ['historical_figure_link', 'title', 'video_column'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['historical_figure', 'title']

    readonly_fields = ['video_preview'] + BaseAdmin.base_readonly_fields
    fields = ['historical_figure', 'title', 'video', 'video_preview', 'description', 'director', 'release_year', 'is_approve'] + BaseAdmin.base_fields

    @admin.display(description='Phim')
    def video_column(self, obj):
        return mark_safe(
            f'<video width="70" controls><source src="{obj.video.url}" type="video/mp4"></video>'
        )
    
    @admin.display(description='')
    def video_preview(self, obj):
        return mark_safe(
            f'<video width="70" controls><source src="{obj.video.url}" type="video/mp4"></video>'
        )
    
    @admin.display(description='Danh nhân lịch sử')
    def historical_figure_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_historical_figures/historicalfigure/{obj.historical_figure.id}/change/">{obj.historical_figure.name}</a>'
        )
    
class HistoricalDocumentAdmin(BaseAdmin):
    list_display = ['historical_figure_link', 'title', 'content', 'document_type', 'author', 'publish_year', 'file_column'] + BaseAdmin.base_list_display
    list_display_links = ['historical_figure_link', 'title', 'content', 'file_column'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['historical_figure', 'title']

    readonly_fields = ['file_preview'] + BaseAdmin.base_readonly_fields
    fields = ['historical_figure', 'title', 'content', 'document_type', 'author', 'publish_year', 'file', 'file_preview'] + BaseAdmin.base_fields

    @admin.display(description="Tệp tài liệu")
    def file_column(self, obj):
        return mark_safe(
            f'<a href="{obj.file.url}" target="_blank">Tải xuống để xem</a>'
        )
    
    @admin.display(description="")
    def file_preview(self, obj):
        return mark_safe(
            f'<a href="{obj.file.url}" target="_blank">Tải xuống để xem</a>'
        )

    @admin.display(description='Danh nhân lịch sử')
    def historical_figure_link(self, obj):
        return mark_safe(
            f'<a href="/admin/app_historical_figures/historicalfigure/{obj.historical_figure.id}/change/">{obj.historical_figure.name}</a>'
        )


admin.site.register(HistoricalFigure, HistoricalFigureAdmin)
admin.site.register(ImageFolder, ImageFolderAdmin)
admin.site.register(HistoricalImage, HistoricalImageAdmin)
admin.site.register(HistoricalFilm, HistoricalFilmAdmin)
admin.site.register(HistoricalDocument, HistoricalDocumentAdmin)
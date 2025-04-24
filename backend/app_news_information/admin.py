from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import NewsTopic, NewsArticle
from backend.custom.admin import BaseAdmin

# Register your models here.

class NewsTopicAdmin(BaseAdmin):
    list_display = ['name', 'description'] + BaseAdmin.base_list_display
    list_display_links = ['name'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['name']

    readonly_fields = BaseAdmin.base_readonly_fields
    fields = ['name', 'description'] + BaseAdmin.base_fields

class NewsArticleAdmin(BaseAdmin):
    list_display = ['news_topic_link', 'title', 'content', 'image_column', 'author'] + BaseAdmin.base_list_display
    list_display_links = ['news_topic_link', 'title'] + BaseAdmin.base_list_display_links
    list_filter = BaseAdmin.base_list_filter
    search_fields = ['news_topic', 'title', 'author']

    readonly_fields = ['image_preview'] + BaseAdmin.base_readonly_fields
    fields = ['news_topic', 'title', 'content', 'image', 'image_preview', 'author'] + BaseAdmin.base_fields

    @admin.display(description='Hình ảnh minh họa')
    def image_column(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return None
    
    @admin.display(description='')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="width:100px; height:100px; object-fit:contain;" />'
            )
        return ''
    @admin.display(description='Chủ đề tin tức')
    def news_topic_link(self, obj):
        if obj.news_topic:
            return mark_safe(
                f'<a href="/admin/app_news_information/newstopic/{obj.news_topic.id}/change/">{obj.news_topic.name}</a>'
            )
        return None



admin.site.register(NewsTopic, NewsTopicAdmin)
admin.site.register(NewsArticle, NewsArticleAdmin)
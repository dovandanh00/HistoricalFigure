from django.db import models

from backend.custom.model import BaseModel
from backend.custom.functions import upload_to

# Create your models here.


class NewsTopic(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Tên chủ đề')
    description = models.TextField(blank=True, verbose_name='Mô tả chủ đề')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_news_topic'
        verbose_name = 'Chủ đề tin tức'
        verbose_name_plural = 'Chủ đề tin tức'

    def __str__(self):
        return self.name
    
class NewsArticle(BaseModel):
    news_topic = models.ForeignKey(NewsTopic, null=True, blank=True, on_delete=models.SET_NULL, related_name='news_topic_article', verbose_name='Chủ đề tin tức')
    title = models.CharField(max_length=255, verbose_name='Tiêu đề bài viết')
    content = models.TextField(verbose_name='Nội dung bài viết')
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name='Hình ảnh minh họa')
    author = models.CharField(max_length=255, blank=True, verbose_name='Tác giả')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_news_article'
        verbose_name = 'Tin tức'
        verbose_name_plural = 'Tin tức'

    def __str__(self):
        return self.title
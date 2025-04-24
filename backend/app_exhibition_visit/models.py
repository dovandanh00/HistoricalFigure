from django.db import models

from backend.custom.model import BaseModel
from backend.custom.functions import upload_to

# Create your models here.

class ExhibitionArea(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Tên khu vực')
    description = models.TextField(blank=True, verbose_name='Mô tả khu vực')
    location = models.CharField(max_length=255, blank=True, verbose_name='Vị trí')

    class Meta: 
        ordering = ['order', 'created_at']
        db_table = 'tb_exhibition_area'
        verbose_name = 'Khu vực trưng bày'
        verbose_name_plural = 'Khu vực trưng bày'

    def __str__(self):
        return self.name
    
class ExhibitionContent(BaseModel):

    CONTENT_TYPE = [
        ('artifact', 'Hiện vật'),
        ('image', 'Hình ảnh'),
        ('video', 'Video'),
        ('document', 'Tài liệu'),
    ]

    exhibition_area = models.ForeignKey(ExhibitionArea, on_delete=models.CASCADE, related_name='exhibition_area_content', verbose_name='Khu vực trưng bày')
    title = models.CharField(max_length=255, verbose_name='Tiêu đề nội dung')
    description = models.TextField(blank=True, verbose_name='Mô tả nội dung')
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE, verbose_name='Kiểu nội dung')
    image = models.FileField(upload_to=upload_to, null=True, blank=True, verbose_name='Hình ảnh nội dung')
    video = models.FileField(upload_to=upload_to, null=True,blank=True, verbose_name='Video nội dung')
    file = models.FileField(upload_to=upload_to, null=True, blank=True, verbose_name='Tệp nội dung')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_exbihition_content'
        verbose_name = 'Nội dung trưng bày'
        verbose_name_plural = 'Nội dung trưng bày'

    def __str__(self):
        return f'{self.title} - {self.exhibition_area.name}'
    
class Artifact(BaseModel):
    exhibition_content = models.OneToOneField(ExhibitionContent, on_delete=models.CASCADE, related_name='exhibition_content_artifact', verbose_name='Nội dung trưng bày')
    origin = models.CharField(max_length=255, blank=True, verbose_name='Nguồn gốc')
    material = models.CharField(max_length=255, blank=True, verbose_name='Chất liệu')
    year = models.CharField(max_length=255, blank=True, verbose_name='Niên đại')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_artifact'
        verbose_name = 'Hiện vật'
        verbose_name_plural = 'Hiện vật'

    def __str__(self):
        return self.exhibition_content.title
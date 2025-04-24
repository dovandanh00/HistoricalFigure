from django.db import models

from backend.custom.model import BaseModel
from backend.custom.functions import upload_to

# Create your models here.

CATEGORY = [
    ('king', 'Vua'),
    ('genaral', 'Tướng'),
    ('scholar', 'Nhà học giả')
]


class HistoricalFigure(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Tên danh nhân')
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name='Ảnh danh nhân')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    death_date = models.DateField(null=True, blank=True, verbose_name='Ngày mất')
    description = models.TextField(blank=True, verbose_name='Mô tả danh nhân')
    category = models.CharField(max_length=100, choices=CATEGORY, verbose_name='Phân loại danh nhân')
    is_approve = models.BooleanField(default=False, verbose_name='Phê duyệt thông tin')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_historical_figure'
        verbose_name = 'Danh nhân lịch sử'
        verbose_name_plural = 'Danh nhân lịch sử'
        permissions = [
            ('can_approve_historical_figure', 'Can approve Danh nhân lịch sử')
        ]

    def __str__(self):
        return self.name
    
class ImageFolder(BaseModel):
    historical_figure = models.ForeignKey(HistoricalFigure, on_delete=models.CASCADE, related_name='historical_figure_folder', verbose_name='Danh nhân lịch sử')
    name = models.CharField(max_length=255, unique=True, verbose_name='Tên thư mục')
    description = models.TextField(blank=True, verbose_name='Mô tả thư mục')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_image_folder'
        verbose_name = 'Thư mục hình ảnh'
        verbose_name_plural = 'Thư mục hình ảnh'

    def __str__(self):
        return self.name
    
class HistoricalImage(BaseModel):
    folder = models.ForeignKey(ImageFolder, on_delete=models.CASCADE, related_name='folder_image', verbose_name='Thư mục hình ảnh')
    historical_figure = models.ForeignKey(HistoricalFigure, on_delete=models.CASCADE, related_name='historical_figure_image', verbose_name='Danh nhân lịch sử')
    image = models.ImageField(upload_to=upload_to, verbose_name='Hình ảnh danh nhân')
    description = models.TextField(blank=True, verbose_name='Mô tả hình ảnh')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_historical_image'
        verbose_name = 'Hình ảnh danh nhân'
        verbose_name_plural = 'Hình ảnh danh nhân'

    def __str__(self):
        return f'Hình ảnh của {self.historical_figure.name} - {self.folder.name}'
    
class HistoricalFilm(BaseModel):
    historical_figure = models.ForeignKey(HistoricalFigure, on_delete=models.CASCADE, related_name='historical_figure_film', verbose_name='Danh nhân lịch sử')
    title = models.CharField(max_length=255, verbose_name='Tiêu đề phim')
    video = models.FileField(upload_to=upload_to, verbose_name='Phim')
    description = models.TextField(blank=True, verbose_name='Mô tả phim')
    director = models.CharField(max_length=100, blank=True, verbose_name='Đạo diễn')
    release_year = models.IntegerField(null=True, blank=True, verbose_name='Năm phát hành')
    is_approve = models.BooleanField(default=False, verbose_name='Phê duyệt thông tin')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_historical_film'
        verbose_name = 'Phim tư liệu'
        verbose_name_plural = 'Phim tư liệu'
        permissions = [
            ('can_approve_historical_film', 'Can approve Phim tư liệu')
        ]

    def __str__(self):
        return self.title
    
class HistoricalDocument(BaseModel):

    DOCUMENT_TYPE = [
        ('directive', 'Chỉ thị'),
        ('decree', 'Sắc lệnh'),
        ('memoir', 'Hồi ký'),
        ('report', 'Báo cáo')
    ]

    historical_figure = models.ForeignKey(HistoricalFigure, on_delete=models.CASCADE, related_name='historical_figure_document', verbose_name='Danh nhân lịch sử')
    title = models.CharField(max_length=255, verbose_name='Tiêu đề tài liệu')
    content = models.TextField(blank=True, verbose_name='Nội dung tài liệu')
    document_type = models.CharField(max_length=100, default='report', choices=DOCUMENT_TYPE, verbose_name='Loại tài liệu')
    author = models.CharField(max_length=100, blank=True, verbose_name='Tác giả')
    publish_year = models.IntegerField(null=True, blank=True, verbose_name='Năm xuất bản')
    file = models.FileField(upload_to=upload_to, verbose_name='Tệp tài liệu')

    class Meta:
        ordering = ['order', 'created_at']
        db_table = 'tb_historical_document'
        verbose_name = 'Tài liệu nghiên cứu'
        verbose_name_plural = 'Tài liệu nghiên cứu'

    def __str__(self):
        return self.title
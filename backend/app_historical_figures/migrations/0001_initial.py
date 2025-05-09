# Generated by Django 5.1.6 on 2025-04-01 07:50

import backend.custom.functions
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorycalFigure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Thứ tự hiển thị')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Xóa')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Ngày xóa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Hoạt động')),
                ('name', models.CharField(max_length=255, verbose_name='Tên danh nhân')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=backend.custom.functions.upload_to, verbose_name='Ảnh danh nhân')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Ngày sinh')),
                ('death_date', models.DateField(blank=True, null=True, verbose_name='Ngày mất')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả danh nhân')),
                ('category', models.CharField(choices=[('king', 'Vua'), ('genaral', 'Tướng'), ('scholar', 'Nhà học giả')], max_length=100, verbose_name='Phân loại danh nhân')),
                ('approve', models.BooleanField(default=False, verbose_name='Phê duyệt thông tin')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người khởi tạo')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Người xóa')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
            ],
            options={
                'verbose_name': 'Danh nhân lịch sử',
                'verbose_name_plural': 'Danh nhân lịch sử',
                'db_table': 'tb_historical_figure',
                'ordering': ['order', 'created_at'],
                'permissions': [('can_approve_historical_figure', 'Can approve Danh nhân lịch sử')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalFilm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Thứ tự hiển thị')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Xóa')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Ngày xóa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Hoạt động')),
                ('title', models.CharField(max_length=255, verbose_name='Tiêu đề phim')),
                ('video', models.FileField(upload_to=backend.custom.functions.upload_to, verbose_name='Phim')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả phim')),
                ('director', models.CharField(blank=True, max_length=100, verbose_name='Đạo diễn')),
                ('release_year', models.IntegerField(blank=True, null=True, verbose_name='Năm phát hành')),
                ('approve', models.BooleanField(default=False, verbose_name='Phê duyệt')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người khởi tạo')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Người xóa')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
                ('historical_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_figure_film', to='app_historical_figures.historycalfigure', verbose_name='Danh nhân lịch sử')),
            ],
            options={
                'verbose_name': 'Phim tư liệu',
                'verbose_name_plural': 'Phim tư liệu',
                'db_table': 'tb_historical_film',
                'ordering': ['order', 'created_at'],
                'permissions': [('can_approve_historical_film', 'Can approve Phim tư liệu')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Thứ tự hiển thị')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Xóa')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Ngày xóa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Hoạt động')),
                ('title', models.CharField(max_length=255, verbose_name='Tiêu đề tài liệu')),
                ('content', models.TextField(blank=True, verbose_name='Nội dung tài liệu')),
                ('document_type', models.CharField(choices=[('directive', 'Chỉ thị'), ('decree', 'Sắc lệnh'), ('memoir', 'Hồi ký'), ('report', 'Báo cáo')], default='report', max_length=100, verbose_name='Loại tài liệu')),
                ('author', models.CharField(blank=True, max_length=100, verbose_name='Tác giả')),
                ('publish_year', models.IntegerField(blank=True, null=True, verbose_name='Năm xuất bản')),
                ('file', models.FileField(upload_to=backend.custom.functions.upload_to, verbose_name='Tệp tài liệu')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người khởi tạo')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Người xóa')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
                ('historical_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_figure_document', to='app_historical_figures.historycalfigure', verbose_name='Danh nhân lịch sử')),
            ],
            options={
                'verbose_name': 'Tài liệu nghiên cứu',
                'verbose_name_plural': 'Tài liệu nghiên cứu',
                'db_table': 'tb_historical_document',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='ImageFolder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Thứ tự hiển thị')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Xóa')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Ngày xóa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Hoạt động')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Tên thư mục')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả thư mục')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người khởi tạo')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Người xóa')),
                ('historical_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_figure_folder', to='app_historical_figures.historycalfigure', verbose_name='Danh nhân lịch sử')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
            ],
            options={
                'verbose_name': 'Thư mục hình ảnh',
                'verbose_name_plural': 'Thư mục hình ảnh',
                'db_table': 'tb_image_folder',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Thứ tự hiển thị')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Xóa')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Ngày xóa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Hoạt động')),
                ('image', models.ImageField(upload_to=backend.custom.functions.upload_to, verbose_name='Hình ảnh danh nhân')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả hình ảnh')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người khởi tạo')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_deleted', to=settings.AUTH_USER_MODEL, verbose_name='Người xóa')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
                ('historical_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_figure_image', to='app_historical_figures.historycalfigure', verbose_name='Danh nhân lịch sử')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_image', to='app_historical_figures.imagefolder', verbose_name='Thư mục hình ảnh')),
            ],
            options={
                'verbose_name': 'Hình ảnh danh nhân',
                'verbose_name_plural': 'Hình ảnh danh nhân',
                'db_table': 'tb_historical_image',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]

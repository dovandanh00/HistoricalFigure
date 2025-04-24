from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView, Response

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.utils import timezone

from rest_framework.decorators import action

from .models import HistoricalFigure, ImageFolder, HistoricalImage, HistoricalFilm, HistoricalDocument
from .serializers import (HistoricalFigureSerializer, HistoricalFigureOverviewSerializer,
                          ImageFolderSerializer, ImageFolderOverviewSerializer,
                          HistoricalImageSerializer, HistoricalImageOverviewSerializer,
                          HistoricalFilmSerializer, HistoricalFilmOverviewSerializer,
                          HistoricalDocumentSerializer, HistoricalDocumentOverviewSerializer)

from backend.custom.views import BaseView
from backend.custom.pagination import CustomPagination
from backend.custom.permissions import (CustomModelPermissions, IsOwnerPermission, 
                                        IsOwnerObjectPermission, IsSuperuserPermission,
                                        SpecialModelPermissions,)

# Create your views here.


class HistoricalFigureView(BaseView):
    queryset = HistoricalFigure.objects.filter(is_approve=True) # Lấy ra danh nhân đã được phê duyệt
    # serializer_class = HistoricalFigureSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')

        if self.request.user.has_perm('app_historical_figures.can_approve_historical_figure'):
            queryset = HistoricalFigure.objects.all() # Nếu user có quyền phê duyệt thì sẽ xem được tất cả danh nhân (bao gồm cả những danh nhân chưa được phê duyệt)
        else:
            queryset = self.queryset # Nếu user không có quyền phê duyệt thì chỉ trả ra những danh nhân đã được phê duyệt rồi
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__icontains=category)

        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return HistoricalFigureOverviewSerializer
        elif self.action in ['retrieve']:
            return HistoricalFigureSerializer
        else:
            return HistoricalFigureSerializer
        
    def get_permissions(self):
        if self.action in ['approve', 'unaprove']:
            return [SpecialModelPermissions(perm='can_approve_historical_figure')] # check permission special
        elif self.action in ['restore']:
            return [IsSuperuserPermission()]
        else:
            return [CustomModelPermissions()]
    
    @action(methods=['patch'], detail=True, url_path='approve') # Phê duyệt thông tin
    def approve(self, request, pk):
        try:

            historical_figure = HistoricalFigure.objects.get(id=pk)
            historical_figure.is_approve = True
            historical_figure.updated_by = request.user
            historical_figure.save()

            return Response('Danh nhân lịch sử đã được phê duyệt', status=200)
        
        except HistoricalFigure.DoesNotExist:

            return Response('Danh nhân lịch sử không tồn tại', status=404)
        
    @action(methods=['patch'], detail=False, url_path='bulk_approve')
    def bulk_approve(self, request):
        ids = request.data.get('ids')
        if not ids:
            return Response('Thiếu danh sách id', status=400)
        queryset = HistoricalFigure.objects.filter(id__in=ids)
        for historical_figure in queryset:
            if historical_figure.is_approve:
                pass
            else:
                historical_figure.is_approve = True
                historical_figure.updated_by = request.user
                historical_figure.save()
        return Response('Danh sách danh nhân lịch sử đã được phê duyệt', status=200)
        
    @action(methods=['patch'], detail=True, url_path='unapprove')
    def unaprove(self, request, pk):
        try:

            historical_figure = HistoricalFigure.objects.get(id=pk)
            historical_figure.is_approve = False
            historical_figure.updated_by = request.user
            historical_figure.save()

            return Response('Danh nhân lịch sử đã bỏ phê duyệt', status=200)
        
        except HistoricalFigure.DoesNotExist:
            
            return Response('Danh nhân lịch sử không tồn tại', status=404)
        
    @action(methods=['patch'], detail=False, url_path='bulk_unapprove')
    def bulk_unapprove(self, request):
        ids = request.data.get('ids')
        if not ids:
            return Response('Thiếu danh sách id', status=400)
        queryset = HistoricalFigure.objects.filter(id__in=ids)
        for historical_figure in queryset:
            if not historical_figure.is_approve:
                pass
            else:
                historical_figure.is_approve = False
                historical_figure.updated_by = request.user
                historical_figure.save()
        return Response('Danh sách danh nhân lịch sử đã bỏ phê duyệt', status=200)

class ImageFolderView(viewsets.ModelViewSet):
    queryset = ImageFolder.objects.all()
    # serializer_class = ImageFolderSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        historical_figure_name = self.request.query_params.get('historical_figure_name')
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        if historical_figure_name:
            queryset = queryset.filter(historical_figure__name__iexact=historical_figure_name)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return ImageFolderOverviewSerializer
        elif self.action in ['retrieve']:
            return ImageFolderSerializer
        else:
            return ImageFolderSerializer
        
class HistoricalImageView(viewsets.ModelViewSet):
    queryset = HistoricalImage.objects.all()
    # serializer_class = HistoricalImageSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        folder_name = self.request.query_params.get('folder_name')
        historical_figure_name = self.request.query_params.get('historical_figure_name')
        queryset = self.queryset
        if folder_name:
            queryset = queryset.filter(folder__name__iexact=folder_name)
        if historical_figure_name:
            queryset = queryset.filter(historical_figure__name__iexact=historical_figure_name)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return HistoricalImageOverviewSerializer
        elif self.action in ['retrieve']:
            return HistoricalImageSerializer
        else:
            return HistoricalImageSerializer
        
class HistoricalFilmView(viewsets.ModelViewSet):
    queryset = HistoricalFilm.objects.filter(is_approve=True)
    # serializer_class = HistoricalFilmSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        title = self.request.query_params.get('title')
        historical_figure_name = self.request.query_params.get('historical_figure_name')

        if self.request.user.has_perm('app_historical_figures.can_approve_historical_film'):
            queryset = HistoricalFilm.objects.all()
        else: 
            queryset = self.queryset
        if title:
            queryset = queryset.filter(title_icontains=title)
        if historical_figure_name:
            queryset = queryset.filter(historical_figure__name_iexact=historical_figure_name)

        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return HistoricalFilmOverviewSerializer
        elif self.action in ['retrieve']:
            return HistoricalFilmSerializer
        else:
            return HistoricalFilmSerializer
        
    def get_permissions(self):
        if self.action in ['approve', 'unapprove']:
            return [SpecialModelPermissions(perm='can_approve_historical_film')]
        else:
            return [CustomModelPermissions()]
        
    @action(methods=['patch'], detail=True, url_path='approve')
    def approve(self, request, pk):
        try:

            historical_film = HistoricalFilm.objects.get(id=pk)
            historical_film.is_approve = True
            historical_film.save()

            return Response('Phim tư liệu đã được phê duyệt', status=200)
        
        except HistoricalFilm.DoesNotExist:

            return Response('Phim tư liệu không tồn tại', status=404)
        
    @action(methods=['patch'], detail=False, url_path='bulk_approve')
    def bulk_approve(self, request):
        ids = request.data.get('ids')
        if not ids:
            return Response('Thiếu danh sách id', status=400)
        queryset = HistoricalFilm.objects.filter(id__in=ids)
        for historical_film in queryset:
            if historical_film.is_approve:
                pass
            else:
                historical_film.is_approve = True
                historical_film.updated_by = request.user
                historical_film.save()
        return Response('Danh sách phim tư liệu đã được phê duyệt', status=200)
        
    @action(methods=['patch'], detail=True, url_path='unapprove')
    def unapprove(self, request, pk):
        try:

            historical_film = HistoricalFilm.objects.get(id=pk)
            historical_film.is_approve = False
            historical_film.save()

            return Response('Phim tư liệu đã bỏ phê duyệt', status=200)
        
        except HistoricalFilm.DoesNotExist:

            return Response('Phim tư liệu không tồn tại', status=404)
        
    @action(methods=['patch'], detail=False, url_path='bulk_unapprove')
    def bulk_unapprove(self, request):
        ids = request.data.get('ids')
        if not ids:
            return Response('Thiếu danh sách id', status=400)
        queryset = HistoricalFilm.objects.filter(id__in=ids)
        for historical_film in queryset:
            if not historical_film.is_approve:
                pass
            else:
                historical_film.is_approve = False
                historical_film.updated_by = request.user
                historical_film.save()
        return Response('Danh sách phim tư liệu đã bỏ phê duyệt', status=200)
        
class HistoricalDocumentView(viewsets.ModelViewSet):
    queryset = HistoricalDocument.objects.all()
    # serializer_class = HistoricalDocumentSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        title = self.request.query_params.get('title')
        document_type = self.request.query_params.get('document_type')
        historical_figure_name = self.request.query_params.get('historical_figure_name')
        queryset = self.queryset
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        if historical_figure_name:
            queryset = queryset.filter(historical_figure__name__iexact=historical_figure_name)

        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return HistoricalDocumentOverviewSerializer
        elif self.action in ['retrieve']:
            return HistoricalDocumentSerializer
        else:
            return HistoricalDocumentSerializer

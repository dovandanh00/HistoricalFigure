from django.shortcuts import render
from rest_framework import viewsets

from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from .models import ExhibitionArea, ExhibitionContent, Artifact
from .serializers import ExhibitionAreaSerializer, ExhibitionAreaOverviewSerializer, ExhibitionContentSerializer, ExhibitionContentOverviewSerializer, ArtifactSerializer

from backend.custom.pagination import CustomPagination
from backend.custom.permissions import CustomModelPermissions, IsOwnerPermission, IsOwnerObjectPermission, IsSuperuserPermission

# Create your views here.

class ExhibitionAreaView(viewsets.ModelViewSet):
    queryset = ExhibitionArea.objects.all()
    # serializer_class = ExhibitionAreaSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        location = self.request.query_params.get('location')
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return ExhibitionAreaOverviewSerializer
        elif self.action in ['retrieve']:
            return ExhibitionAreaSerializer
        else:
            return ExhibitionAreaSerializer

class ExhibitionContentView(viewsets.ModelViewSet):
    queryset = ExhibitionContent.objects.all()
    # serializer_class = ExhibitionContentSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        title = self.request.query_params.get('title')
        content_type = self.request.query_params.get('content_type')
        queryset = self.queryset
        if title:
            queryset = queryset.filter(title__icontains=title)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return ExhibitionContentOverviewSerializer
        elif self.action in ['retrieve']:
            return ExhibitionContentSerializer
        else:
            return ExhibitionContentSerializer

class ArtifactView(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

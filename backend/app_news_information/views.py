from django.shortcuts import render
from rest_framework import viewsets

from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from .models import NewsTopic, NewsArticle
from .serializers import NewsTopicSerializer, NewsTopicOverviewSerializer, NewsArticleSerializer, NewsArticleOverviewSerializer

from backend.custom.pagination import CustomPagination
from backend.custom.views import BaseView
from backend.custom.permissions import CustomModelPermissions, IsOwnerPermission, IsOwnerObjectPermission, IsSuperuserPermission

# Create your views here.

class NewsTopicView(BaseView):
    queryset = NewsTopic.objects.all()
    # serializer_class = NewsTopicSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return NewsTopicOverviewSerializer
        elif self.action in ['retrieve']:
            return NewsTopicSerializer
        else:
            return NewsTopicSerializer

class NewsArticleView(BaseView):
    queryset = NewsArticle.objects.all()
    # serializer_class = NewsArticleSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        title = self.request.query_params.get('title')
        news_topic_name = self.request.query_params.get('news_topic_name')
        queryset = self.queryset
        if title:
            queryset = queryset.filter(title__icontains=title)
        if news_topic_name:
            queryset = queryset.filter(news_topic__name__iexact=news_topic_name) # Tìm kiếm bằng tên chủ đề, dùng iexact để tìm chính xác không phân biệt hoa thường
        return queryset

    def get_serializer_class(self):
        if self.action in ['list']:
            return NewsArticleOverviewSerializer
        elif self.action in ['retrieve']:
            return NewsArticleSerializer
        else:
            return NewsArticleSerializer



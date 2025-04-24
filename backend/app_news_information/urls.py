from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NewsTopicView, NewsArticleView

router = DefaultRouter()
router.register('news-topic', NewsTopicView, basename='news-topic')
router.register('news-article', NewsArticleView, basename='news-article')

urlpatterns = [

    path('', include(router.urls)),

]
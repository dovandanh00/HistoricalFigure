from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HistoricalFigureView, ImageFolderView, HistoricalImageView, HistoricalFilmView, HistoricalDocumentView

router = DefaultRouter()
router.register('historical-figure', HistoricalFigureView, basename='historical-figure')
router.register('image-folder', ImageFolderView, basename='image-folder')
router.register('historical-image', HistoricalImageView, basename='historical-image')
router.register('historical-film', HistoricalFilmView, basename='historical-film')
router.register('historical-document', HistoricalDocumentView, basename='historical-document')

urlpatterns = [

    path('', include(router.urls)),

]
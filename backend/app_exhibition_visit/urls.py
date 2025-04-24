from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExhibitionAreaView, ExhibitionContentView, ArtifactView

router = DefaultRouter()
router.register('exhibition-area', ExhibitionAreaView, basename='exhibition-area')
router.register('exhibition-content', ExhibitionContentView, basename='exhibition-content')
router.register('artifact', ArtifactView, basename='artifact')

urlpatterns = [

    path('', include(router.urls)),

]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserView, CreateSuperUserView, GroupView, PermissionView, APIKeyView, TokenView, LogoutView, LogEntryView

router = DefaultRouter()
router.register('user', UserView, basename='user')
router.register('create-superuser', CreateSuperUserView, basename='create-superuser')
router.register('groups', GroupView, basename='groups')
router.register('permissions', PermissionView, basename='permissions')
router.register('apikey', APIKeyView, basename='apikey')
router.register('logentry', LogEntryView, basename='logentry')

urlpatterns = [

    path('', include(router.urls)),

    path('login', TokenView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]
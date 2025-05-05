from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import Group, Permission
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from rest_framework.exceptions import ValidationError

from auditlog.models import LogEntry

from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
from django.utils import timezone

from .serializers import (UserSerializer, SuperUserSerializer, UserOverviewSerializer, GroupSerializer, 
                        PermissionSerializer, ChangePasswordSerializer, ResetPasswordSerializer, APIKeySerializer, LogEntrySerializer)
from .models import User, APIKey
from django.contrib.auth.models import Group

from backend.custom.views import BaseView
from backend.custom.pagination import CustomPagination
from backend.custom.permissions import IsOwnerPermission, CustomModelPermissions, IsOwnerObjectPermission, IsSuperuserPermission
from backend.custom.functions import check_validate_password, get_random_password


# Create your views here.


class UserView(BaseView):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name')
        last_name = self.request.query_params.get('last_name')
        group_id = self.request.query_params.get('group_id')
        group_name = self.request.query_params.get('group_name')
        avatar = self.request.query_params.get('avatar')
        queryset = self.queryset
        if avatar == '0':
            queryset = queryset.filter(avatar__isnull=True) # Lấy ra các obj có avatar (tức là null=False trong trường avatar)
        elif avatar == '1':
            queryset = queryset.filter(avatar__isnull=False) # Lấy ra các obj không có avatar (tức là null=True trong trường avatar), vì mặc định là để null=True (có thể bỏ trống)
        if group_id:
            queryset = queryset.filter(groups=group_id)
        if group_name:
            queryset = queryset.filter(groups__name__iexact=group_name)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name) # Tìm kiếm gần đúng giá trị và không phân biệt hoa thường bằng __icontains (__icontains có thể lúc chạy lúc không chạy do từng db)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserSerializer
        if self.action in ['retrieve'] and self.kwargs.get('pk') != str(self.request.user.id):
            return UserOverviewSerializer
        elif self.action in ['list']:
            return UserOverviewSerializer
        else:
            return UserSerializer
    
    def get_permissions(self): 
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerPermission()]
        elif self.action in ['reset_password']:
            return [IsSuperuserPermission()]
        else:
            return [permissions.IsAuthenticated(), IsOwnerPermission()]
        
    @action(methods=['post'], detail=True, url_path='add_perm')
    def add_permission(self, request, pk):
        perm_id = request.data.get('perm_id')
        if not perm_id:
            return Response('Thiếu perm_id', status=400)
        try:
            user = User.objects.get(id=pk)
            perm = Permission.objects.get(id=perm_id)
            user.user_permissions.add(perm)
            return Response('Đã thêm thành công quyền vào người dùng', status=200)
        except User.DoesNotExist:
            return Response('Người dùng không tồn tại', status=404)
        
    @action(methods=['patch'], detail=False, url_path='change_pass')
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request}) # Truyền request vào context
        if not serializer.is_valid(): # Gọi ra hàm is_valid() để chạy ChangePasswordSerializer
            return Response(serializer.errors, status=400)
        user = request.user
        new_pass = serializer.validated_data['new_pass']
        user.set_password(new_pass)
        user.save()
        return Response('Mật khẩu thay đổi thành công', status=200)

    @action(methods=['post'], detail=True, url_path='reset_password') # Chức năng này thường dùng cho admin/dev/support
    def reset_password(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = ResetPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            new_pass = serializer.validated_data['new_pass']
            user.set_password(new_pass)
            user.save()
            return Response('Đặt lại mật khẩu thành công', status=200)
        except User.DoesNotExist:
            return Response('Người dùng không tồn tại', status=404)
        

class CreateSuperUserView(viewsets.ViewSet,
                    generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperUserSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsSuperuserPermission]
        
class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsSuperuserPermission]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    @action(methods=['post'], detail=True, url_path='add_perm')
    def add_permission(self, request, pk):
        perm_id = request.data.get('perm_id')
        if not perm_id:
            return Response('Thiếu perm_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            perm = Permission.objects.get(id=perm_id)
            group.permissions.add(perm)
            return Response('Thêm permission vào nhóm thành công', status=200) # hoặc trả ra kiểu return Response(self.get_serializer_class()(obj).data, status=200)
        except Group.DoesNotExist:
            return Response('Group không tồn tại', status=404)
        except Permission.DoesNotExist:
            return Response('Permission không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
    @action(methods=['post'], detail=True, url_path='bulk_add_permission')
    def bulk_add_permission(self, request, pk):
        perm_ids = request.data.get('perm_ids')
        if not perm_ids:
            return Response('Thiếu danh sách permission id', status=400)
        try:
            group = Group.objects.get(id=pk)
            queryset = Permission.objects.filter(id__in=perm_ids)
            for perm in queryset:
                if perm in group.permissions.all():
                    pass
                else:
                    group.permissions.add(perm)
            return Response('Thêm danh sách permission vào nhóm thành công', status=200)
        except Group.DoesNotExist:
            return Response('Group không tồn tại', status=404)

    @action(methods=['delete'], detail=True, url_path='remove_perm')
    def remove_permission(self, request, pk):
        perm_id = request.data.get('perm_id')
        if not perm_id:
            return Response('Thiếu perm_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            perm = Permission.objects.get(id=perm_id)
            group.permissions.remove(perm)
            return Response('Đã xóa permission khỏi nhóm', status=200)
        except Group.DoesNotExist:
            return Response('Group không tồn tại', status=404)
        except Permission.DoesNotExist:
            return Response('Permission không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
    @action(methods=['delete'], detail=True, url_path='bulk_remove_permission')
    def bulk_remove_permission(self, request, pk):
        perm_ids = request.data.get('perm_ids')
        if not perm_ids:
            return Response('Thiếu danh sách perm_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            queryset = Permission.objects.filter(id__in=perm_ids)
            for perm in queryset:
                if perm not in group.permissions.all():
                    pass
                else:
                    group.permissions.remove(perm)
            return Response('Đã xóa danh sách quyền trong nhóm thành công', status=200)
        except Group.DoesNotExist:
            return Response('Nhóm không tồn tại', status=404)
    
    @action(methods=['post'], detail=True, url_path='add_user')
    def add_user(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response('Thiếu user_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            user = User.objects.get(id=user_id)
            group.user_set.add(user)
            return Response('Thêm user vào nhóm thành công', status=200)
        except Group.DoesNotExist:
            return Response('Group không tồn tại', status=404)
        except User.DoesNotExist:
            return Response('User không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
    @action(methods=['post'], detail=True, url_path='bulk_add_user')
    def bulk_add_user(self, request, pk):
        user_ids = request.data.get('user_ids')
        if not user_ids:
            return Response('Thiếu danh sách user_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            queryset = User.objects.filter(id__in=user_ids)
            for user in queryset:
                if user in group.user_set.all():
                    pass
                else:
                    group.user_set.add(user)
            return Response('Đã thêm danh sách user vào nhóm thành công', status=200)
        except Group.DoesNotExist:
            return Response('Nhóm không tồn tại', status=404)

    
    @action(methods=['delete'], detail=True, url_path='remove_user')
    def remove_user(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response('Thiếu user_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            user = User.objects.get(id=user_id)
            group.user_set.remove(user)
            return Response('Đã xóa user khỏi nhóm', status=200)
        except Group.DoesNotExist:
            return Response('Group không tồn tại', status=404)
        except User.DoesNotExist:
            return Response('User không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
    @action(methods=['delete'], detail=True, url_path='bulk_remove_user')
    def bulk_remove_user(self, request, pk):
        user_ids = request.data.get('user_ids')
        if not user_ids:
            return Response('Thiếu danh sách user_id', status=400)
        try:
            group = Group.objects.get(id=pk)
            queryset = User.objects.filter(id__in=user_ids)
            for user in queryset:
                if user not in group.user_set.all():
                    pass
                else:
                    group.user_set.remove(user)
            return Response('Đã xóa danh sách user khỏi nhóm', status=200)
        except Group.DoesNotExist:
            return Response('Nhóm không tồn tại', status=404) # Mai test api
        
class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsSuperuserPermission]

class APIKeyView(BaseView):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsSuperuserPermission]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            try:
                queryset = queryset.filter(name__icontains=name)
            except:
                queryset = []
        return queryset
    
    @action(methods=['post'], detail=True, url_path='add_perm')
    def add_permission(self, request, pk):
        perm_id = request.data.get('perm_id')
        if not perm_id:
            return Response('Thiếu perm_id', status=400)
        try:
            apikey = APIKey.objects.get(id=pk)
            perm = Permission.objects.get(id=perm_id)
            apikey.permission.add(perm)
            return Response('Thêm thành công permission vào apikey', status=200)
        except APIKey.DoesNotExist:
            return Response('APIKey không tồn tại', status=404)
        except Permission.DoesNotExist:
            return Response('Permission không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
    @action(methods=['delete'], detail=True, url_path='remove_perm')
    def remove_permission(self, request, pk):
        perm_id = request.data.get('perm_id')
        if not perm_id:
            return Response('Thiếu perm_id', status=400)
        try:
            apikey = APIKey.objects.get(id=pk)
            perm = Permission.objects.get(id=perm_id)
            apikey.permission.remove(perm)
            return Response('Đã xóa permission khỏi apikey', status=200)
        except APIKey.DoesNotExist:
            return Response('APIKey không tồn tại', status=404)
        except Permission.DoesNotExist:
            return Response('Permission không tồn tại', status=404)
        except Exception as e:
            return Response(str(e), status=404)
        
class LogEntryView(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    pagination_class = CustomPagination
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomModelPermissions]

    def get_queryset(self):
        username = self.request.query_params.get('username')
        queryset = self.queryset
        if username:
            queryset = queryset.filter(user__username__iexact=username)
        return queryset
        
class TokenView(OAuthLibMixin, APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username_email = request.data.get('username_email')
        password = request.data.get('password')
        user = None
        if not username_email or not password:
            return Response('Thiếu thông tin đăng nhập', status=400)
        
        try:

            if '@' in username_email:
                username = User.objects.get(email=username_email).username # Tìm đối tượng user theo username_email được truyền vào rồi lấy thuộc tính username của đối tượng vừa tìm được gán vào biến username
            else:
                username = username_email

            user = authenticate(username=username, password=password) # Kiểm tra xem username và password có tồn tại trong DB hay không

            if not user:
                return Response('Sai tên đăng nhập hoặc mật khẩu')
        
        except User.DoesNotExist:
            return Response('Người dùng không tồn tại')
        
        post = request.data.copy() # Tạo request giả xong gán dữ liệu ở bên dưới vào
        post['username'] = user.username
        post['client_id'] = settings.CLIENT_ID
        post['client_secret'] = settings.CLIENT_SECRET
        post['grant_type'] = 'password'
        request._request.POST = post # Truyền data cho OAuthLibMixin

        _, _, body, status = self.create_token_response(request._request) # Tạo token dựa vào request thêm vào ở bên trên, hàm create_token_response() sẽ trả về 4 giá trị header, response, body, status
        body = json.loads(body) # Chuyển dữ liệu về dạng dict trước khi gửi về client vì hàm create_token_response() sẽ trả về body dạng chuỗi JSON (str)
        # body['group'] = user.group.id if user.group else None # custom trả ra thêm group nếu api yêu cầu

        if status == 200:
            user.last_login = timezone.now()
            user.save()

        return Response(body, status=status)
    
class LogoutView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        all = request.data.get('all')
        if all:
            access_token = AccessToken.objects.filter(user=request.user)
            refresh_token = RefreshToken.objects.filter(user=request.user)
            access_token.delete()
            refresh_token.delete()
            return Response('Đã đăng xuất khỏi tất cả các thiết bị', status=200)
        else:
            access_token = AccessToken.objects.get(token=request.auth)
            refresh_token = RefreshToken.objects.get(access_token=access_token)
            access_token.delete()
            refresh_token.delete()
            return Response('Đã đăng xuất khỏi thiết bị', status=200)
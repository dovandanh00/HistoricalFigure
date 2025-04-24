from rest_framework.permissions import BasePermission
from app_user.models import APIKey


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
    
class IsOwnerObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
    
class IsSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class CustomModelPermissions(BasePermission):
    def has_permission(self, request, view):
        app_name = view.queryset.model._meta.app_label
        model_name = view.queryset.model._meta.model_name

        apikey = request.query_params.get('api_key')
        if apikey: 
            try:
                key = APIKey.objects.get(id=apikey)
                if not key.is_active:
                    return False
                if request.method == 'GET':
                    return True if f'view_{model_name}' in [i.codename for i in key.permission.all()] else False
                elif request.method == 'POST':
                    return True if f'add_{model_name}' in [i.codename for i in key.permission.all()] else False
                elif request.method == 'PATCH'or request.method == 'PUT':
                    return True if f'change_{model_name}' in [i.codename for i in key.permission.all()] else False
                elif request.method == 'DELETE':
                    return True if f'delete_{model_name}' in [i.codename for i in key.permission.all()] else False
                else:
                    return False
            except:
                return False

        if request.method == 'GET':
            # return request.user.has_perm(f'{app_name}.view_{model_name}') or request.user.is_superuser
            return True
        elif request.method == 'POST':
            return request.user.has_perm(f'{app_name}.add_{model_name}') or request.user.is_superuser
        elif request.method == 'PATCH' or request.method == 'PUT':
            return request.user.has_perm(f'{app_name}.change_{model_name}') or request.user.is_superuser
        elif request.method == 'DELETE':
            return request.user.has_perm(f'{app_name}.delete_{model_name}') or request.user.is_superuser
        else:
            return False
        
class SpecialModelPermissions(BasePermission): # Kiểm tra quyền đặc biệt cho user (vd: approve permission)
    def __init__(self, perm=None):
        self.perm = perm
        super().__init__()

    def has_permission(self, request, view):
        app_name = view.queryset.model._meta.app_label
        return request.user.is_superuser or request.user.has_perm(f'{app_name}.{self.perm}')
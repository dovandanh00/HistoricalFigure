from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from auditlog.models import LogEntry

import json

from .models import User, APIKey
from backend.custom.functions import check_validate_password


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_login', 'first_name', 'last_name', 
                  'gender', 'birthday', 'address', 'avatar', 'bio', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_groups(self, obj):
        groups = obj.groups.all()
        if not groups:
            return []
        results = []
        for group in groups:
            results.append({
                'id': group.id,
                'name': group.name,
                'permissions': self.get_permissions(group)
            })
        return results
    
    def get_permissions(self, group):
        permissions = group.permissions.all()
        if not permissions:
            return []
        results = []
        for permission in permissions:
            results.append({
                'id': permission.id,
            })
        return results

    def create(self, validated_data): # Hàm này sẽ chạy khi post dữ liệu hợp lệ lên để tạo mới user
        groups = validated_data.pop('groups', [])  # Lấy danh sách nhóm (.pop() giúp lấy dữ liệu và loại bỏ nó khỏi validated_data để tránh lỗi khi tạo User)
        permissions = validated_data.pop('user_permissions', [])  # Lấy danh sách quyền
        user = User.objects.create_user(**validated_data) # Dữ liệu hợp lệ sẽ truyền vào hàm create_user để kiểm tra username, emai, password hợp lệ, nếu hợp lệ sẽ tạo mới user
        user.groups.set(groups)  # Sử dụng .set() để gán nhóm
        user.user_permissions.set(permissions)  # Dùng .set() để gán quyền
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        id = self.context.get('request').query_params.get('id')
        fields = self.context.get('request').query_params.get('fields')

        if fields: # Chỉ trả ra những trường mà truyền vào params
            fields_list = [item.strip() for item in fields.split(',')]
            for i in list(data.keys()):
                if i not in fields_list:
                    del data[i]

        if id == '0': # Ẩn hiện fields khi có điều kiện nào đó (vd: ẩn hiện fields 'id' khi truyền vào id = 0)
            del data['id']

        # if not data['avatar']:
        #     data['avatar'] = 'link...' # Sửa dữ liệu json trả ra (tính năng của hàm to_representation())

        return data
    
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_login', 'first_name', 'last_name', 
                  'gender', 'birthday', 'address', 'avatar', 'bio', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', []) # Lấy danh sách nhóm (.pop() giúp lấy dữ liệu và loại bỏ nó khỏi validated_data để tránh lỗi khi tạo User)
        user_permissions = validated_data.pop('user_permissions', []) # Lấy danh sách quyền
        user = User.objects.create_superuser(**validated_data) # Tạo User bằng dữ liệu hợp lệ được truyền vào
        user.groups.set(groups) # Gán lại danh sách nhóm vào User bằng hàm set()
        user.user_permissions.set(user_permissions) # Gán lại danh sách quyền vào User bằng hàm set()
        return user # Trả ra User đã tạo đầy đủ
    
class UserOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 
                  'gender', 'birthday', 'address', 'avatar', 'bio']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        id = self.context.get('request').query_params.get('id')
        fields = self.context.get('request').query_params.get('fields')

        if id == '0':
            del data['id']

        if fields:
            fields_list = [item.strip() for item in fields.split(',')]
            for i in list(data.keys()):
                if i not in fields_list:
                    del data[i]
        
        # if not data['avatar']:
        #     data['avatar'] = 'link...'

        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)

    def validate_old_pass(self, old_pass): # Kiểm tra mật khẩu cũ có đúng hay không
        user = self.context['request'].user # Lấy user từ context request
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Mật khẩu cũ không chính xác')
        return old_pass
    
    def validate_new_pass(self, new_pass): # Kiểm tra hợp lệ new_pass khi truyền vào từ data
        check_validate_password(new_pass)
        return new_pass
    
    def validate(self, data):
        if data['old_pass'] == data['new_pass']: # Lấy ra dữ liệu mk cũ và mk mới rồi so sánh
            raise serializers.ValidationError('Mật khẩu cũ và mật khẩu mới không được trùng nhau')
        return data
    
class ResetPasswordSerializer(serializers.Serializer):
    new_pass = serializers.CharField(required=True)
    confirm_pass = serializers.CharField(required=True)

    def validate_new_pass(self, new_pass):
        check_validate_password(new_pass)
        return new_pass
    
    def validate(self, data):
        if data['new_pass'] != data['confirm_pass']:
            raise serializers.ValidationError('Mật khẩu xác nhận không khớp')
        return data

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class APIKeySerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    class Meta:
        model = APIKey
        fields = ['id', 'key', 'name', 'permission']

    def get_key(self, obj):
        return obj.id
    
class LogEntrySerializer(serializers.ModelSerializer):
    # action_flag = serializers.SerializerMethodField()
    # user = serializers.SerializerMethodField()
    # content_type = serializers.SerializerMethodField()
    # change_message = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        # fields = ['id', 'action_time', 'object_id', 'object_repr', 
        #           'action_flag', 'change_message', 'user', 'content_type']
        fields = '__all__'
        
    # def get_action_flag(self, obj):
    #     if obj.action_flag == 1:
    #         return 'Thêm'
    #     elif obj.action_flag == 2:
    #         return 'Thay đổi'
    #     else:
    #         return 'Xóa'
        
    # def get_user(self, obj):
    #     if not obj.user:
    #         return None
    #     return {
    #         'id': obj.user.id,
    #         'username': obj.user.username,
    #     }
    
    # def get_content_type(self, obj):
    #     if not obj.content_type:
    #         return None
    #     return {
    #         'id': str(obj.content_type.id),
    #         'app_label': obj.content_type.app_label,
    #         'model': obj.content_type.model,
    #     } 
    
    # def get_change_message(self, obj):
    #     try:
    #         messages = json.loads(obj.change_message) # Chuyển Json str thành python dict
    #     except Exception:
    #         return obj.change_message # Nếu change_message ko phải Json str thì trả về chuỗi ban đầu
    #     results = []
    #     for message in messages:
    #         if 'added' in message:
    #             name = message['added'].get('name', '') # Lấy name trong added
    #             results.append(f'Đã thêm: {name}')
    #         elif 'changed' in message:
    #             fields = message['changed'].get('fields', [])
    #             results.append(f'Đã thay đổi các trường: {fields}')
    #         elif 'deleted' in message:
    #             name = message['deleted'].get('name', '')
    #             results.append(f'Đã xóa: {name}')
    #     return results if results else None
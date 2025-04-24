from rest_framework import viewsets
from rest_framework.views import Response

from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

from django.http import Http404
from django.utils import timezone


class BaseView(viewsets.ModelViewSet):
    def perform_create(self, serializer): # Thêm thông tin người tạo trước khi serializer dữ liệu để lưu vào db (override hàm perform_create để truyền thêm thông tin user đang gửi request)
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer): # Thêm thông tin người cập nhật trước khi serializer dữ liệu để lưu vào db (override hàm perform_update để truyền thêm thông tin user đang gửi request)
        serializer.save(updated_by=self.request.user)

    def destroy(self, request, pk):
        instance = self.queryset.model.objects_all.get(pk=pk)
        if not instance.is_deleted:
            instance.is_deleted = True
            instance.deleted_by = request.user
            instance.deleted_at = timezone.now()
            instance.save()
            return Response('Đã xóa mềm', status=200)
        else:
            instance.delete()
            return Response('Đã xóa vĩnh viễn', status=204)
        
    def bulk_destroy(self, request, queryset):
        for instance in queryset:
            if not instance.is_deleted:
                instance.is_deleted = True
                instance.deleted_by = request.user
                instance.deleted_at = timezone.now()
                instance.save()
            else:
                instance.delete()

    def get_object_all(self, pk):
        try:
            return self.queryset.model.objects_all.get(pk=pk) # truy vấn tất cả bản ghi mà ko bị lọc bởi is_deleted=True trong hàm get_queryset() (tức là truy vấn trực tiếp vào model bỏ qua get_queryset())
                                                            # self.queryset.model chính là model của class đang dùng (vd: HistoricalFigure)
                                                            # --> self.queryset.model.objects_all.get(pk=pk) = HistoricalFigure.objects_all.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            raise NotFound('Không tìm thấy đối tượng') # Dùng hàm get...() khi mà muốn trả ra lỗi thì ko nên trả ra return Response mà phải trả ra raise ...

    @action(methods=['patch'], detail=True, url_path='restore') # Khôi phục lại dữ liệu bị xóa mềm
    def restore(self, request, pk): 
        instance = self.get_object_all(pk) # Truyền pk vào hàm get_object_all để gọi hàm

        if not instance.is_deleted:
            return Response('Đối tượng này chưa bị xóa mềm', status=400)
        
        instance.restore() # Hàm restore này đã được định nghĩa ở bên models (dùng hàm này bằng cách gọi lại trong action)
        
        return Response('Đã khôi phục xóa mềm', status=200)
    
    @action(methods=['patch'], detail=False, url_path='bulk_restore')
    def bulk_restore(self, request):
        ids = request.data.get('ids')
        if not ids:
            return Response('Thiếu danh sách id', status=400)
        
        queryset = self.queryset.model.objects_all.filter(id__in=ids)

        for instance in queryset:
            if not instance.is_deleted: # Bỏ qua những đối tượng chưa bị xóa mềm
                pass
            else:
                instance.restore()

        return Response('Đã khôi phục danh sách xóa mềm', status=200)
    
    @action(methods=['delete'], detail=False, url_path='bulk_destroy')
    def bulk_destroy_action(self, request):
        ids = request.data.get('ids')

        if not ids:
            return Response('Thiếu danh sách id', status=400)
        
        queryset = self.queryset.model.objects_all.filter(id__in=ids) # Lấy những obj có id nằm trong list ids mà user gửi lên (id__in là lấy nhiều obj theo list id)
        self.bulk_destroy(request, queryset)

        return Response('Đã xử lý xóa', status=200)
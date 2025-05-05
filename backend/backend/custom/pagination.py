from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings


class CustomPagination(PageNumberPagination):
    page_size = 10 # Mặc định bằng 10 object/1 trang
    page_query_param = 'page' # Tên tham số trong URL để chỉ trang số mấy (?page=1)
    page_size_query_param = 'per_page' # Tên tham số trong URL để chỉ bao nhiêu object/1 trang (?per_page=50 hoặc dùng ?page_size cùng được)
    max_page_size = 1000 # Tối đa 1000 object/1 trang

    def get_page_size(self, request): # override hàm get_page_size
        page_size = request.query_params.get("page_size")
        if page_size:
            return page_size
        else:
            return self.page_size
        
    def paginate_queryset(self, queryset, request, view=None):
        if 'all' in request.query_params and len(queryset): # Nếu có all trong query_params và dữ liệu không rỗng thì sẽ trả ra hết dữ liệu không phân trang nữa
            self.page_size = len(queryset) # len(queryset) là đếm toàn bộ dữ liệu có trong DB và gán nó bằng page_size (vd: len(queryset)=50 thì page_size=50)
            return super().paginate_queryset(queryset, request, view)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'page_size': len(data), # len(data) là đếm toàn bộ dữ liệu ở trong trang 
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': f'{settings.API_URL}{self.get_next_link()[21:]}' if self.get_next_link() else None,
            'previous': f'{settings.API_URL}{self.get_previous_link()[21:]}' if self.get_previous_link() else None,
            'results': data,
        })
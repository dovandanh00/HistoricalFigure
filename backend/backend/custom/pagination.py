from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def get_page_size(self, request):
        page_size = request.query_params.get("page_size")
        if page_size:
            return page_size
        else:
            return self.page_size
        
    def paginate_queryset(self, queryset, request, view=None):
        if 'all' in request.query_params and len(queryset):
            self.page_size = len(queryset)
            return super().paginate_queryset(queryset, request, view)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'page_size': len(data),
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': f'{settings.API_URL}{self.get_next_link()[21:]}' if self.get_next_link() else None,
            'previous': f'{settings.API_URL}{self.get_previous_link()[21:]}' if self.get_previous_link() else None,
            'results': data,
        })
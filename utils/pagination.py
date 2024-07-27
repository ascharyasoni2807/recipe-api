
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow client to override, using `?page_size=xxx`
    max_page_size = 100  # Maximum limit for page size

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        total_counts = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        max_page_size = min(total_counts, 100)

        return Response({
            'total_counts': total_counts,
            'total_pages': self.page.paginator.num_pages,
            'per_page_count': page_size,
            'current_page': self.page.number,
            'max_page_size': max_page_size,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            try:
                page_size = int(request.query_params['page_size'])
                return min(page_size, self.max_page_size)
            except (TypeError, ValueError):
                pass
        return self.page_size

"""
Pagination classes and mixins
"""

# pylint: disable=missing-function-docstring
from rest_framework import pagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class ArticlePaginator(pagination.PageNumberPagination):
    """
    Returns a paginated list of articles
    """
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        assert self is not None
        return Response({
            'results': data,
            'links': {
                'previous': self.get_previous_link(),
                'next': self.get_next_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE))
        })


class PaginationHandlerMixin():
    """
    hanldes pagination on view
    """

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

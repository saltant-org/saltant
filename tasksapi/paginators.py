"""Contains paginators for the API.

See http://www.django-rest-framework.org/api-guide/pagination/
"""

from rest_framework.pagination import PageNumberPagination


class PageNumberVariableSizePagination(PageNumberPagination):
    """A paginator that allows for variable page size."""
    page_size_query_param = 'page_size'

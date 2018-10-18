"""Contains paginators for the API.

See http://www.django-rest-framework.org/api-guide/pagination/
"""

from rest_framework.pagination import PageNumberPagination


class PageNumberVariableSizePagination(PageNumberPagination):
    """A paginator that allows for variable page size."""

    page_size_query_param = "page_size"


class LargeResultsSetPagination(PageNumberVariableSizePagination):
    """A paginator that shows lots of results."""

    page_size = 100


class SmallResultsSetPagination(PageNumberVariableSizePagination):
    """A paginator that shows _some_ results."""

    page_size = 10

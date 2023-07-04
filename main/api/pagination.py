from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class EnterprisePaginator(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100
    # last_page_strings = 'end'


class EdificacionLOPagination(LimitOffsetPagination):
    default_limit = 1

from rest_framework.pagination import LimitOffsetPagination


class ListPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limited'
    offset_query_param = 'offset'

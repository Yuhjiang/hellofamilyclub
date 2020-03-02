from rest_framework.pagination import LimitOffsetPagination


class PostListPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'limited'
    offset_query_param = 'offset'

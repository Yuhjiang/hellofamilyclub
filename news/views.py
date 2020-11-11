from rest_framework import viewsets

from .models import NewsType, HelloNews
from .serializers import NewsTypeSerializer, HelloNewsSerializer, NewsTypeSerializerList, \
    HelloNewsSerializerEdit
from .pagination import ListPagination
from hellofamilyclub.utils.decorators import admin_required_api, login_required_api


class NewsTypeViewSet(viewsets.ModelViewSet):
    serializer_class = NewsTypeSerializer
    queryset = NewsType.objects.filter()
    pagination_class = ListPagination

    @admin_required_api(message='管理员才可添加分类')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = NewsTypeSerializerList
        return super().list(request, *args, **kwargs)


class HelloNewsViewSet(viewsets.ModelViewSet):
    serializer_class = HelloNewsSerializer
    queryset = HelloNews.objects.filter().order_by('-created_date')
    pagination_class = ListPagination

    def get_queryset(self):
        query_params = self.request.query_params
        params = {}
        if query_params.get('category'):
            params['category_id'] = int(query_params['category'])
        if query_params.get('group'):
            params['group__in'] = [int(query_params['group'])]
        if query_params.get('member'):
            params['member__in'] = [int(query_params['member'])]
        new_queryset = self.queryset.filter(**params)
        return new_queryset

    @admin_required_api(message='只有管理员可以修改资讯内容')
    def update(self, request, *args, **kwargs):
        self.serializer_class = HelloNewsSerializerEdit
        return super().update(request, *args, **kwargs)

    @admin_required_api(message='只有管理员可以添加资讯内容')
    def create(self, request, *args, **kwargs):
        self.serializer_class = HelloNewsSerializerEdit
        return super().create(request, *args, **kwargs)

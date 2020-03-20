from rest_framework import viewsets

from .models import NewsType, HelloNews
from .serializers import NewsTypeSerializer, HelloNewsSerializer
from .pagination import ListPagination
from hellofamilyclub.utils.decorators import admin_required_api, login_required_api


class NewsTypeViewSet(viewsets.ModelViewSet):
    serializer_class = NewsTypeSerializer
    queryset = NewsType.objects.filter()
    pagination_class = ListPagination

    # @admin_required_api(message='管理员才可添加分类')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class HelloNewsViewSet(viewsets.ModelViewSet):
    serializer_class = HelloNewsSerializer
    queryset = HelloNews.objects.filter()
    pagination_class = ListPagination

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Group, Member, CarouselPicture
from .serializers import GroupSerializer, MemberSerializer, CarouselPictureSerializer
from .pagination import ListPagination
from hellofamilyclub.utils.decorators import admin_required_api


class GroupList(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            'created_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({'status': 200, 'errMsg': '',
                         'data': {'groups': serializer.data}})


class MemberList(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get_queryset(self):
        if self.request.query_params.get('group_id'):
            group_id = int(self.request.query_params['group_id'])
            return Member.objects.filter(group_id=group_id).order_by('-status')
        else:
            return Member.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({'status': 200, 'errMsg': '',
                         'data': {'members': serializer.data}})


class CarouselPictureViewSet(viewsets.ModelViewSet):
    serializer_class = CarouselPictureSerializer
    queryset = CarouselPicture.objects.filter()
    pagination_class = ListPagination

    @admin_required_api(message='你没有权限添加图片')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @admin_required_api(message='你没有权限修改图片')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @admin_required_api(message='你没有权限删除图片')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = CarouselPicture.STATUS_DELETE
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
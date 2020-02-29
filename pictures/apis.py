from rest_framework import generics
from rest_framework.response import Response

from .models import Group, Member
from .serializers import GroupSerializer, MemberSerializer


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

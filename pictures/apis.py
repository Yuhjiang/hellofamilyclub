from rest_framework import generics

from .models import Group, Member
from .serializers import GroupSerializer, MemberSerializer


class GroupList(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter()


class MemberList(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get_queryset(self):
        if self.request.query_params.get('group_id'):
            group_id = int(self.request.query_params['group_id'])
            return Member.objects.filter(group_id=group_id).order_by('-status')
        else:
            return Member.objects.filter()

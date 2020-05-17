from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from album.models import Album, Picture
from album.serializers import AlbumSerializer, PictureSerializer
from album.pagination import LimitOffsetPagination
from hellofamilyclub.utils.permissions import SameUserPermission


class CreateMixin:
    def create(self, request, *args, **kwargs):
        query_dict = request.data.copy()
        query_dict['owner'] = request.user.id
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AlbumViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    pagination_class = LimitOffsetPagination
    # permission_classes = [IsAuthenticated & SameUserPermission]


class PictureViewSet(viewsets.ModelViewSet):
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()

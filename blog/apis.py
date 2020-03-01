from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from blog.models import Post
from blog.serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.filter()

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = PostListSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        query_dict = request.data.copy()
        # owner要从token里取出来
        query_dict['owner'] = request.user.id
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
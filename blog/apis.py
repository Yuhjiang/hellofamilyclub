from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Category, Tag, Picture
from blog.serializers import PostListSerializer, PostDetailSerializer, CategorySerializer,\
    TagSerializer
from blog.pagination import PostListPagination
from hellofamilyclub.utils.decorators import login_required_api


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.filter()
    pagination_class = PostListPagination

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


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    def create(self, request, *args, **kwargs):
        query_dict = request.data.copy()
        # owner要从token里取出来
        query_dict['owner'] = request.user.id
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
@login_required_api
def upload_picture(request):
    """
    上传图片的接口，存储默认使用七牛云
    :param request:
    :return:
    """
    file = request.FILES['content']
    user = request.user
    instance = Picture(name=file.name, content=file, owner_id=user.id)
    instance.save()
    return Response({'status': 200, 'data': {'url': instance.content.url}})

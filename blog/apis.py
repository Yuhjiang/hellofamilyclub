from django.db.models import F, Q
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Category, Tag, Picture
from blog.serializers import PostListSerializer, PostDetailSerializer, CategorySerializer,\
    TagSerializer, PostCreateSerializer, CategoryUpdateSerializer, PostUpdateSerializer
from blog.pagination import ListPagination
from hellofamilyclub.utils.decorators import login_required, login_required_api, admin_required_api,\
    same_user_required_api


class CreateMixin:
    @login_required_api()
    def create(self, request, *args, **kwargs):
        query_dict = request.data.copy()
        # owner要从token里取出来
        query_dict['owner'] = request.user.id
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateMixin:
    @same_user_required_api
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        query_dict = request.data.copy()
        query_dict['owner'] = request.user.id
        serializer = self.get_serializer(instance, data=query_dict, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PostViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.filter(~Q(status=0))
    pagination_class = ListPagination

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        self.handle_visit(request.user, kwargs.get('pk'))
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = PostListSerializer
        return super().list(request, *args, **kwargs)

    @login_required_api()
    def create(self, request, *args, **kwargs):
        self.serializer_class = PostCreateSerializer
        return super().create(request, *args, **kwargs)

    @same_user_required_api(message='你没有权限修改文章')
    def update(self, request, *args, **kwargs):
        self.serializer_class = PostUpdateSerializer
        return super().update(request, *args, **kwargs)

    @same_user_required_api(message='你没有权限删除文章')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @staticmethod
    def handle_visit(user, post_id):
        """
        TODO 后续要把统计阅读量的逻辑放进redis，不要每次访问都进行统计
        记录某个用户对某篇文章的访问
        :param user: 用户
        :param post_id: 文章id
        :return:
        """
        if not user:
            user_id = -1
        else:
            user_id = 1
        key = 'visit:{}:{}'.format(user_id, post_id)
        if not cache.get(key):
            Post.objects.filter(pk=post_id).update(amount=F('amount') + 1)
            cache.set(key, 60)


class CategoryViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    pagination_class = ListPagination

    def update(self, request, *args, **kwargs):
        self.serializer_class = CategoryUpdateSerializer
        return super().update(request, *args, **kwargs)

    @same_user_required_api(message='你没有权限删除分类')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TagViewSet(CreateMixin, UpdateMixin, viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)
    pagination_class = ListPagination

    @same_user_required_api(message='你没有权限删除标签')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
@login_required
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

from datetime import datetime

from django.db.models import F, Q
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Category, Tag, Comment
from album.models import Picture, Album
from blog.serializers import PostListSerializer, PostDetailSerializer, CategorySerializer,\
    TagSerializer, PostCreateSerializer, CategoryUpdateSerializer, PostUpdateSerializer, \
    CommentListSerializer, CommentCreateSerializer
from blog.pagination import ListPagination
from hellofamilyclub.utils.decorators import login_required, login_required_api, admin_required_api,\
    same_user_required_api
from hellofamilyclub.utils.websocket import send_message


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

    def get_queryset(self):
        query_params = self.request.query_params

        params = {}
        if query_params.get('category'):
            params['category_id'] = int(query_params['category'])
        if query_params.get('tag'):
            params['tag'] = int(query_params['tag'])
        if query_params.get('title'):
            params['title__contains'] = query_params['title']
        if query_params.get('nickname'):
            params['owner__nickname__contains'] = query_params['nickname']
        if query_params.get('owner'):
            params['owner__nickname__contains'] = query_params['owner']
        if query_params.get('start_date') and query_params.get('end_date'):
            params['created_time__range'] = (
                datetime.strptime(query_params['start_date'], '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(query_params['end_date'], '%Y-%m-%d %H:%M:%S'))
        new_queryset = self.queryset.filter(**params)
        return new_queryset

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

    def get_queryset(self):
        query_params = self.request.query_params

        params = {}
        if query_params.get('name'):
            params['name__contains'] = query_params['name']
        new_queryset = self.queryset.filter(**params)
        return new_queryset

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

    def get_queryset(self):
        query_params = self.request.query_params

        params = {}
        if query_params.get('name'):
            params['name__contains'] = query_params['name']
        new_queryset = self.queryset.filter(**params)
        return new_queryset

    @same_user_required_api(message='你没有权限删除标签')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all().order_by('-created_time')
    pagination_class = ListPagination

    def get_queryset(self):
        query_params = self.request.query_params
        new_queryset = self.queryset
        params = {}
        if query_params.get('post_id'):
            params['post_id'] = int(query_params['post_id'])
        if query_params.get('status') or query_params.get('status') == 0:
            params['status'] = int(query_params['status'])
        new_queryset = new_queryset.filter(**params)
        return new_queryset

    @login_required_api('请登录后再进行评论')
    def create(self, request, *args, **kwargs):
        self.serializer_class = CommentCreateSerializer
        send_comment_message(request)
        return super().create(request, *args, **kwargs)


def send_comment_message(request):
    room_name = request.data.get('to_user')
    content = request.data.get('content')
    current_user = request.user.nickname
    message = '评论了你: {}'.format(content)

    send_message(room_name, message, current_user)


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
    album = get_default_album(user.id)
    instance = Picture(name=file.name, content=file, owner_id=user.id, album_id=album)
    instance.save()
    return Response({'status': 200, 'data': {'url': instance.content.url}})


def get_default_album(user_id):
    """
    获取某个人用户的默认相册
    :param user_id: 用户id
    :return: Album id
    """
    try:
        album = Album.objects.get(owner_id=user_id, name='默认相册')
        return album.id
    except Album.DoesNotExist:
        return None

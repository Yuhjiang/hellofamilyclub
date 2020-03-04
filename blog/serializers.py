from datetime import datetime

from rest_framework import serializers

from .models import Post, Category, Tag
from user.models import HelloUser


class PostListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'desc', 'owner', 'created_time', 'updated_time',
                  'amount']


class PostDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.filter())
    tag = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.filter(), many=True)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=HelloUser.objects.filter())
    amount = serializers.IntegerField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'content', 'draft',
                  'category', 'tag', 'owner', 'created_time', 'updated_time',
                  'is_md', 'amount']

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.updated_time = datetime.now()
        instance.save()
        return instance


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'content', 'draft',
                  'category', 'tag', 'owner', 'created_time', 'updated_time',
                  'is_md', 'amount']

    def create(self, validated_data):
        # tag是多对多，所以需要实例化一个对象后再添加
        tags = validated_data.pop('tag')
        post = Post(**validated_data)
        post.save()
        post.updated_time = datetime.now()
        post.tag.set(tags)
        return post


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'created_time', 'is_nav', 'owner', 'color', 'post_count')

    def get_post_count(self, obj):
        return obj.post_set.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_time', 'owner', 'color')


if __name__ == '__main__':
    p = Post.objects.filter()[0]
    print(PostDetailSerializer(p).data)

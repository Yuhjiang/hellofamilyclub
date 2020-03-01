from datetime import datetime

from rest_framework import serializers

from .models import Post


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
    # owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    amount = serializers.IntegerField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'desc', 'content', 'content_html', 'draft',
                  'category', 'tag', 'owner', 'created_time', 'updated_time',
                  'is_md', 'amount']

    def create(self, validated_data):
        # tag是多对多，所以需要实例化一个对象后再添加
        tags = validated_data.pop('tag')
        post = Post(**validated_data)
        post.save()
        post.tag.set(tags)
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.updated_time = datetime.now()
        instance.save()
        return instance


if __name__ == '__main__':
    p = Post.objects.filter()[0]
    print(PostDetailSerializer(p).data)

from datetime import datetime

from django.contrib import admin

from blog.models import Category, Tag, Post


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    创建分类和标签时增加创建者
    """
    exclude = ('owner', 'updated_time')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status')

    def post_count(self, obj):
        return obj.post_set.count()


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'desc', 'amount', 'category', 'owner', 'created_time',
                    'updated_time')
    fields = ('title', 'desc', 'content', 'category', 'tag', )
    filter_horizontal = ('tag', )

    def save_model(self, request, obj, form, change):
        obj.update_time = obj.created_time
        return super().save_model(request, obj, form, change)

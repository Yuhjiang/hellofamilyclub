from django.contrib import admin

from .models import Group, Member
from .adminforms import MemberAdminForm


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_jp', 'name_en', 'created_time', 'status')
    list_filter = ('status', )
    search_fields = ('name', 'name_jp', 'name_en')

    fieldsets = (
        ('基本信息', {
            'description': None,
            'fields': (
                ('name', 'name_jp', 'name_en'),
                ('status', 'created_time')
            )
        }),
        ('其他信息', {
            'description': None,
            'fields': (
                ('color', ),
                ('homepage', ),
                ('favicon', )
            )
        })
    )

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm
    list_display = ('name', 'name_jp', 'name_en', 'nickname', 'birthday',
                    'status', 'hometown', 'joined_time', 'graduated_time',
                    'group')
    list_filter = ('status', 'group__name_jp')
    search_fields = ('name', 'name_jp', 'name_en', 'group__name')

    fieldsets = (
        ('基本信息', {
            'description': None,
            'fields': (
                ('name', 'name_jp', 'name_en', 'nickname', 'group'),
                ('status', 'birthday', 'joined_time', 'graduated_time')
            )
        }),
        ('其他信息', {
            'description': None,
            'fields': (
                ('color', 'hometown'),
                ('favicon', )
            )
        })
    )

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True
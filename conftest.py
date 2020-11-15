import pytest

from user.models import HelloUser, Role
from hellofamilyclub.utils.base_test import BaseUser


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    print('初始化测试环境')
    with django_db_blocker.unblock():
        admin = Role.objects.create(name='admin', desc='最高权限')
        normal = Role.objects.create(name='normal', desc='普通用户')

        admin_user = HelloUser.objects.create_user(
            username=BaseUser.admin, password=BaseUser.password
        )
        admin_user.role = admin
        admin_user.is_admin = True
        admin_user.save()
        normal_user = HelloUser.objects.create_user(
            username=BaseUser.normal, password=BaseUser.password
        )


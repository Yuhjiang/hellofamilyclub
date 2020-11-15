from typing import Dict, List, Tuple

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from user.models import HelloUser


class BaseUser:
    anonymous = 'none'
    admin = 'admin'
    normal = 'hello'
    password = '1230zxcvas'


@pytest.mark.django_db
class BaseViewTest:
    @pytest.fixture(scope='function')
    def client(self) -> APIClient:
        client = APIClient()
        return client

    @pytest.fixture(scope='function')
    def anonymous_client(self) -> APIClient:
        client = APIClient(user=None)
        return client

    @pytest.fixture(scope='function')
    def admin_client(self) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=HelloUser.objects.get(
            username=BaseUser.admin))
        return client

    @pytest.fixture(scope='function')
    def normal_client(self) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=HelloUser.objects.get(
            username=BaseUser.normal))
        return client

    @pytest.fixture(scope='function')
    def all_client(self, anonymous_client: APIClient, admin_client: APIClient,
                   normal_client: APIClient) -> Dict[str, APIClient]:
        return {
            BaseUser.anonymous: anonymous_client,
            BaseUser.admin: admin_client,
            BaseUser.normal: normal_client,
        }


def add_permission(basic: List[Tuple[str, int]], add: Tuple[str, int]):
    basic = basic.copy()
    basic.append(add)

    return basic


class AdminPermission:
    base_permission = [
        (BaseUser.anonymous, status.HTTP_401_UNAUTHORIZED),
        (BaseUser.normal, status.HTTP_403_FORBIDDEN),
    ]

    read_permission = pytest.mark.parametrize(
        'user, expect_code',
        add_permission(base_permission,
                       (BaseUser.admin, status.HTTP_200_OK))
    )

    create_permission = pytest.mark.parametrize(
        'user, expect_code',
        add_permission(base_permission,
                       (BaseUser.admin, status.HTTP_201_CREATED))
    )

    delete_permission = pytest.mark.parametrize(
        'user, expect_code',
        add_permission(base_permission,
                       (BaseUser.admin, status.HTTP_204_NO_CONTENT))
    )

    update_permission = pytest.mark.parametrize(
        'user, expect_code',
        add_permission(base_permission,
                       (BaseUser.admin, status.HTTP_200_OK))
    )

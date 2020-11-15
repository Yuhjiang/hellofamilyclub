from typing import Dict

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


class AdminPermission:
    read_only = pytest.mark.parametrize(
        'user, expect_code',
        [
            (BaseUser.anonymous, status.HTTP_401_UNAUTHORIZED),
            (BaseUser.admin, status.HTTP_200_OK),
            (BaseUser.normal, status.HTTP_403_FORBIDDEN),
        ]
    )
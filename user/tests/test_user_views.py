from typing import Dict

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from utils.base_test import BaseViewTest, AdminPermission
from user.models import HelloUser


@pytest.mark.django_db
class TestUserView(BaseViewTest):
    @AdminPermission.read_permission
    def test_permission(self, all_client: Dict[str, APIClient], user: str,
                        expect_code: int):
        client = all_client[user]

        response = client.get(
            reverse('user-list'),
        )

        assert response.status_code == expect_code

    @AdminPermission.delete_permission
    def test_permission(self, all_client: Dict[str, APIClient], user: str,
                        expect_code: int):
        client = all_client[user]
        user = HelloUser.objects.create_user(username='1234', password='1230xc')

        response = client.delete(
            reverse('user-detail', args=(user.id, )),
        )

        assert response.status_code == expect_code


@pytest.mark.django_db
class TestUserRegister(BaseViewTest):
    def test_register(self, anonymous_client: APIClient):
        data = dict(
            username='hello123',
            password='1230zxcvas',
            nickname='hello',
            email='13041@qq.com'
        )

        response = anonymous_client.post(
            reverse('user-register'),
            data=data,
            format='json',
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert HelloUser.objects.filter(username=data['username']).exists()

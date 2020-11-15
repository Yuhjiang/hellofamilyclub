from typing import Dict

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from hellofamilyclub.utils.base_test import BaseViewTest, AdminPermission


@pytest.mark.django_db
class TestUserView(BaseViewTest):
    @AdminPermission.read_only
    def test_permission(self, all_client: Dict[str, APIClient], user: str,
                        expect_code: int):
        client = all_client[user]

        response = client.get(
            reverse('user-list'),
        )

        assert response.status_code == expect_code

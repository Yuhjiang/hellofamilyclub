import os
from datetime import date, datetime

import django
from django.test import TestCase, Client

from .views import MemberFaceAPI
from .models import Member, Group

profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))


class MemberTestCase(TestCase):
    def setUp(self):
        group = Group.objects.create(
            name='morning musume',

        )
        Member.objects.create(
            name='mizuki',
            name_jp='hello',
            name_en='project',
            status=0,
            joined_time=date.today(),
            group_id=group.id
        )

    def test_create_member(self):
        member = Member.objects.create(
            name='mizuki111',
            name_jp='hello',
            name_en='project',
            status=0,
            joined_time=date.today(),
            group_id=1
        )
        member.save()

        result = Member.objects.get(name='mizuki111')
        self.assertEqual(result.name_jp, 'hello')

    def test_get_face(self):
        client = Client()
        response = client.get('/api/pictures/')
        self.assertEqual(response.status_code, 200, 'status code must be 200')


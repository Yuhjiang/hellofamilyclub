import os
import sys
from datetime import datetime

import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))
django.setup()

from user.models import HelloUser
from album.models import Album


def init_album():
    """
    初始化相册
    :return:
    """
    users = HelloUser.objects.all()
    for user in users:
        album = Album(owner_id=user.id, updated_time=datetime.now())
        album.save()


if __name__ == '__main__':
    init_album()

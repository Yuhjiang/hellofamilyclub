"""
迁移hellofamily.club旧人脸识别数据
"""
import logging
from datetime import datetime

import django

from pictures.service.config import db_client, mongo_db
django.setup()
from pictures.models import Member


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s -'
                               ' %(message)s')
logger = logging.getLogger(__name__)


def translate_name(name):
    """
    因为老数据的缘故，导致有些人名错了，需要翻译一下
    :param name: 成员或组合名
    :return:
    """
    name_dict = {
        'ruru_dambara': 'ruru_danbara',
        'memi_tamura': 'meimi_tamura',
        'chisaki_morito_m': 'chisaki_morito',
        'musubu_funaki_a': 'musubu_funaki'
    }

    return name_dict.get(name, name)


def migrate_one(image):
    """
    迁移一条数据，现在的数据格式
    name, url, created_time, created_date, members, size, downloaded, recognized
    members: id, name_en, name_jp, group
    :param image:
    :return:
    """
    timestamp = image['timestamp']
    created_time = datetime.fromtimestamp(timestamp)
    size = image['size']
    one = {'name': image['name'], 'url': image['url'], 'downloaded': False,
           'created_time': created_time,
           'created_date': created_time.replace(hour=0, minute=0, second=0)}
    if size >= 1:
        one['recognized'] = True
    else:
        one['recognized'] = False

    members = []
    for member in image['members']:
        name_en = translate_name(member['name_en'])
        try:
            current_member = Member.objects.get(name_en=name_en)
            members.append({'id': current_member.id,
                            'name_en': current_member.name_en,
                            'name_jp': current_member.name_jp,
                            'group': current_member.group.name_en})
        except Member.DoesNotExist:
            logger.error("Not Found {}".format(name_en))
    one['size'] = len(members)
    one['members'] = members

    return one


def migrate_all():
    names = mongo_db['images'].distinct('name')
    images = list(db_client['helloproject']['images'].find(
        {'name': {'$nin': names}}))
    for image in images:
        exist = mongo_db['images'].find_one({'name': image['name']})
        if not exist:
            result = migrate_one(image)
            mongo_db['images'].insert_one(result)
        else:
            continue


if __name__ == '__main__':
    migrate_all()
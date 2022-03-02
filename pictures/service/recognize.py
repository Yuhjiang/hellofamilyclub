"""
识别模块
"""
import logging
import os
import time
from datetime import datetime, timedelta

import django

django.setup()
from pictures.models import Member
from hellofamilyclub.utils.utils import image_to_base64, download_picture

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s -'
                               ' %(message)s')
logger = logging.getLogger(__name__)


def recognize_multi(picture: dict, url: str, image_type: str, save=False,
                    redownload=False):
    """
    M:N识别人像，
    :param picture: mongo存储记录，需要使用'name'和'created_time'字段
    :param url: 图片地址
    :param image_type: 图片名，从本地去取
    :param save: 是否存数据库
    :param redownload: 需要识别的图片在本地不存在时，是否重新下载它
    :return:
    """
    name = picture['name']
    if name.split('.')[-1] == 'gif':
        return None

    if image_type == 'BASE64':
        # 图片按照日期分文件夹存储
        image_dir = os.path.join(IMAGE_DIR, str(picture['created_time'].date()))
        file_path = os.path.join(image_dir, name)
        if not os.path.exists(file_pclasath) and redownload:
            # 图片不存在并要重下载
            download_picture(picture['url'], path=image_dir, file_name=name)
        image = image_to_base64(file_path)
        if not image:
            return None
    else:
        image = url
    group_id_list = 'Hello_Project'
    options = {
        'max_face_num': 10,
        'match_threshold': 70,
        'max_user_num': 1,
    }
    response = client.multiSearch(image, image_type, group_id_list, options)

    if save and response['error_msg'] == 'SUCCESS':
        face_to_database(name, response)
    return True


def face_to_database(name, response):
    face_list = response['result']['face_list']
    members = []
    for face in face_list:
        if face['user_list']:
            name_en = face['user_list'][0]['user_id']
            try:
                member = Member.objects.get(name_en=name_en)
                members.append({
                    'id': member.id,
                    'name_en': member.name_en,
                    'name_jp': member.name_jp,
                    'group': member.group.name_en,
                })
            except Member.DoesNotExist:
                logger.error("Not Found {}".format(name_en))
    members = {'$set': {'members': members, 'size': len(members),
                        'recognized': True}}
    mongo_db['images'].update_one({'name': name}, members)


def recognize_all_pictures():
    pictures = list(mongo_db['images'].find(
        {'recognized': False,
         'created_time': {'$gte': datetime.now() - timedelta(days=7)}}
    ))
    for picture in pictures:
        try:
            recognize_multi(picture, url=picture['url'], image_type='BASE64',
                            save=True, redownload=True)
        except Exception as e:
            logger.error(e)
        time.sleep(0.5)
    logger.info("recognize_all_pictures end!")


if __name__ == '__main__':
    # # recognize_multi('http://cdn.helloproject.com/img/rotation/e71f732f2172dee0dcaed2960db291f3c420f933.jpg')
    # recognize_multi('785f6650gy1gbwzacr3n5g20bo0fa4qy.gif',
    #                 'https://wx1.sinaimg.cn/mw690/785f6650gy1gbwzacr3n5g20bo0fa4qy.gif',
    #                 'BASE64')
    recognize_all_pictures()
    pass

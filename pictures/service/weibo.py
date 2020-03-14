"""
爬虫下载照片
"""
import os
import requests
import logging
import json
from datetime import datetime

import django
# from django.core.mail import send_mail

from pictures.service.config import headers, image_url, IMAGE_DIR, mongo_db
from hellofamilyclub.utils.utils import download_picture
from pictures.tasks import send_recognize_mail as send_mail

django.setup()
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s -'
                               ' %(message)s')
logger = logging.getLogger(__name__)


def get_cookie():
    return mongo_db['cookie'].find({}).limit(1).sort(
        'update_time', -1)[0]['cookie']


def fetch_json_response(url):
    """
    获取url的json数据
    :param url: 默认小晴的相册
    :return: 返回photo_list
    """
    res = requests.get(url, headers=headers).json()
    if not res['result']:
        logger.error('failed to download data {}'.format(url))
        return []
    else:
        return res['data']['photo_list']


def get_pictures_info(start=1, end=1, save=False, download=False):
    """
    解析json，获取照片信息
    :param start: 开始页
    :param end: 结束页
    :param save: 是否存mongo
    :param download: 是否下载到本地
    :return:
    """
    for page in range(start, end + 1):
        url = image_url.format(page)
        try:
            photo_list = fetch_json_response(url)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            send_mail.delay('微博爬虫模块出错', message='出错信息: {}'.format(e),
                            from_email='jiangyuhao@hellofamily.club', recipient_list=[
                    'jiang.yuhao0809@gmail.com', ], fail_silently=False)
            break
        except Exception as e:
            logger.error(e)
            send_mail.delay('微博爬虫模块出错', message='出错信息: {}'.format(e),
                            from_email='jiangyuhao@hellofamily.club', recipient_list=[
                    'jiang.yuhao0809@gmail.com', ], fail_silently=False)
            break

        data_to_save = []
        for photo in photo_list:
            name = photo['pic_name']
            url = photo['pic_host'] + '/mw690/' + name
            timestamp = photo['timestamp']
            created_time = datetime.fromtimestamp(timestamp)

            data_to_insert = {
                'name': name,
                'url': url,
                'created_time': created_time,
                'created_date': created_time.replace(hour=0, minute=0, second=0),
                'members': [],
                'size': 0,  # 图片里的人数
                'downloaded': False,  # 是否被下载到本地
                'recognized': False  # 是否被识别过
            }

            exist = mongo_db['images'].find_one({'name': name})
            if download is True:
                if (exist and not exist['downloaded']) or not exist:
                    # 存在记录但没下载过，或者没有记录
                    image_dir = os.path.join(
                        IMAGE_DIR, str(created_time.date()))
                    download_picture(url, image_dir, name, save=True)
                    data_to_insert['downloaded'] = True

            if save is True and not exist:
                # 已经存储过的就不管了,没存储过的存储
                data_to_save.append(data_to_insert)

        if data_to_save:
            mongo_db['images'].insert_many(data_to_save)


def fetch_weibo_pictures():
    logger.info("fetch_weibo_pictures start!")
    try:
        headers['Cookie'] = get_cookie()
        get_pictures_info(1, 20, save=True, download=True)
    except Exception as e:
        logger.error(e)
    logger.info("fetch_weibo_pictures end!")


if __name__ == '__main__':
    fetch_weibo_pictures()

"""
爬虫下载照片
"""
import requests
from datetime import datetime

from pictures.service import mongo_db
from pictures.service.config import headers, image_url, IMAGE_DIR
from hellofamilyclub.utils.utils import download_picture, logger


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
    for page in range(start, end+1):
        url = image_url.format(page)
        photo_list = fetch_json_response(url)

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
                'members': [],
                'size': 0,              # 图片里的人数
                'downloaded': False,    # 是否被下载到本地
                'recognized': False       # 是否被识别过
            }

            if download is True:
                download_picture(url, IMAGE_DIR, name)
                data_to_insert['downloaded'] = True

            if save is True:
                data_to_save.append(data_to_insert)

        if data_to_save:
            mongo_db['images'].insert_many(data_to_save)


if __name__ == '__main__':
    get_pictures_info(1, 1, save=True, download=True)
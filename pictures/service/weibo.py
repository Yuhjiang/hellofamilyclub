"""
爬虫下载照片
"""
import requests
from datetime import datetime

from pictures.service.config import headers, image_url, IMAGE_DIR, mongo_db
from hellofamilyclub.utils.utils import download_picture, logger


def get_cookie():
    return mongo_db['cookie'].find({}).limit(1).sort(
        'update_time', -1)[0]['cookie']


def fetch_json_response(url):
    """
    获取url的json数据
    :param url: 默认小晴的相册
    :return: 返回photo_list
    """
    headers['Cookie'] = get_cookie()
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
                'created_date': created_time.replace(hour=0, minute=0, second=0),
                'members': [],
                'size': 0,              # 图片里的人数
                'downloaded': False,    # 是否被下载到本地
                'recognized': False       # 是否被识别过
            }

            exist = mongo_db['images'].find_one({'name': name})
            if download is True and exist and not exist['downloaded']:
                download_picture(url, IMAGE_DIR, name, save=True)
                data_to_insert['downloaded'] = True

            if save is True and not exist:
                # 已经存储过的就不管了,没存储过的存储
                data_to_save.append(data_to_insert)

        if data_to_save:
            mongo_db['images'].insert_many(data_to_save)


def fetch_weibo_pictures():
    try:
        get_pictures_info(1, 20, save=True, download=True)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    fetch_weibo_pictures()
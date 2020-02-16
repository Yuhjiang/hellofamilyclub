"""
通用方法
"""
import requests
import os
import base64
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def valid_image(image):
    return image.history == []


def download_picture(url, path, file_name, **kwargs):
    image = requests.get(url, **kwargs)
    if not valid_image(image):
        logger.error('Failed to download the picture {}'.format(url))
        return None
    if not os.path.exists(path):
        os.mkdir(path)

    image_path = os.path.join(path, file_name)
    if os.path.exists(image_path):
        return None
    with open(image_path, 'ab') as f:
        f.write(image.content)


def page_limit_skip(page, limit):
    if not limit:
        limit = 20
    limit = int(limit)
    if not page:
        return limit, 0
    else:
        page = int(page)
        return limit, (page - 1) * limit


if __name__ == '__main__':
    download_picture()

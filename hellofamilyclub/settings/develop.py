"""
开发环境Django设置
"""
import os

from hellofamilyclub.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '123-zxcvAS',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': "hellofamily_db",
        'TEST': {
            'NAME': 'test_hellofamily_db',
        }
    }
}

# 微博爬虫和识别
MONGODB = {
    'url': 'mongodb://10.20.3.232:27017'
}
IMAGE_DIR = '/Users/yuhao/Pictures/hellofamily'
IMAGE_URL = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
            '&type=3&__rnd=1546678278092'
# 百度人工智能key
APP_ID = '14303012'
API_KEY = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'

REDIS_URL = 'redis://127.0.0.1:6379/1'

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = 'hellofamily.club邮件报警'

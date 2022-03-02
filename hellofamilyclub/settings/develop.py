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
        'NAME': "hellofamily_bak",
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
# 百度人工智能key
APP_ID = '14303012'
API_KEY = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'
APP_GROUP_ID = 'Hello_Project'

REDIS_URL = 'redis://127.0.0.1:6379/1'

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = 'hellofamily.club邮件报警'

REQUESTS_PROXY = {
    'http': 'http://localhost:1087',
    'https': 'http://localhost:1087',
}

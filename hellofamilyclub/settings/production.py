from .base import *

DEBUG = False

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
ALLOWED_HOSTS = ['hellofamily.club']

# 微博爬虫和识别
MONGODB = {
    'url': 'mongodb://localhost:27017'
}
IMAGE_DIR = '/home/images/hellofamily'
IMAGE_URL = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
              '&type=3&__rnd=1546678278092'
# 百度人工智能key
APP_ID = '14303012'
API_KEY = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'

REDIS_URL = 'redis://127.0.0.1:6379/1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}

STATIC_ROOT = '/var/www/hellofamilyfront/buid/static'

ADMINS = MANAGERS = (
    'yuhao', 'jiang.yuhao0809@gmail.com',
)

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = 'hellofamily.club邮件报警'

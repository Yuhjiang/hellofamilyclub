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

MONGODB = {
    'url': 'mongo://localhost:27017'
}
IMAGE_DIR = '/home/hellofamily'
IMAGE_URL = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
              '&type=3&__rnd=1546678278092'

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

STATIC_ROOT = '/tmp/static'
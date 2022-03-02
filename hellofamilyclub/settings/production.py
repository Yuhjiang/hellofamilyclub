from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': os.environ.get('mysqlPassword'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': "hellofamily_db",
        'TEST': {
            'NAME': 'test_hellofamily_db',
        }
    }
}
ALLOWED_HOSTS = ['hellofamily.club']

# 百度人工智能key
APP_ID = '14303012'
API_KEY = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'
APP_GROUP_ID = 'Hello_Project'

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = 'hellofamily.club邮件报警'


# CELERY配置
CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_SERIALIZER = 'json'


# Websocket设置
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        }
    }
}

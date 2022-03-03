"""
识别未未识别过的图片
"""
import logging

from django.core.management.base import BaseCommand

from pictures.models import Picture
from pictures.service import RecognizeService

LOG = logging.getLogger(__name__)


def picture_recognize():
    LOG.info('开始人脸识别')
    # 获取最近的100张未识别的照片
    pictures = Picture.objects.filter(recognized=False).order_by('-id')[
               :100]
    service = RecognizeService(pictures)
    service.recognize_all()
    LOG.info('人脸识别完成')


class Command(BaseCommand):
    help = '微博爬虫脚本'

    def handle(self, *args, **options):
        picture_recognize()

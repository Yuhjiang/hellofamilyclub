from django.conf import settings
from django.core.management.base import BaseCommand
import logging
from pictures.service import HelloProjectHomePageCrawler

LOG = logging.getLogger(__name__)


def save_homepage_picture():
    LOG.info('获取官网首页滚动图片')
    service = HelloProjectHomePageCrawler(proxy=settings.REQUESTS_PROXY)
    service.save_homepage_pictures()


class Command(BaseCommand):
    help = '爬虫官网主页的内容'

    def handle(self, *args, **options):
        save_homepage_picture()

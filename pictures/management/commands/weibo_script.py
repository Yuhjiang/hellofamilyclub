"""
从weibo爬取照片
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from pictures.service import WeiboCrawler
from utils.cache import cache_client
from utils.core.exceptions import WeiboFetchCookieError

LOG = logging.getLogger(__name__)


def weibo_script():
    crawler = WeiboCrawler(1, 20, save=True, download=False, interval=10)
    try:
        crawler.do_fetch()
    except WeiboFetchCookieError as e:
        LOG.warning("微博爬虫失败，请更新Cookie")
        crawler.save_pictures()
        if cache_client.setnx(crawler.ALERT_EMAIL_KEY, 1):
            send_mail('Hellofamily微博爬虫失败', e.detail,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=['jiang.yuhao0809@gmail.com'])


class Command(BaseCommand):
    help = '微博爬虫脚本'

    def handle(self, *args, **options):
        weibo_script()

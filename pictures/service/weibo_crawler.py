import logging
from pictures.models import Cookie
import requests
from django.conf import settings


LOG = logging.getLogger(__name__)


class WeiboCrawler(object):
    def __init__(self, start: int, end: int, save: bool = False,
                 download: bool = False):
        """
        微博照片爬虫服务
        :param start: 开始爬虫页面
        :param end: 结束爬虫页面
        :param save: 是否保存到数据库
        :param download: 是否下载到本地
        """
        self.start = start
        self.end = end
        self.save = save
        self.download = download
        _cookie = Cookie.objects.get(id=1)
        self._cookie = _cookie

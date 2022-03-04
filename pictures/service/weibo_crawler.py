import json
import logging
import os
import time
from typing import List

import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from hellofamilyclub.utils.utils import download_picture
from pictures.models import Cookie
from pictures.models import Picture
from utils.core.exceptions import WeiboFetchCookieError

LOG = logging.getLogger(__name__)


class WeiboCrawler(object):
    ALERT_EMAIL_KEY = 'weibo:crawler:alert:'

    def __init__(self, start: int, end: int, save: bool = False,
                 download: bool = False, interval: int = 60,
                 skip: bool = True):
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
        self.pic_to_save: List[Picture] = []
        self.interval = interval
        self.skip = skip    # 是否跳过已经爬取过的
        self.stop = False

    def stop_fetch(self) -> bool:
        if self.skip:
            self.stop = True
        return self.stop

    def should_stop_fetch(self):
        return self.stop

    def do_fetch(self):
        logging.info('开始爬取微博照片')
        for page in range(self.start, self.end + 1):
            data = self.get_one_page(page)
            self.process_pic_list(data)
            time.sleep(self.interval)
            if self.should_stop_fetch():
                LOG.info('获取到重复的图片，停止爬虫')
                break
        self.save_pictures()
        logging.info('结束爬取微博照片')

    def get_one_page(self, page: int) -> List:
        url = settings.IMAGE_URL.format(page)
        res = requests.get(url, headers={
            'User-Agent': settings.USER_AGENT,
            'Cookie': self._cookie.cookie,
        })
        try:
            data = res.json()
            return data['data']['photo_list']
        except json.JSONDecodeError:
            logging.error('cookie失效', res.text[:100])
            raise WeiboFetchCookieError(res.text)

    def process_pic_list(self, data: List):
        for d in data:
            try:
                pic = Picture.objects.get(pic_id=d['photo_id'])
                if self.stop_fetch():
                    return
            except Picture.DoesNotExist:
                timestamp = d['timestamp']
                date_time = datetime.fromtimestamp(timestamp)
                pic = Picture(
                    pic_id=d['photo_id'],
                    name=d['pic_name'],
                    url=d['pic_host'] + '/mw690/' + d['pic_name'],
                    mem_count=0,
                    create_time=date_time.astimezone(timezone.utc),
                    create_date=date_time.date(),
                )
                if self.save:
                    self.pic_to_save.append(pic)
            if self.download:
                download_picture(pic.url, os.path.join(settings.IMAGE_DIR, str(
                    timezone.now().date())), pic.name, save=True)
                pic.download = True

    def save_pictures(self):
        Picture.objects.bulk_create(self.pic_to_save)

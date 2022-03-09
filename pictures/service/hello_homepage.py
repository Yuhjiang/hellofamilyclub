"""
hello project 主页图片爬虫
"""
from typing import List

import requests
from bs4 import BeautifulSoup

from pictures.models import CarouselPicture
from django.db import transaction


class HelloProjectHomePageCrawler(object):
    def __init__(self, official_site='http://www.helloproject.com', proxy=None,
                 timeout=5):
        self.official_site = official_site
        self.proxy = proxy
        self.timeout = timeout

    def get_homepage_pictures(self) -> List[CarouselPicture]:
        """
        获取主页的滚动图片
        """
        text = requests.get(self.official_site, proxies=self.proxy,
                            timeout=5).text
        bs = BeautifulSoup(text, 'html.parser')
        all_img = bs.select('#top_photo > ul > li > a > img')
        pictures_list = []
        for img in all_img:
            pictures_list.append(
                CarouselPicture(name=img.get('alt'), image=img.get('src'))
            )
        return pictures_list

    @transaction.atomic
    def save_homepage_pictures(self) -> List[CarouselPicture]:
        """
        获取主页滚动图片并保存
        """
        data = self.get_homepage_pictures()
        CarouselPicture.objects.update(status=CarouselPicture.STATUS_DELETE)
        for d in data:
            if CarouselPicture.objects.filter(name=d.name).exists():
                CarouselPicture.objects.filter(name=d.name).update(
                    status=CarouselPicture.STATUS_NORMAL)
            else:
                d.save()
        return data

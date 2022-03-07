import base64
import logging
import time
from typing import List, Dict

import requests

from pictures.models import Picture, Member
from pictures.service import aip_service
from utils.cache import cache_client

LOG = logging.getLogger(__name__)


class RecognizeService(object):
    RECOGNIZE_ERROR_KEY = 'recognize:error:pic:'
    ERROR_TIMEOUT = 60 * 60 * 24

    def __init__(self, queryset, interval=0.5):
        self.pictures: List[Picture] = list(queryset)
        self.member_cache: Dict[str, int] = {}
        self.interval = interval

    @classmethod
    def error_key(cls, pic_id: str):
        return cls.RECOGNIZE_ERROR_KEY + pic_id

    def set_error_cache(self, pic_id: str, err_msg: str):
        cache_client.setex(self.error_key(pic_id), self.ERROR_TIMEOUT, err_msg)

    def get_error_cache(self, pic_id: str):
        return cache_client.get(self.error_key(pic_id))

    def recognize_all(self):
        for pic in self.pictures:
            if self.get_error_cache(pic.pic_id):
                continue
            try:
                member_ids = self.recognize(pic)
                pic.set_members(member_ids)
                time.sleep(0.5)
            except Exception as e:
                LOG.error('人脸识别失败, 异常内容: {}'.format(e))

    def recognize(self, pic: Picture) -> List[int]:
        ids = []
        resp = requests.get(pic.url)
        image = base64.b64encode(resp.content).decode('utf-8')
        resp = aip_service.multi_search(image)
        if resp['error_code'] != 0:
            LOG.warning(f'图像识别失败, picture_id={pic.id}, url={pic.url}')
            LOG.warning(resp)
            self.set_error_cache(pic.pic_id, resp.get('error_msg', '识别失败'))
            return []
        face_list = resp['result']['face_list']
        for face in face_list:
            if not face['user_list']:
                continue
            name_en = face['user_list'][0]['user_id']
            _id = self.member_cache.get(name_en)
            if _id:
                ids.append(_id)
            else:
                try:
                    m = Member.objects.get(name_en=name_en)
                    self.member_cache[name_en] = m.id
                    ids.append(m.id)
                except Member.DoesNotExist:
                    pass
        return ids

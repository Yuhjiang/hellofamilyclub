import base64
import logging
import time
from typing import List, Dict

import requests

from pictures.models import Picture, Member
from pictures.service import aip_service

LOG = logging.getLogger(__name__)


class RecognizeService(object):
    def __init__(self, queryset, interval=0.5):
        self.pictures = list(queryset)
        self.member_cache: Dict[str, int] = {}
        self.interval = interval

    def recognize_all(self):
        for pic in self.pictures:
            member_ids = self.recognize(pic)
            pic.set_members(member_ids)
            time.sleep(0.5)

    def recognize(self, pic: Picture) -> List[int]:
        ids = []
        resp = requests.get(pic.url)
        image = base64.b64encode(resp.content).decode('utf-8')
        resp = aip_service.multi_search(image)
        if resp['error_code'] != 0:
            LOG.warning(f'图像识别失败, picture_id={pic.id}, url={pic.url}')
            LOG.warning(resp)
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

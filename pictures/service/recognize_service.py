from pictures.models import Picture, Member
from pictures.service import aip_service
import requests
import base64
import logging
from typing import List, Dict

LOG = logging.getLogger(__name__)


class RecognizeService(object):
    def __init__(self, redo=False):
        queryset = Picture.objects.filter()
        if not redo:
            queryset = queryset.filter(recognized=False)
        self.pictures = list(queryset)
        self.member_cache: Dict[str, int] = {}

    def recognize_all(self):
        for pic in self.pictures:
            member_ids = self.recognize(pic)
            pic.set_members(member_ids)

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


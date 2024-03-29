import logging

from aip import AipFace
from django.conf import settings

LOG = logging.getLogger(__name__)


class AipService(object):
    def __init__(self, group_id: str):
        self.group_id = group_id
        self.client = AipFace(settings.APP_ID, settings.API_KEY,
                              settings.SECRET_KEY)

    def add_face(self, image: bytes, member: str) -> str:
        """
        注册人脸
        :param image: base64格式的图片
        :param member: 成员名字，默认是name_en
        :return:
        {'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 1325694738,
        'timestamp': 1646050925, 'cached': 0,
        'result': {'face_token': 'ec0a51673869492dd1b667dc8a0c2415',
        'location': {'left': 80.33, 'top': 68.65, 'width': 69, 'height': 69,
         'rotation': -1}}}
        """
        r = self.client.addUser(str(image), 'BASE64', self.group_id, member)
        if r['error_code'] == 0:
            return r['result']['face_token']
        else:
            LOG.warning('人脸注册失败, {}'.format(r))
            return ''

    def delete_face(self, member: str, face_token: str) -> bool:
        """
        删除已经注册的人脸
        :param member: 成员名字
        :param face_token: 注册ID
        """
        r = self.client.faceDelete(member, self.group_id, face_token)
        return r['error_code'] == 0

    def multi_search(self, image: bytes, max_face_num = 10, match_threshold=70,
                     max_user_num=1):
        options = dict(
            max_face_num=max_face_num,
            match_threshold=match_threshold,
            max_user_num=max_user_num,
        )
        response = self.client.multiSearch(image, 'BASE64', self.group_id,
                                           options)
        return response

    def get_face_list(self, name_en: str):
        resp = self.client.faceGetlist(name_en, self.group_id)
        if resp['error_code'] == 0:
            return resp['result']['face_list']
        else:
            return []

    def get_client(self) -> AipFace:
        return self.client


aip_service = AipService(settings.APP_GROUP_ID)

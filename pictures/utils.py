import base64
from typing import Optional

import requests

from pictures.models import Member, MemberFace
from pictures.service import aip_service
from django.conf import settings


def add_face_for_member(url: str, member: Member) -> Optional[MemberFace]:
    """
    :param url: 人脸图片地址
    :param member: 成员
    :return:
    """
    resp = requests.get(url, proxies=settings.REQUESTS_PROXY)
    picture = resp.content
    picture = base64.b64encode(picture).decode('utf-8')
    face_id = aip_service.add_face(picture, member.name_en)
    if not face_id:
        return None
    else:
        return MemberFace.objects.create(member=member, face_id=face_id,
                                         url=url)

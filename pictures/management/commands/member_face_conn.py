import time

from django.core.management.base import BaseCommand

from pictures.models import Member, MemberFace
from pictures.service import aip_service


class Command(BaseCommand):
    help = '绑定百度云上已有的人脸到数据库'

    def handle(self, *args, **options):
        members = Member.objects.filter()
        for m in members:
            face_list = aip_service.get_face_list(m.name_en)
            for face in face_list:
                face_id = face['face_token']
                if MemberFace.objects.filter(face_id=face_id).exists():
                    continue
                MemberFace.objects.create(member=m, face_id=face_id,
                                          url='')
                # print(m.name_en, m.name_jp, face_id)
            time.sleep(0.5)

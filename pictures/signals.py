from django.db.models.signals import pre_delete
from django.dispatch import receiver
from pictures.models import MemberFace
from pictures.service import aip_service


@receiver(pre_delete, sender=MemberFace)
def delete_member_face(sender, instance: MemberFace, **kwargs):
    """
    删除人脸后，删除百度云上的注册人脸
    """
    aip_service.delete_face(instance.member.name_en, instance.face_id)

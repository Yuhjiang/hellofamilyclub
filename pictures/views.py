from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from aip import AipFace

from .models import Member

APP_ID = '14303012'
API_KEK = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'


client = AipFace(APP_ID, API_KEK, SECRET_KEY)


class MemberFace(APIView):
    groupId = 'Hello_Project'

    def post(self, request):
        """
        注册人脸
        :param request:
        :return:
        """
        body = request.POST
        try:
            member = Member.objects.get(id=body.get('member_id'))
        except Member.DoesNotExist:
            return Response({'status': 'failed', 'message': '未找到成员'})
        user_id = member.name_en

        client.addUser(image=body.get('image'),
                       image_type=body.get('imageType'), group_id=self.groupId,
                       user_id=user_id)
        return Response({'status': 'success', 'message': '注册成功'})

    def get(self, request):
        """
        获取人脸
        :param request:
        :return:
        """
        query = request.GET
        try:
            member = Member.objects.get(id=query.get('member_id'))
        except Member.DoesNotExist:
            return Response({'status': 'failed', 'message': '未找到成员'})
        user_id = member.name_en

        faces = client.faceGetlist(user_id=user_id, group_id=self.groupId)

        return Response({'status': 'succeed', 'message': '成功获取人脸',
                         'data': faces})

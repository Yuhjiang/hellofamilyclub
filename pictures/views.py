from django.shortcuts import render, get_object_or_404, reverse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from aip import AipFace

from .models import Member, Group
from .forms import MemberForm
from .service import mongo_db

APP_ID = '14303012'
API_KEK = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = 'VxKOFYYdvvRuk4MGrlyxlg6asArkRUlR'


client = AipFace(APP_ID, API_KEK, SECRET_KEY)


class BaseView(View):
    @staticmethod
    def get_context_data(request):
        groups = Group.get_all()

        return {'groups': groups}


class MemberFace(BaseView):
    def get(self, request):
        form = MemberForm
        context = {
            'form': form,
        }
        context.update(self.get_context_data(request))
        return render(request, "pictures/add.html", context=context)


class MemberFaceIndex(BaseView):
    def get(self, request):
        images = list(mongo_db['images'].find().
                      limit(20).skip(0))
        context = {
            'images': images,
        }
        context.update(self.get_context_data(request))
        return render(request, 'pictures/index.html', context=context)



class MemberFaceAPI(APIView):
    groupId = 'Hello_Project'

    def post(self, request):
        """
        注册人脸
        :param request:
        :return:
        """
        body = request.POST
        try:
            member = Member.objects.get(id=body.get('member'))
        except Member.DoesNotExist:
            return Response({'status': 'failed', 'message': '未找到成员'})
        user_id = member.name_en
        if body.get('image_url'):
            image = body['image_url']
            image_type = 'URL'
        else:
            image = body['image_file']
            image_type = 'BASE64'
        client.addUser(image=image, image_type=image_type,
                       group_id=self.groupId, user_id=user_id)
        return Response({'status': 'success', 'message': '注册成功'})

    def get(self, request):
        """
        获取人脸
        :param request:
        :return:
        """
        query = request.GET
        try:
            member = Member.objects.get(id=query.get('member'))
        except Member.DoesNotExist:
            return Response({'status': 'failed', 'message': '未找到成员'})
        user_id = member.name_en

        faces = client.faceGetlist(user_id=user_id, group_id=self.groupId)

        return Response({'status': 'succeed', 'message': '成功获取人脸',
                         'data': faces})

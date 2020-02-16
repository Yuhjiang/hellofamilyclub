from django.shortcuts import render, get_object_or_404, reverse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from aip import AipFace

from .models import Member, Group
from .forms import MemberForm
from .service import mongo_db
from .service.config import APP_ID, API_KEY, SECRET_KEY
from config.models import SideBar
from hellofamilyclub.utils.utils import page_limit_skip


client = AipFace(APP_ID, API_KEY, SECRET_KEY)


class BaseView(View):
    @staticmethod
    def get_context_data(request):
        groups = Group.get_all()
        if request.user.is_authenticated:
            sidebars = SideBar.get_all().filter(owner=request.user)
        else:
            sidebars = SideBar.objects.none()
        return {'groups': groups, 'sidebars': sidebars}


class GroupProfile(BaseView):
    """
    显示Hello！Project所有组合，时间线
    """
    def get(self, request):
        groups = Group.objects.filter().order_by('created_time')
        context = {
            'groups_ordered': groups
        }
        context.update(self.get_context_data(request))
        return render(request, 'pictures/profile.html', context=context)


class MemberFace(BaseView):
    def get(self, request):
        form = MemberForm
        context = {
            'form': form,
        }
        context.update(self.get_context_data(request))
        return render(request, 'pictures/add.html', context=context)


class MemberFaceIndex(BaseView):
    def get(self, request):
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        limit, skip = page_limit_skip(page, limit)
        images = list(mongo_db['images'].find().limit(limit).skip(skip))
        count = mongo_db['images'].count()
        context = {
            'images': images,
            'current': page,
            'limit': limit,
            'count': count
        }
        context.update(self.get_context_data(request))
        return render(request, 'pictures/index.html', context=context)


class MemberFaceList(APIView):
    def get(self, request):
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        limit, skip = page_limit_skip(page, limit)
        images = list(mongo_db['images'].find({}, {'_id': 0}).
                      limit(limit).skip(skip))
        count = mongo_db['images'].count()
        result = {
            'images': images,
            'current': page,
            'limit': limit,
            'count': count
        }
        return Response(result)


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

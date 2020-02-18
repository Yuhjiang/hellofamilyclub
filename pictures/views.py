from datetime import datetime

from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from aip import AipFace

from .models import Member, Group
from .forms import MemberForm
from .service.config import mongo_db
from config.models import SideBar
from hellofamilyclub.utils.utils import page_limit_skip
from hellofamilyclub.utils.decorators import admin_required


APP_ID = settings.APP_ID
API_KEY = settings.API_KEY
SECRET_KEY = settings.SECRET_KEY
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


"""
后端渲染页面
"""


class BaseView(View):
    @staticmethod
    def get_context_data(request):
        groups = Group.get_all()
        if request.user.is_authenticated:
            sidebars = SideBar.get_all().filter(owner=request.user)
        else:
            sidebars = SideBar.objects.none()
        members = Member.objects.filter().only('id', 'name')
        return {'groups': groups, 'sidebars': sidebars, 'members': members}


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
    @method_decorator(admin_required)
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
            'count': count,
        }
        context.update(self.get_context_data(request))
        return render(request, 'pictures/index.html', context=context)


"""
Restful API
"""


class CookieApi(APIView):
    @staticmethod
    def post(request):
        body = request.POST
        if body.get('cookie'):
            current_time = datetime.now()
            result = mongo_db['cookie'].insert_one({
                'cookie': body['cookie'],
                'update_time': current_time,
            })
            return Response({'result': result.acknowledged,
                             'message': '成功更新Cookie'})
        else:
            return Response({
                'result': False,
                'message': 'Cookie更新失败'
            })


class MemberFaceList(APIView):
    @staticmethod
    def all_member():
        return {}

    @staticmethod
    def single_member(query):
        return {'members.id': int(query['member1'])}

    @staticmethod
    def double_member(query):
        member_ids = [int(query['member1']), int(query['member2'])]
        return {'members.id': {'$in': member_ids}, 'size': 2}

    def get(self, request):
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        if request.GET.get('member2') and int(request.GET['member2']):
            query = self.double_member(request.GET)
        elif request.GET.get('member1') and int(request.GET['member1']):
            query = self.single_member(request.GET)
        else:
            query = self.all_member()
        limit, skip = page_limit_skip(page, limit)
        images = list(mongo_db['images'].find(query, {'_id': 0}).
                      limit(limit).skip(skip))

        count = mongo_db['images'].count(query)
        result = {
            'images': images,
            'current': page,
            'limit': limit,
            'count': count
        }
        return Response(result)


class MemberFaceListDate(APIView):
    def get(self, request):
        member_id = request.GET.get('member1')
        images = list(mongo_db['images'].aggregate([
            {'$match': {'members.id': int(member_id)}},
            {'$group': {
                '_id': '$created_date',
                'pictures': {'$push': {'name': '$name', 'url': '$url'}},
                'date': {'$first': 1}
            }},
            {'$sort': {'_id': -1}},
        ]))
        for image in images:
            image['date'] = image['_id'].strftime('%Y年%m月%d日')
        result = {
            'images': images
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

import requests
import json
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from pictures import serializers
from pictures.models import Cookie
from utils.core.permissions import AdminPermission


def get_weibo_response(cookie: str) -> requests.Response:
    resp = requests.get(settings.IMAGE_URL.format(1),
                        headers={'User-Agent': settings.USER_AGENT,
                                 'Cookie': cookie})
    return resp


class WeiboCookieView(GenericAPIView):
    """
    更新weibo爬虫的cookie
    """
    permission_classes = (AdminPermission,)
    serializer_class = serializers.CookieSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cookie_str = serializer.validated_data['cookie']
        resp = get_weibo_response(cookie_str)
        try:
            data = resp.json()
            if data['result']:
                c, _ = Cookie.objects.get_or_create(id=1)
                c.cookie = cookie_str
                c.save()
                return Response({'status': 200, 'errMsg': 'Cookie更新成功'})
            else:
                return Response({'status': 500, 'errMsg': 'Cookie更新失败'})
        except json.JSONDecodeError:
            return Response({'status': 500, 'errMsg': 'Cookie更新失败'})

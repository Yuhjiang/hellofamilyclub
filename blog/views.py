import json

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Picture


@api_view(['POST'])
def upload_picture(request):
    file = request.FILES['content']

    instance = Picture(name=file.name, content=file, owner_id=2)
    instance.save()
    return Response({'status': 200, 'data': {'url': instance.content.url}})

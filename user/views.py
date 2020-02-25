import time
import json

from django.shortcuts import render
from django.views import View

from dwebsocket.decorators import accept_websocket, require_websocket


@accept_websocket
def test_websocket(request):
    if request.is_webosocket():
        while 1:
            time.sleep(1)
            dit = {
                'time': time.strftime('%Y.%m.%d %H:%M:%S',
                                      time.localtime(time.time()))
            }
            request.websocket.send(json.dumps(dit))

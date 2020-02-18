import os

import django
from django.conf import settings

from pymongo import MongoClient


profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))
django.setup()


User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) ' \
             'Chrome/22.0.1207.1 Safari/537.1'
Cookie = 'SINAGLOBAL=4041173730931.1226.1574765168991; UOR=,,login.sina.com.cn; login_sid_t=4e328565e54d71f19e4112d5e3a7dfa3; cross_origin_proto=SSL; _s_tentry=-; Apache=1276732691318.9958.1580023421915; ULV=1580023421921:7:2:1:1276732691318.9958.1580023421915:1577964495769; SSOLoginState=1580709100; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF5SSkZaQym.hgJRur5llA05JpX5KMhUgL.Fo2Ne0MES0qESKM2dJLoIpBLxKnLBKeLBonLxK-LBKBL129KKntt; ALF=1613305910; SCF=ApNwV7RyD2LbNpA2Wx55Si5g_kv1RJZBow0bNnoFImEu_pMF1uhZQe3mkx_DrOQp4_4GTJRguwV1oLZJjtG9o78.; SUB=_2A25zQ5ToDeRhGedJ6FUT9yjOzjuIHXVQOIEgrDV8PUNbmtAfLRXYkW9NVjU2Yi99NkC2_CU1f0gcEwQk1d3WRHFP; SUHB=0k1TuQQ3Jcos9k'
headers = {'User-Agent': User_Agent, 'Cookie': Cookie}
MONGODB = settings.MONGODB
IMAGE_DIR = settings.IMAGE_DIR
image_url = settings.IMAGE_URL

db_client = MongoClient(MONGODB['url'])
mongo_db = db_client['hellofamily']

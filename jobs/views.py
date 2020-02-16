import os
import sys
import django
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from pictures.service.weibo import fetch_weibo_pictures
from pictures.service.recognize import recognize_all_pictures
from pictures.service import db_client


logging.basicConfig(filename='/Users/yuhao/log/job.log', filemode='a')

logging.getLogger('apscheduler').setLevel(logging.DEBUG)


jobstores = {
    'mongo': MongoDBJobStore(collection='job', database='hellofamily',
                             client=db_client),
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 10,
}

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors,
                              job_defaults=job_defaults)


scheduler.add_job(fetch_weibo_pictures, 'interval', hours=1,
                  replace_existing=True, id='fetch_weibo_pictures',
                  jobstore='mongo', max_instances=1)
scheduler.add_job(recognize_all_pictures, 'interval', hours=1,
                  replace_existing=True, id='recognize_all_pictures',
                  jobstore='mongo', max_instances=1)

scheduler.start()

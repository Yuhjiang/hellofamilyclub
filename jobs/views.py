import logging

from apscheduler import events
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.db import connections

from pictures.management.commands import picture_recognize, weibo_script

LOG = logging.getLogger(__name__)
jobstores = {
    'default': RedisJobStore(jobs_key='hellofamily_dispatched_jobs',
                             run_times_key='hellofamily_dispatch_running',
                             host=settings.REDIS_HOST,
                             port=settings.REDIS_PORT)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5),
}

job_defaults = {
    'coalesce': False,
    'max_instances': 10,
}


def close_connections(event):
    LOG.info(f'{event.job_id}:关闭定时任务数据库连接')
    connections.close_all()


scheduler = BlockingScheduler(jobstores=jobstores, executors=executors,
                              job_defaults=job_defaults)
scheduler.add_listener(close_connections,
                       events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)

scheduler.add_job(weibo_script, trigger='cron', hour='*/1',
                  replace_existing=True, id='fetch_weibo_pictures',
                  max_instances=1)
scheduler.add_job(picture_recognize, trigger='cron', minute='*/1',
                  replace_existing=True, id='recognize_all_pictures',
                  max_instances=1)

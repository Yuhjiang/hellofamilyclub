from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings

from pictures.management.commands import picture_recognize, weibo_script

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

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors,
                              job_defaults=job_defaults)

scheduler.add_job(weibo_script, trigger='cron', hour='*/1',
                  replace_existing=True, id='fetch_weibo_pictures',
                  max_instances=1)
scheduler.add_job(picture_recognize, trigger='cron', hour='*/1',
                  replace_existing=True, id='recognize_all_pictures',
                  max_instances=1)

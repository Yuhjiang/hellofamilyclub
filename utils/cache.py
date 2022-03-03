import redis
from django.conf import settings

cache_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

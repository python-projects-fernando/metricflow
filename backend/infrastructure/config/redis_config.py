import os
import redis
from backend.infrastructure.config.settings import settings

def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=False,
    )


# redis_client = get_redis_client()
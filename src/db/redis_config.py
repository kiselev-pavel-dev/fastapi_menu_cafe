import aioredis

from src.settings import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB

if not settings.docker_mode:
    REDIS_HOST = "localhost"

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


async def get_cache():
    cache = aioredis.from_url(REDIS_URL)
    try:
        yield cache
    finally:
        await cache.close()

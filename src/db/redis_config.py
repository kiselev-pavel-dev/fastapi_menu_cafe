import redis

from src.settings import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB

if not settings.docker_mode:
    REDIS_HOST = "localhost"

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)
redis_cache = redis.Redis(connection_pool=pool)

import json
from typing import Any, List

from fastapi.encoders import jsonable_encoder

from src.db.redis_config import redis_cache


class RedisCache:

    def get(self, key: str) -> Any | None:
        data = redis_cache.get(name=key)
        if not data:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any) -> None:
        data = json.dumps(jsonable_encoder(value))
        redis_cache.set(name=key, value=data)

    def delete_one(self, keys: List[str] | str) -> None:
        redis_cache.delete(*keys)

    def delete_all(self, key: str) -> None:
        keys = redis_cache.keys(f"{key}*")
        if keys:
            redis_cache.delete(*keys)


cache = RedisCache()

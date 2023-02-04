import json
from typing import Any

from fastapi.encoders import jsonable_encoder


class RedisCache:
    def __init__(self, cache: Any) -> None:
        self.cache = cache

    async def get(self, key: str) -> Any | None:
        data = await self.cache.get(key)
        if not data:
            return None
        return json.loads(data)

    async def set(self, key: str, value: Any) -> None:
        data = json.dumps(jsonable_encoder(value))
        await self.cache.set(key, data)

    async def delete_one(self, keys: list[str] | str) -> None:
        await self.cache.delete(*keys)

    async def delete_all(self, key: str) -> None:
        keys = await self.cache.keys(f"{key}*")
        if keys:
            await self.cache.delete(*keys)

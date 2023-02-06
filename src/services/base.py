from typing import Any

from src.crud.cache import RedisCache


class BaseService:
    def __init__(self, crud: Any, cache: RedisCache) -> None:
        self.crud = crud
        self.cache = cache

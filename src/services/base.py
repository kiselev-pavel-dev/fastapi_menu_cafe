from typing import Any


class BaseService:
    def __init__(self, crud: Any, cache: Any) -> None:
        self.crud = crud
        self.cache = cache

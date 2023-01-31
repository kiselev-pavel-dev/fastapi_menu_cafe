from typing import Any


class BaseService:
    def __init__(self, crud: Any) -> None:
        self.crud = crud

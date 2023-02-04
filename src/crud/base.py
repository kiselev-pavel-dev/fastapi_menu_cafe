from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

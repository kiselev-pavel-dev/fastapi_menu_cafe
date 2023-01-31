from sqlalchemy.orm import Session


class BaseCrud:
    def __init__(self, session: Session) -> None:
        self.session = session

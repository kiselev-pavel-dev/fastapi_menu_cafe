from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import Base
from src.settings import settings

POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
DB_HOST = settings.DB_HOST
DB_NAME = settings.POSTGRES_DB
DB_PORT = settings.DB_PORT

if not settings.docker_mode:
    DB_HOST = "localhost"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

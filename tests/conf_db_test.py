import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from src.db.database import get_db
from src.main import app
from src.models.models import Base
from src.settings import settings

POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
DB_HOST = "db_tests"
DB_NAME = settings.POSTGRES_DB_TESTS
DB_PORT = settings.DB_PORT

if not settings.docker_mode:
    DB_HOST = "localhost"

REDIS_HOST = "redis_tests"
REDIS_PORT = 6379
REDIS_DB = 1

if not settings.docker_mode:
    REDIS_HOST = "localhost"

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)
redis_cache = redis.Redis(connection_pool=pool)

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine,
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

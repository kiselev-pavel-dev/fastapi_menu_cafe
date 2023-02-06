import asyncio

import aioredis
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from src.crud.crud import DishCrud, MenuCrud, SubmenuCrud
from src.db.database import get_session
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

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,
)
SessionLocalTest = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_session() -> AsyncSession:
    async with SessionLocalTest() as session:
        yield session


async def get_cache_test():
    cache = aioredis.from_url(REDIS_URL)
    try:
        yield cache
    finally:
        await cache.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function")
async def db(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    db = AsyncSession(bind=connection)

    yield db

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db):
    app.dependency_overrides[get_session] = lambda: db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture()
async def menu_data():
    return {"id": 1, "title": "Тестовое меню", "description": "Описание тестового меню"}


@pytest_asyncio.fixture()
async def submenu_data():
    return {
        "id": 1,
        "title": "Тестовое подменю 1",
        "description": "Описание тестового подменю 1",
    }


@pytest_asyncio.fixture()
async def dish_data():
    return {
        "id": 1,
        "title": "Тестовое блюдо 1",
        "description": "Описание тестового блюда 1",
        "price": "12.12",
    }


@pytest_asyncio.fixture
async def create_menu(db, menu_data):
    menu = await MenuCrud(session=db).create_menu(menu_data)
    return await MenuCrud(session=db).get_menu(menu.id)


@pytest_asyncio.fixture
async def create_submenu(db, submenu_data):
    submenu = await SubmenuCrud(session=db).create_submenu(submenu_data, 1)
    return await SubmenuCrud(session=db).get_submenu(submenu.id)


@pytest_asyncio.fixture
async def create_dish(db, dish_data):
    dish = await DishCrud(session=db).create_dish(dish_data, 1)
    return await DishCrud(session=db).get_dish(dish.id)

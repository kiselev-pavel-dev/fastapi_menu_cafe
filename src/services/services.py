import json

import aiofiles  # type: ignore
from aioredis import Redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from src.celery.tasks import app_celery
from src.crud.cache import RedisCache
from src.crud.crud import DishCrud, MenuCrud, SubmenuCrud, TestDataCrud
from src.db.database import get_session
from src.db.redis_config import get_cache
from src.schemas.schemas import (
    Dish,
    DishCreate,
    DishUpdate,
    Menu,
    MenuCreate,
    MenuUpdate,
    SubMenu,
    SubMenuCreate,
    SubMenuUpdate,
)
from src.services.base import BaseService


class MenuServices(BaseService):
    async def get_list_menus(self) -> list[Menu]:
        redis_key = "menu:list"
        menus = await self.cache.get(redis_key)
        if not menus:
            res = await self.crud.get_menu_list()
            menus = []
            for item in res:
                menu = dict()
                submenus_count = await self.crud.get_submenus_count(id=item.id)
                dishes_count = await self.crud.get_dishes_count(id=item.id)
                menu["id"] = item.id
                menu["title"] = item.title
                menu["description"] = item.description
                menu["submenus_count"] = submenus_count
                menu["dishes_count"] = dishes_count
                menus.append(menu)
            await self.cache.set(redis_key, menus)
        return menus

    async def get_menu(self, id: int) -> Menu:
        redis_key = f"menu:{id}"
        menu = await self.cache.get(redis_key)
        if not menu:
            menu = await self.crud.get_menu(id=id)
            self.menu_empty(not menu)
            menu = dict(menu)
            submenus_count = await self.crud.get_submenus_count(id=id)
            dishes_count = await self.crud.get_dishes_count(id=id)
            menu["submenus_count"] = submenus_count
            menu["dishes_count"] = dishes_count
            await self.cache.set(redis_key, menu)
        return menu

    async def create_menu(self, menu: MenuCreate) -> Menu:
        await self.cache.delete_one(["menu:list"])
        data = jsonable_encoder(menu)
        return await self.crud.create_menu(data)

    async def update_menu(self, id: int, menu: MenuUpdate) -> Menu:
        redis_key = [f"menu:{id}", "menu:list"]
        current_menu = await self.crud.get_menu(id=id)
        self.menu_empty(not current_menu)
        await self.cache.delete_one(redis_key)
        await self.crud.update_menu(id=id, title=menu.title, description=menu.description)
        return await self.get_menu(id=id)

    async def delete_menu(self, id: int) -> dict:
        redis_keys = [f"menu:{id}", "menu:list"]
        menu = await self.crud.get_menu(id=id)
        self.menu_empty(not menu)
        await self.crud.delete_menu(id=id)
        await self.cache.delete_one(redis_keys)
        await self.cache.delete_all(f"submenu:{id}:")
        await self.cache.delete_all(f"dish:{menu.id}:")
        return {"status": True, "message": "The menu has been deleted"}

    async def create_menu_excel_file(self) -> dict:
        data = await self.crud.get_all_data_from_menus_submenus_dishes()
        task = app_celery.send_task("create_excel", kwargs={"data": data})
        return {"task_id": task.id}

    async def get_menu_excel_file(self, id: str) -> dict:
        return FileResponse(
            path=f"/uploads/{id}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="Menu.xlsx",
        )

    def menu_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="menu not found",
            )


class SubmenuServices(BaseService):
    async def get_submenu(self, id: int, menu_id: int) -> SubMenu:
        redis_key = f"submenu:{menu_id}:{id}"
        submenu = await self.cache.get(redis_key)
        if not submenu:
            submenu = await self.crud.get_submenu(id=id)
            self.submenu_empty(not submenu)
            dishes_count = await self.crud.get_dishes_count(
                id=int(submenu.id),
            )
            submenu = dict(submenu)
            submenu["dishes_count"] = dishes_count
            await self.cache.set(key=redis_key, value=submenu)
        return submenu

    async def get_submenu_list(self, menu_id: int) -> list[SubMenu]:
        redis_key = f"submenu:{menu_id}:list"
        submenus = await self.cache.get(redis_key)
        if not submenus:
            result = await self.crud.get_submenu_list(menu_id=menu_id)
            submenus = []
            for item in result:
                submenu = dict()
                dishes_count = await self.crud.get_dishes_count(
                    id=int(item.id),
                )
                submenu["id"] = item.id
                submenu["title"] = item.title
                submenu["description"] = item.description
                submenu["dishes_count"] = dishes_count
                submenus.append(submenu)
            await self.cache.set(redis_key, submenus)
        return submenus

    async def create_submenu(
        self,
        submenu: SubMenuCreate,
        menu_id: int,
    ) -> SubMenu:
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
        ]
        await self.cache.delete_one(redis_keys)
        data = jsonable_encoder(submenu)
        return await self.crud.create_submenu(data, id=menu_id)

    async def update_submenu(
        self,
        id: int,
        menu_id: int,
        submenu: SubMenuUpdate,
    ) -> SubMenu:
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
            f"submenu:{menu_id}:{id}",
        ]
        current_submenu = await self.get_submenu(
            id=id,
            menu_id=menu_id,
        )
        self.submenu_empty(not current_submenu)
        await self.cache.delete_one(redis_keys)
        await self.crud.update_submenu(
            id=id,
            title=submenu.title,
            description=submenu.description,
        )
        return await self.get_submenu(id=id, menu_id=menu_id)

    async def delete_submenu(self, id: int, menu_id: int) -> dict:
        submenu = await self.crud.get_submenu(id)
        self.submenu_empty(not submenu)
        await self.crud.delete_submenu(id=id)
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
            f"submenu:{menu_id}:{id}",
        ]
        await self.cache.delete_one(redis_keys)
        return {"status": True, "message": "The submenu has been deleted"}

    def submenu_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )


class DishServices(BaseService):
    async def get_dish(
        self,
        id: int,
        menu_id: int,
        submenu_id: int,
    ) -> Dish:
        redis_key = f"dish:{menu_id}:{submenu_id}:{id}"
        dish = await self.cache.get(redis_key)
        if not dish:
            dish = await self.crud.get_dish(id=id)
            self.dish_empty(not dish)
            dish = dict(dish)
            await self.cache.set(key=redis_key, value=dish)
        return dish

    async def get_list_dishes(
        self,
        submenu_id: int,
        menu_id: int,
    ) -> list[Dish]:
        redis_key = f"dish:{menu_id}:{submenu_id}:list"
        dishes = await self.cache.get(redis_key)
        if not dishes:
            dishes = await self.crud.get_list_dish(id_submenu=submenu_id)
            await self.cache.set(key=redis_key, value=dishes)
        return dishes

    async def create_dish(
        self,
        submenu_id: int,
        menu_id: int,
        dish: DishCreate,
    ) -> Dish:
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
            f"submenu:{menu_id}:{submenu_id}",
        ]
        data = jsonable_encoder(dish)
        await self.cache.delete_one(redis_keys)
        return await self.crud.create_dish(data=data, id=submenu_id)

    async def update_dish(
        self,
        id: int,
        menu_id: int,
        submenu_id: int,
        dish: DishUpdate,
    ) -> Dish:
        current_dish = await self.get_dish(
            id=id,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
            f"submenu:{menu_id}:{submenu_id}",
            f"dish:{menu_id}:{submenu_id}:{id}",
            f"dish:{menu_id}:{submenu_id}:list",
        ]
        await self.cache.delete_one(redis_keys)
        self.dish_empty(not current_dish)
        await self.crud.update_dish(
            id=id,
            title=dish.title,
            description=dish.description,
            price=dish.price,
        )
        return await self.get_dish(id=id, menu_id=menu_id, submenu_id=submenu_id)

    async def delete_dish(
        self,
        id: int,
        menu_id: int,
        submenu_id: int,
    ) -> dict:
        redis_keys = [
            f"dish:{menu_id}:{submenu_id}:{id}",
            f"dish:{menu_id}:{submenu_id}:list",
        ]
        dish = await self.crud.get_dish(id=id)
        self.dish_empty(not dish)
        await self.crud.delete_dish(id=id)
        await self.cache.delete_one(redis_keys)
        return {"status": True, "message": "The dish has been deleted"}

    def dish_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="dish not found",
            )


class TestDataServices:
    def __init__(self, crud: TestDataCrud) -> None:
        self.crud = crud

    async def test_data_create(self) -> dict:
        await self.crud.delete_all_tables()
        async with aiofiles.open("test_data/menus.json", mode="r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)
        for item in data:
            menu_data = {
                "id": int(item["id"]),
                "title": item["title"],
                "description": item["description"],
            }
            await self.crud.create_menu(menu_data=menu_data)
            for item_submenu in item["submenu"]:
                submenu_data = {
                    "id": int(item_submenu["id"]),
                    "title": item_submenu["title"],
                    "description": item_submenu["description"],
                    "menu_id": int(item["id"]),
                }
                await self.crud.create_submenu(submenu_data=submenu_data)
                for item_dish in item_submenu["dishes"]:
                    dish_data = {
                        "id": int(item_dish["id"]),
                        "title": item_dish["title"],
                        "description": item_dish["description"],
                        "price": item_dish["price"],
                        "submenu_id": int(item_submenu["id"]),
                    }
                    await self.crud.create_dish(dish_data=dish_data)
        return {"status": True, "message": "Test data uploaded successfully!"}


async def menu_services(
    session: AsyncSession = Depends(get_session), cache: Redis = Depends(get_cache)
) -> MenuServices:
    crud = MenuCrud(session=session)
    cache = RedisCache(cache=cache)
    return MenuServices(crud=crud, cache=cache)


async def submenu_services(
    session: AsyncSession = Depends(get_session), cache: Redis = Depends(get_cache)
) -> SubmenuServices:
    crud = SubmenuCrud(session=session)
    cache = RedisCache(cache=cache)
    return SubmenuServices(crud=crud, cache=cache)


async def dish_services(
    session: AsyncSession = Depends(get_session), cache: Redis = Depends(get_cache)
) -> DishServices:
    crud = DishCrud(session=session)
    cache = RedisCache(cache=cache)
    return DishServices(crud=crud, cache=cache)


async def test_data_service(
    session: AsyncSession = Depends(get_session),
) -> TestDataServices:
    crud = TestDataCrud(session=session)
    return TestDataServices(crud=crud)

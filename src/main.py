from typing import List

from fastapi import FastAPI, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.db.redis_config import pool, redis
from src.schemas import schemas
from src.services.services import (
    dish_services, menu_services,
    submenu_services, MenuServices, SubmenuServices, DishServices,
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis.Redis(connection_pool=pool)


@app.get(
    "/api/v1/menus",
    response_model=List[schemas.Menu],
    summary="Список меню",
    description="Получение списка всех меню",
    status_code=HTTP_200_OK,
)
def list_menus(service: MenuServices = Depends(menu_services)):
    return service.get_list_menus()


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
    summary="Получить меню",
    description="Получение меню по его идентификатору",
    status_code=HTTP_200_OK,
)
def get_menu(menu_id: int, service: MenuServices = Depends(menu_services)):
    return service.get_menu(id=menu_id)


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    summary="Создать меню",
    description="Создание меню",
    status_code=HTTP_201_CREATED,
)
def create_menu(
    menu: schemas.MenuCreate,
    service: MenuServices = Depends(menu_services),
):
    return service.create_menu(menu=menu)


@app.patch(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
    summary="Обновить меню",
    description="Обновление меню",
    status_code=HTTP_200_OK,
)
def patch_menu(
    menu_id: int,
    menu: schemas.MenuUpdate,
    service: MenuServices = Depends(menu_services),
):
    return service.update_menu(id=menu_id, menu=menu)


@app.delete(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.MenuDelete,
    summary="Удалить меню",
    description="Удаление меню",
    status_code=HTTP_200_OK,
)
def delete_menu(menu_id: int, service: MenuServices = Depends(menu_services)):
    return service.delete_menu(id=menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[schemas.SubMenu],
    summary="Список подменю",
    description="Получение списка подменю определенного меню",
    status_code=HTTP_200_OK,
)
def list_submenus(menu_id: int, service: SubmenuServices = Depends(submenu_services)):
    return service.get_submenu_list(id=menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    summary="Получить подменю",
    description="Получение подменю по его идентификатору",
    status_code=HTTP_200_OK,
)
def get_submenu(
    submenu_id: int,
    menu_id: int,
    service: SubmenuServices = Depends(submenu_services),
):
    return service.get_submenu(
        id=submenu_id,
        menu_id=menu_id,
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.SubMenu,
    summary="Создать подменю",
    description="Создание подменю",
    status_code=HTTP_201_CREATED,
)
def create_submenu(
    menu_id: int,
    submenu: schemas.SubMenuCreate,
    service: SubmenuServices = Depends(submenu_services),
):
    return service.create_submenu(
        submenu=submenu,
        menu_id=menu_id,
    )


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenuDelete,
    summary="Удалить подменю",
    description="Удаление подменю",
    status_code=HTTP_200_OK,
)
def delete_submenu(
    submenu_id: int,
    service: SubmenuServices = Depends(submenu_services),
):
    return service.delete_submenu(id=submenu_id)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    summary="Обновить подменю",
    description="Обновление подменю",
    status_code=HTTP_200_OK,
)
def patch_submenu(
    submenu_id: int,
    menu_id: int,
    submenu: schemas.SubMenuUpdate,
    service: SubmenuServices = Depends(submenu_services),
):
    return service.update_submenu(
        id=submenu_id,
        menu_id=menu_id,
        submenu=submenu,
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[schemas.Dish],
    summary="Список блюд",
    description="Получение списка блюд",
    status_code=HTTP_200_OK,
)
def list_dishes(
    submenu_id: int,
    menu_id: int,
    service: DishServices = Depends(dish_services),
):
    return service.get_list_dishes(
        submenu_id=submenu_id,
        menu_id=menu_id,
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    summary="Получить блюдо",
    description="Получение блюда",
    status_code=HTTP_200_OK,
)
def get_dish(
    dish_id: int,
    menu_id: int,
    submenu_id: int,
    service: DishServices = Depends(dish_services),
):
    return service.get_dish(
        id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    summary="Создать блюдо",
    description="Создание блюда",
    status_code=HTTP_201_CREATED,
)
def create_dish(
    dish: schemas.DishCreate,
    submenu_id: int,
    menu_id: int,
    service: DishServices = Depends(dish_services),
):
    return service.create_dish(
        submenu_id=submenu_id,
        menu_id=menu_id,
        dish=dish,
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    summary="Обновить блюдо",
    description="Обновление блюда",
    status_code=HTTP_200_OK,
)
def patch_dish(
    dish_id,
    menu_id: int,
    submenu_id: int,
    dish: schemas.DishCreate,
    service: DishServices = Depends(dish_services),
):
    return service.update_dish(
        id=dish_id,
        dish=dish,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    description="Удаление блюда",
    summary="Удалить блюдо",
    response_model=schemas.DishDelete,
    status_code=HTTP_200_OK,
)
def delete_dish(
    dish_id: int,
    menu_id: int,
    submenu_id: int,
    service: DishServices = Depends(dish_services),
):
    return service.delete_dish(
        id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

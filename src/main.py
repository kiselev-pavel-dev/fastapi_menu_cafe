import aioredis
from fastapi import Depends, FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from src.db.database import init_db
from src.db.redis_config import REDIS_URL
from src.schemas import schemas
from src.services.services import (
    DishServices,
    MenuServices,
    SubmenuServices,
    TestDataServices,
    dish_services,
    menu_services,
    submenu_services,
    test_data_service,
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()
    aioredis.from_url(REDIS_URL)


@app.on_event("shutdown")
async def shutdown_event():
    cache = aioredis.from_url(REDIS_URL)
    await cache.flushall()


@app.get(
    "/api/v1/menus",
    response_model=list[schemas.Menu],
    summary="Список меню",
    description="Получение списка всех меню",
    status_code=HTTP_200_OK,
)
async def list_menus(service: MenuServices = Depends(menu_services)):
    return await service.get_list_menus()


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
    summary="Получить меню",
    description="Получение меню по его идентификатору",
    status_code=HTTP_200_OK,
)
async def get_menu(menu_id: int, service: MenuServices = Depends(menu_services)):
    return await service.get_menu(id=menu_id)


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    summary="Создать меню",
    description="Создание меню",
    status_code=HTTP_201_CREATED,
)
async def create_menu(
    menu: schemas.MenuCreate,
    service: MenuServices = Depends(menu_services),
):
    return await service.create_menu(menu=menu)


@app.patch(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
    summary="Обновить меню",
    description="Обновление меню",
    status_code=HTTP_200_OK,
)
async def patch_menu(
    menu_id: int,
    menu: schemas.MenuUpdate,
    service: MenuServices = Depends(menu_services),
):
    return await service.update_menu(id=menu_id, menu=menu)


@app.delete(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.MenuDelete,
    summary="Удалить меню",
    description="Удаление меню",
    status_code=HTTP_200_OK,
)
async def delete_menu(
    menu_id: int,
    service: MenuServices = Depends(menu_services),
):
    return await service.delete_menu(id=menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=list[schemas.SubMenu],
    summary="Список подменю",
    description="Получение списка подменю определенного меню",
    status_code=HTTP_200_OK,
)
async def list_submenus(
    menu_id: int,
    service: SubmenuServices = Depends(submenu_services),
):
    return await service.get_submenu_list(menu_id=menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    summary="Получить подменю",
    description="Получение подменю по его идентификатору",
    status_code=HTTP_200_OK,
)
async def get_submenu(
    submenu_id: int,
    menu_id: int,
    service: SubmenuServices = Depends(submenu_services),
):
    return await service.get_submenu(
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
async def create_submenu(
    menu_id: int,
    submenu: schemas.SubMenuCreate,
    service: SubmenuServices = Depends(submenu_services),
):
    return await service.create_submenu(
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
async def delete_submenu(
    submenu_id: int,
    menu_id: int,
    service: SubmenuServices = Depends(submenu_services),
):
    return await service.delete_submenu(id=submenu_id, menu_id=menu_id)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    summary="Обновить подменю",
    description="Обновление подменю",
    status_code=HTTP_200_OK,
)
async def patch_submenu(
    submenu_id: int,
    menu_id: int,
    submenu: schemas.SubMenuUpdate,
    service: SubmenuServices = Depends(submenu_services),
):
    return await service.update_submenu(
        id=submenu_id,
        menu_id=menu_id,
        submenu=submenu,
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.Dish],
    summary="Список блюд",
    description="Получение списка блюд",
    status_code=HTTP_200_OK,
)
async def list_dishes(
    submenu_id: int,
    menu_id: int,
    service: DishServices = Depends(dish_services),
):
    return await service.get_list_dishes(
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
async def get_dish(
    dish_id: int,
    menu_id: int,
    submenu_id: int,
    service: DishServices = Depends(dish_services),
):
    return await service.get_dish(
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
async def create_dish(
    dish: schemas.DishCreate,
    submenu_id: int,
    menu_id: int,
    service: DishServices = Depends(dish_services),
):
    return await service.create_dish(
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
async def patch_dish(
    dish_id: int,
    menu_id: int,
    submenu_id: int,
    dish: schemas.DishCreate,
    service: DishServices = Depends(dish_services),
):
    return await service.update_dish(
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
async def delete_dish(
    dish_id: int,
    menu_id: int,
    submenu_id: int,
    service: DishServices = Depends(dish_services),
):
    return await service.delete_dish(
        id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@app.get(
    "/api/v1/download_test_data",
    description="Загрузка тестовых данных",
    summary="Загрузить тестовые данные",
    status_code=HTTP_200_OK,
)
async def download_test_data(service: TestDataServices = Depends(test_data_service)):
    return await service.test_data_create()


@app.get(
    "/api/v1/get_menu_file/{id}",
    description="Загрузка меню в виде excel файла",
    summary="Получение меню в excel",
    status_code=HTTP_200_OK,
)
async def get_menu_file(id: str, service: MenuServices = Depends(menu_services)):
    return await service.get_menu_excel_file(id=id)


@app.post(
    "/api/v1/create_menu_file",
    description="Создать меню в виде excel файла",
    summary="Создать меню в excel",
    status_code=HTTP_202_ACCEPTED,
)
async def create_menu_file(service: MenuServices = Depends(menu_services)):
    return await service.create_menu_excel_file()

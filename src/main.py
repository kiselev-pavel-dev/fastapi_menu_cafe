from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.db.database import get_db
from src.schemas import schemas
from src.services.services import (
    dish_services, menu_services,
    submenu_services,
)

app = FastAPI()


@app.get(
    "/api/v1/menus",
    response_model=List[schemas.Menu],
    summary="Список меню",
    description="Получение списка всех меню",
    status_code=HTTP_200_OK,
)
def list_menus(session: Session = Depends(get_db)):
    return menu_services.get_list_menus(session=session)


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.Menu,
    summary="Получить меню",
    description="Получение меню по его идентификатору",
    status_code=HTTP_200_OK,
)
def get_menu(menu_id: int, session: Session = Depends(get_db)):
    return menu_services.get_menu(session=session, id=menu_id)


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    summary="Создать меню",
    description="Создание меню",
    status_code=HTTP_201_CREATED,
)
def create_menu(menu: schemas.MenuCreate, session: Session = Depends(get_db)):
    return menu_services.create_menu(session=session, menu=menu)


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
    session: Session = Depends(get_db),
):
    return menu_services.update_menu(session=session, id=menu_id, menu=menu)


@app.delete(
    "/api/v1/menus/{menu_id}",
    response_model=schemas.MenuDelete,
    summary="Удалить меню",
    description="Удаление меню",
    status_code=HTTP_200_OK,
)
def delete_menu(menu_id: int, session: Session = Depends(get_db)):
    return menu_services.delete_menu(session=session, id=menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[schemas.SubMenu],
    summary="Список подменю",
    description="Получение списка подменю определенного меню",
    status_code=HTTP_200_OK,
)
def list_submenus(menu_id: int, session: Session = Depends(get_db)):
    return submenu_services.get_submenu_list(session=session, id=menu_id)


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
    session: Session = Depends(get_db),
):
    return submenu_services.get_submenu(
        session=session,
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
    session: Session = Depends(get_db),
):
    return submenu_services.create_submenu(
        session=session,
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
def delete_submenu(submenu_id: int, session: Session = Depends(get_db)):
    return submenu_services.delete_submenu(session=session, id=submenu_id)


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
    session: Session = Depends(get_db),
):
    return submenu_services.update_submenu(
        session=session,
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
    session: Session = Depends(get_db),
):
    return dish_services.get_list_dishes(
        session=session,
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
    session: Session = Depends(get_db),
):
    return dish_services.get_dish(
        session=session,
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
    session: Session = Depends(get_db),
):
    return dish_services.create_dish(
        session=session,
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
    session: Session = Depends(get_db),
):
    return dish_services.update_dish(
        session=session,
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
    session: Session = Depends(get_db),
):
    return dish_services.delete_dish(
        session=session,
        id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

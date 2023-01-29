from typing import Dict, List

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.crud.cache import cache
from src.crud.crud import DishCrud, MenuCrud, SubmenuCrud
from src.schemas.schemas import (
    Dish, DishCreate, DishUpdate, Menu,
    MenuCreate, MenuUpdate, SubMenu,
    SubMenuCreate, SubMenuUpdate,
)


class MenuServices:

    def get_list_menus(self, session: Session) -> List[Menu]:
        redis_key = "menu:list"
        menus = cache.get(redis_key)
        if not menus:
            crud = MenuCrud(session=session)
            menus = crud.get_menu_list()
            for menu in menus:
                menu.submenus_count = crud.get_submenus_count(id=int(menu.id))
                menu.dishes_count = crud.get_dishes_count(id=int(menu.id))
            cache.set(redis_key, menus)
        return menus

    def get_menu(self, session: Session, id: int) -> Menu:
        redis_key = f"menu:{id}"
        menu = cache.get(redis_key)
        if not menu:
            crud = MenuCrud(session=session)
            menu = crud.get_menu(id=id)
            self.menu_empty(not menu)
            menu.submenus_count = crud.get_submenus_count(id=int(menu.id))
            menu.dishes_count = crud.get_dishes_count(id=int(menu.id))
            cache.set(redis_key, menu)
        return menu

    def create_menu(self, session: Session, menu: MenuCreate) -> Menu:
        cache.delete_one("menu:list")
        crud = MenuCrud(session=session)
        data = jsonable_encoder(menu)
        return crud.create_menu(data)

    def update_menu(self, session: Session, id: int, menu: MenuUpdate) -> Menu:
        redis_key = [f"menu:{id}", "menu:list"]
        crud = MenuCrud(session=session)
        current_menu = crud.get_menu(id=id)
        self.menu_empty(not current_menu)
        current_menu.title = menu.title
        current_menu.description = menu.description
        cache.delete_one(redis_key)
        return crud.update_menu(current_menu)

    def delete_menu(self, session: Session, id: int) -> Dict:
        redis_keys = [f"menu:{id}", "menu:list"]
        crud = MenuCrud(session=session)
        menu = crud.get_menu(id=id)
        self.menu_empty(not menu)
        crud.delete_menu(id=id)
        cache.delete_one(redis_keys)
        cache.delete_all(f"submenu:{id}:")
        cache.delete_all(f"dish:{menu.id}:")
        return {"status": True, "message": "The menu has been deleted"}

    def menu_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="menu not found",
            )


class SubmenuServices:
    def get_submenu(self, session: Session, id: int, menu_id: int) -> SubMenu:
        redis_key = f"submenu:{menu_id}:{id}"
        submenu = cache.get(redis_key)
        if not submenu:
            menu_services.get_menu(session=session, id=menu_id)
            crud = SubmenuCrud(session=session)
            submenu = crud.get_submenu(id=id)
            self.submenu_empty(not submenu)
            submenu.dishes_count = crud.get_dishes_count(id=int(submenu.id))
            cache.set(key=redis_key, value=submenu)
        return submenu

    def get_submenu_list(self, session: Session, id: int) -> List[SubMenu]:
        redis_key = f"submenu:{id}:list"
        submenus = cache.get(redis_key)
        if not submenus:
            menu_services.get_menu(session=session, id=id)
            crud = SubmenuCrud(session=session)
            submenus = crud.get_submenu_list(id=id)
            for submenu in submenus:
                submenu.dishes_count = crud.get_dishes_count(
                    id=int(submenu.id),
                )
            cache.set(redis_key, submenus)
        return submenus

    def create_submenu(
        self,
        session: Session,
        submenu: SubMenuCreate,
        menu_id: int,
    ) -> SubMenu:
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list", f"submenu:{menu_id}:list",
        ]
        cache.delete_one(redis_keys)
        menu_services.get_menu(session=session, id=menu_id)
        crud = SubmenuCrud(session=session)
        data = jsonable_encoder(submenu)
        submenu = crud.create_submenu(data, id=menu_id)
        return submenu

    def update_submenu(
        self,
        session: Session,
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
        current_submenu = self.get_submenu(
            session=session, id=id, menu_id=menu_id,
        )
        self.submenu_empty(not current_submenu)
        crud = SubmenuCrud(session=session)
        cache.delete_one(redis_keys)
        return crud.update_submenu(
            id=id,
            title=submenu.title,
            description=submenu.description,
        )

    def delete_submenu(self, session: Session, id: int) -> Dict:
        crud = SubmenuCrud(session=session)
        submenu = crud.get_submenu(id)
        self.submenu_empty(not submenu)
        crud.delete_submenu(id=id)
        redis_keys = [
            f"menu:{submenu.menu_id}",
            "menu:list",
            f"submenu:{submenu.menu_id}:list",
            f"submenu:{submenu.menu_id}:{id}",
        ]
        cache.delete_one(redis_keys)
        return {"status": True, "message": "The submenu has been deleted"}

    def submenu_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )


class DishServices:

    def get_dish(
        self,
        session: Session,
        id: int,
        menu_id: int,
        submenu_id: int,
    ) -> Dish:
        redis_key = f"dish:{menu_id}:{submenu_id}:{id}"
        dish = cache.get(redis_key)
        if not dish:
            crud = DishCrud(session=session)
            dish = crud.get_dish(id=id)
            self.dish_empty(not dish)
            cache.set(key=redis_key, value=dish)
        return dish

    def get_list_dishes(
        self,
        session: Session,
        submenu_id: int,
        menu_id: int,
    ) -> List[Dish]:
        redis_key = f"dish:{menu_id}:{submenu_id}:list"
        dishes = cache.get(redis_key)
        if not dishes:
            crud = DishCrud(session=session)
            dishes = crud.get_list_dish(id_submenu=submenu_id)
            cache.set(key=redis_key, value=dishes)
        return dishes

    def create_dish(
        self,
        session: Session,
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
        submenu_services.get_submenu(
            session=session, id=submenu_id, menu_id=menu_id,
        )
        crud = DishCrud(session=session)
        data = jsonable_encoder(dish)
        cache.delete_one(redis_keys)
        return crud.create_dish(data=data, id=submenu_id)

    def update_dish(
        self,
        session: Session,
        id: int,
        menu_id: int,
        submenu_id: int,
        dish: DishUpdate,
    ) -> Dish:
        current_dish = self.get_dish(
            session=session, id=id, menu_id=menu_id, submenu_id=submenu_id,
        )
        redis_keys = [
            f"menu:{menu_id}",
            "menu:list",
            f"submenu:{menu_id}:list",
            f"submenu:{menu_id}:{submenu_id}",
            f"dish:{menu_id}:{submenu_id}:{id}",
            f"dish:{menu_id}:{submenu_id}:list",
        ]
        cache.delete_one(redis_keys)
        self.dish_empty(not current_dish)
        crud = DishCrud(session=session)
        return crud.update_dish(
            id=id,
            title=dish.title,
            description=dish.description,
            price=dish.price,
        )

    def delete_dish(
        self,
        session: Session,
        id: int,
        menu_id: int,
        submenu_id: int,
    ) -> Dict:
        redis_keys = [
            f"dish:{menu_id}:{submenu_id}:{id}",
            f"dish:{menu_id}:{submenu_id}:list",
        ]
        crud = DishCrud(session=session)
        dish = crud.get_dish(id=id)
        self.dish_empty(not dish)
        crud.delete_dish(id=id)
        cache.delete_one(redis_keys)
        return {"status": True, "message": "The dish has been deleted"}

    def dish_empty(self, empty: bool) -> None:
        if empty:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="dish not found",
            )


menu_services = MenuServices()
submenu_services = SubmenuServices()
dish_services = DishServices()

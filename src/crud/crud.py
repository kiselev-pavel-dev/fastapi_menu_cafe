from dataclasses import dataclass
from typing import Dict, List

from sqlalchemy.orm import Session

from src.models.models import Dish, Menu, SubMenu
from src.schemas import schemas


@dataclass
class MenuCrud:

    session: Session

    def get_menu_list(self) -> List[schemas.Menu]:
        return self.session.query(Menu).all()

    def get_menu(self, id: int) -> schemas.Menu:
        return self.session.query(Menu).filter_by(id=id).first()

    def create_menu(self, data: Dict) -> schemas.Menu:
        menu = Menu(**data)
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def update_menu(self, menu: schemas.MenuUpdate) -> schemas.Menu:
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def delete_menu(self, id: int) -> None:
        self.session.query(Menu).filter_by(id=id).delete()
        self.session.commit()

    def get_submenus_count(self, id: int) -> int:
        return self.session.query(SubMenu).filter_by(menu_id=id).count()

    def get_dishes_count(self, id: int) -> int:
        return self.session.query(Dish).filter(
            Dish.submenu_id == SubMenu.id,
        ).filter(
            SubMenu.menu_id == id,
        ).count()


@dataclass
class SubmenuCrud:
    session: Session

    def get_submenu(self, id: int) -> schemas.SubMenu:
        return self.session.query(SubMenu).filter_by(id=id).first()

    def get_submenu_list(self, id: int) -> List[schemas.SubMenu]:
        return self.session.query(SubMenu).filter_by(menu_id=id).all()

    def create_submenu(self, data: Dict, id: int) -> schemas.SubMenu:
        submenu = SubMenu(**data, menu_id=id)
        self.session.add(submenu)
        self.session.commit()
        self.session.refresh(submenu)
        return submenu

    def update_submenu(
        self,
        id: int,
        title: str,
        description: str,
    ) -> schemas.SubMenu:
        submenu = self.session.query(SubMenu).filter_by(id=id).one()
        submenu.title = title
        submenu.description = description
        self.session.add(submenu)
        self.session.commit()
        self.session.refresh(submenu)
        return submenu

    def delete_submenu(self, id: int) -> None:
        self.session.query(SubMenu).filter_by(id=id).delete()
        self.session.commit()

    def get_dishes_count(self, id: int) -> int:
        return self.session.query(Dish).filter(
            Dish.submenu_id == id,
        ).count()


@dataclass
class DishCrud:
    session: Session

    def get_dish(self, id: int) -> schemas.Dish:
        return self.session.query(Dish).filter_by(id=id).first()

    def get_list_dish(self, id_submenu: int) -> List[schemas.Dish]:
        return self.session.query(Dish).filter_by(submenu_id=id_submenu).all()

    def create_dish(self, data: Dict, id: int) -> schemas.Dish:
        dish = Dish(**data, submenu_id=id)
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def update_dish(
        self,
        id: int,
        title: str,
        description: str,
        price: str,
    ) -> schemas.Dish:
        dish = self.session.query(Dish).filter_by(id=id).one()
        dish.title = title
        dish.description = description
        dish.price = price
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def delete_dish(self, id: int) -> None:
        self.session.query(Dish).filter_by(id=id).delete()
        self.session.commit()

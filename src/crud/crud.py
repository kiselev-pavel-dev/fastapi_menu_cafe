from sqlalchemy import delete, func, select, update

from src.crud.base import BaseCrud
from src.models.models import Dish, Menu, SubMenu
from src.schemas import schemas


class MenuCrud(BaseCrud):
    async def get_menu_list(self) -> list[schemas.Menu]:
        statement = select(
            Menu.id,
            Menu.title,
            Menu.description,
        ).group_by(Menu.id)
        result = await self.session.execute(statement)
        menu_list: list[schemas.Menu] = result.all()
        return menu_list

    async def get_menu(self, id: int) -> schemas.Menu:
        statement = select(
            Menu.id,
            Menu.title,
            Menu.description,
        ).where(Menu.id == id)
        result = await self.session.execute(statement)
        menu = result.one_or_none()
        return menu

    async def create_menu(self, data: dict) -> schemas.Menu:
        menu = Menu(**data)
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def update_menu(self, id: int, title: str, description: str) -> schemas.Menu:
        statement = (
            update(Menu)
            .where(Menu.id == id)
            .values(
                title=title,
                description=description,
            )
        )
        return await self.session.execute(statement)

    async def delete_menu(self, id: int) -> None:
        statement = delete(Menu).where(Menu.id == id)
        await self.session.execute(statement)
        await self.session.commit()

    async def get_submenus_count(self, id: int) -> int:
        statement = select(
            func.count(SubMenu.id).label("count"),
        ).where(
            SubMenu.menu_id == id,
        )
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_dishes_count(self, id: int) -> int:
        statement = (
            select(
                func.count(Dish.id).label("dishes_count"),
            )
            .join(SubMenu)
            .where(SubMenu.menu_id == id)
        )
        result = await self.session.execute(statement)
        return result.scalar()


class SubmenuCrud(BaseCrud):
    async def get_submenu(self, id: int) -> schemas.SubMenu:
        statement = select(
            SubMenu.id,
            SubMenu.title,
            SubMenu.description,
        ).where(SubMenu.id == id)
        result = await self.session.execute(statement)
        return result.one_or_none()

    async def get_submenu_list(self, menu_id: int) -> list[schemas.SubMenu]:
        statement = select(SubMenu.id, SubMenu.title, SubMenu.description).where(
            SubMenu.menu_id == menu_id,
        )
        result = await self.session.execute(statement)
        submenu_list: list[schemas.SubMenu] = result.all()
        return submenu_list

    async def create_submenu(self, data: dict, id: int) -> schemas.SubMenu:
        submenu = SubMenu(**data, menu_id=id)
        self.session.add(submenu)
        await self.session.commit()
        await self.session.refresh(submenu)
        return submenu

    async def update_submenu(
        self,
        id: int,
        title: str,
        description: str,
    ) -> schemas.SubMenu:
        statement = (
            update(SubMenu)
            .where(SubMenu.id == id)
            .values(
                title=title,
                description=description,
            )
        )
        return await self.session.execute(statement)

    async def delete_submenu(self, id: int) -> None:
        statement = delete(SubMenu).where(SubMenu.id == id)
        await self.session.execute(statement)
        await self.session.commit()

    async def get_dishes_count(self, id: int) -> int:
        statement = select(
            func.count(Dish.id).label("dishes_count"),
        ).where(SubMenu.id == id)
        result = await self.session.execute(statement)
        return result.scalar()


class DishCrud(BaseCrud):
    async def get_dish(self, id: int) -> schemas.Dish:
        statement = select(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
        ).where(Dish.id == id)
        result = await self.session.execute(statement)
        return result.one_or_none()

    async def get_list_dish(self, id_submenu: int) -> list[schemas.Dish]:
        statement = select(Dish.id, Dish.title, Dish.description, Dish.price).where(
            Dish.submenu_id == id_submenu,
        )
        result = await self.session.execute(statement)
        dish_list: list[schemas.Dish] = result.all()
        return dish_list

    async def create_dish(self, data: dict, id: int) -> schemas.Dish:
        dish = Dish(**data, submenu_id=id)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def update_dish(
        self,
        id: int,
        title: str,
        description: str,
        price: str,
    ) -> schemas.Dish:
        statement = (
            update(Dish)
            .where(Dish.id == id)
            .values(
                title=title,
                description=description,
                price=price,
            )
        )
        return await self.session.execute(statement)

    async def delete_dish(self, id: int) -> None:
        statement = delete(Dish).where(Dish.id == id)
        await self.session.execute(statement)
        await self.session.commit()


class TestDataCrud(BaseCrud):
    async def delete_all_tables(self) -> None:
        statement = delete(Menu)
        await self.session.execute(statement)
        statement = delete(SubMenu)
        await self.session.execute(statement)
        statement = delete(Dish)
        await self.session.execute(statement)
        await self.session.commit()

    async def create_menu(self, menu_data: dict) -> None:
        menu = Menu(**menu_data)
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)

    async def create_submenu(self, submenu_data: dict) -> None:
        submenu = SubMenu(**submenu_data)
        self.session.add(submenu)
        await self.session.commit()
        await self.session.refresh(submenu)

    async def create_dish(self, dish_data: dict) -> None:
        dish = Dish(**dish_data)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)

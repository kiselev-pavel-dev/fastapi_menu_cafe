from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Menu title",
                "description": "Menu description"
            }
        }


class MenuCreate(BaseMenu):
    pass


class MenuUpdate(BaseMenu):
    class Config:
        schema_extra = {
            "example": {
                "title": "New menu title",
                "description": "New menu description"
            }
        }


class Menu(BaseMenu):
    id: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Menu title",
                "description": "Menu description",
                "submenus_count": 0,
                "dishes_count": 0
            }
        }


class MenuDelete(BaseModel):
    status: bool = True
    message: str = "The menu has been deleted"

    class Config:
        schema_extra = {"example": {"status": True,
                                    "message": "The menu has been deleted"}}


class BaseSubMenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Submenu title",
                "description": "Submenu description"
            }
        }


class SubMenuCreate(BaseSubMenu):
    pass


class SubMenuUpdate(BaseSubMenu):
    class Config:
        schema_extra = {
            "example": {
                "title": "New submenu title",
                "description": "New submenu description"
            }
        }


class SubMenu(BaseSubMenu):
    id: str
    dishes_count: int = 0

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Submenu title",
                "description": "Submenu description",
                "dishes_count": 0
            }
        }


class SubMenuDelete(BaseModel):
    status: bool = True
    message: str = "The submenu has been deleted"

    class Config:
        schema_extra = {"example": {"status": True,
                                    "message": "The submenu has been deleted"}}


class BaseDish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Dish title",
                "description": "Dish description",
                "price": "22.87"
            }
        }


class DishCreate(BaseDish):
    pass


class DishUpdate(BaseDish):
    class Config:
        schema_extra = {
            "example": {
                "title": "New dish title",
                "description": "New dish description",
                "price": "77.77"
            }
        }


class Dish(BaseDish):
    id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Dish title",
                "description": "Dish description",
                "price": "22.87"
            }
        }


class DishDelete(BaseModel):
    status: bool = True
    message: str = "The dish has been deleted"

    class Config:
        schema_extra = {"example": {"status": True,
                                    "message": "The dish has been deleted"}}

from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Menu(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubMenuCreate(BaseModel):
    title: str
    description: str
    menu_id: None = 0

    class Config:
        orm_mode = True


class SubMenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int = 0

    class Config:
        orm_mode = True


class DishCreate(BaseModel):
    title: str
    description: str
    price: str
    submenu_id: None = 0

    class Config:
        orm_mode = True


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True

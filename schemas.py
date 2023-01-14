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


class SubMenu(BaseModel):
    id: int
    title: str
    description: str
    menu: int

    class Config:
        orm_mode = True


class Dish(BaseModel):
    id: int
    title: str
    description: str
    price: float
    submenu: int

    class Config:
        orm_mode = True

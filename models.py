from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db.database import Base


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


# class SubMenu(Base):
#     __tablename__ = "submenus"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     menu = relationship("Menu", cascade="all,delete")


# class Dish(Base):
#     __tablename__ = "dishes"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     price = Column(Float)
#     submenu = relationship("SubMenu", cascade="all,delete")

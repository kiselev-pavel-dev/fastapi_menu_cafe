from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import Base
from models import Menu, SubMenu, Dish
import schemas


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseActions(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj: CreateSchemaType) -> ModelType:
        obj = jsonable_encoder(obj)
        db_obj = self.model(**obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, obj_curr: ModelType, obj_update: ModelType) -> ModelType:
        obj_curr.title = obj_update.title
        obj_curr.description = obj_update.description
        db.add(obj_curr)
        db.commit()
        db.refresh(obj_curr)
        return obj_curr

    def delete(self, db: Session, id: int, message: str) -> ModelType:
        obj = db.query(self.model).filter(self.model.id == id).delete()
        db.commit()
        return {"status": True, "message": message}


class MenuActions(BaseActions[Menu, schemas.MenuCreate]):
    pass


class SubMenuActions(BaseActions[SubMenu, schemas.SubMenuCreate]):
    def get_all(self, db: Session, id: int) -> List[ModelType]:
        return db.query(self.model).filter(self.model.menu_id == id).all()


class DishActions(BaseActions[Dish, schemas.DishCreate]):
    def get_all(self, db: Session, id: int) -> List[ModelType]:
        return db.query(self.model).filter(self.model.submenu_id == id).all()


menu = MenuActions(Menu)
submenu = SubMenuActions(SubMenu)
dish = DishActions(Dish)

from typing import Union, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import models

from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=List[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    for menu in menus:
        menu.submenus_count = 123
        menu.dishes_count = 123
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(
        models.Menu.id == str(menu_id)).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = models.Menu(title=menu.title, description=menu.description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: int, menu: schemas.Menu, db: Session = Depends(get_db)):
    menu_curr = db.query(models.Menu).filter(
        models.Menu.id == str(menu_id)).first()
    if menu_curr is None:
        raise HTTPException(status_code=404, detail="menu not found")
    print(menu_curr.title, "----------", menu.title)
    menu_curr.title = menu.title
    menu_curr.description = menu.description
    db.add(menu_curr)
    db.commit()
    db.refresh(menu_curr)
    return menu_curr


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(
        models.Menu.id == str(menu_id)).first()
    db.delete(menu)
    db.commit()
    return {"status": True, "message": "The menu has been deleted"}

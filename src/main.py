from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from services import actions
from models import schemas
import tables as models
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=List[schemas.Menu])
def list_menus(db: Session = Depends(get_db)):
    menus = actions.menu.get_all(db=db)
    for menu in menus:
        menu.submenus_count = db.query(models.SubMenu).filter(
            models.SubMenu.menu_id == menu.id).count()
        menu.dishes_count = db.query(models.Dish).filter(
            models.Dish.submenu_id == models.SubMenu.id).filter(
            models.SubMenu.menu_id == menu.id).count()
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = actions.menu.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="menu not found")
    menu.submenus_count = db.query(models.SubMenu).filter(
        models.SubMenu.menu_id == menu_id).count()
    menu.dishes_count = db.query(models.Dish).filter(
        models.Dish.submenu_id == models.SubMenu.id).filter(
        models.SubMenu.menu_id == menu_id).count()
    return menu


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    status_code=HTTP_201_CREATED
)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = actions.menu.create(db=db, obj=menu)
    return menu


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def patch_menu(
    menu_id: int,
    menu: schemas.MenuCreate,
    db: Session = Depends(get_db)
):
    menu_curr = actions.menu.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="menu not found")
    menu_curr = actions.menu.update(db=db, obj_curr=menu_curr, obj_update=menu)
    return menu_curr


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = actions.menu.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="menu not found")
    message = "The menu has been deleted"
    menu = actions.menu.delete(db=db, id=menu_id, message=message)
    return menu


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[schemas.SubMenu]
)
def list_submenus(menu_id: int, db: Session = Depends(get_db)):
    submenus = actions.submenu.get_all(db=db, id=menu_id)
    for submenu in submenus:
        submenu.dishes_count = db.query(models.Dish).filter(
            models.Dish.submenu_id == submenu.id).count()
    return submenus


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu
)
def get_submenu(submenu_id: int, db: Session = Depends(get_db)):
    submenu = actions.submenu.get(db=db, id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="submenu not found")
    submenu.dishes_count = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu.id).count()
    return submenu


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.SubMenu,
    status_code=HTTP_201_CREATED
)
def create_submenu(
    menu_id: int,
    submenu: schemas.SubMenuCreate,
    db: Session = Depends(get_db)
):
    menu = actions.menu.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="menu not found")
    submenu.menu_id = menu_id
    submenu = actions.submenu.create(db=db, obj=submenu)
    return submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(submenu_id: int, db: Session = Depends(get_db)):
    submenu = actions.submenu.get(db=db, id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Submenu not found")
    message = "The submenu has been deleted"
    submenu = actions.submenu.delete(db=db, id=submenu_id, message=message)
    return submenu


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu
)
def patch_submenu(
    submenu_id: int,
    submenu: schemas.SubMenuCreate,
    db: Session = Depends(get_db)
):
    submenu_curr = actions.submenu.get(db=db, id=submenu_id)
    if not submenu_curr:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="submenu not found")
    submenu_curr = actions.submenu.update(
        db=db, obj_curr=submenu_curr, obj_update=submenu)
    return submenu_curr


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[schemas.Dish]
)
def list_dishes(submenu_id: int, db: Session = Depends(get_db)):
    dishes = actions.dish.get_all(db=db, id=submenu_id)
    return dishes


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish
)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = actions.dish.get(db=db, id=dish_id)
    if not dish:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="dish not found")
    return dish


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    status_code=HTTP_201_CREATED
)
def create_dish(dish: schemas.DishCreate,
                submenu_id: int,
                db: Session = Depends(get_db)
                ):
    submenu = actions.submenu.get(db=db, id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="submenu not found")
    dish.submenu_id = submenu_id
    dish = actions.dish.create(db=db, obj=dish)
    return dish


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = actions.dish.get(db=db, id=dish_id)
    if not dish:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="dish not found")
    message = "The dish has been deleted"
    dish = actions.dish.delete(db=db, id=dish_id, message=message)
    return dish


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish
)
def patch_dish(
    dish_id,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db)
):
    dish_curr = actions.dish.get(db=db, id=dish_id)
    if not dish_curr:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="dish not found")
    dish_curr.price = dish.price
    dish_curr = actions.dish.update(
        db=db, obj_curr=dish_curr, obj_update=dish)
    return dish_curr

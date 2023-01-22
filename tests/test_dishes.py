import json
import pytest

from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY

from src.tables import Dish, Menu, SubMenu
from .conf_test_db import app, override_get_db

client = TestClient(app=app)
db = next(override_get_db())


@pytest.fixture(name="create_menu")
def create_menu():
    menu = {"title": "Тестовое меню",
            "description": "Описание тестового меню"}
    db_obj = Menu(**menu)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@pytest.fixture(name="create_submenu")
def create_submenu():
    menu = db.query(Menu).first()
    submenu = {"title": "Тестовое подменю",
               "description": "Описание тестового подменю",
               "menu_id": menu.id
               }
    db_obj = SubMenu(**submenu)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@pytest.fixture(name="create_dish")
def create_dish():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    dish = {"title": "Тестовое блюдо",
            "description": "Описание тестового блюда",
            "price": "33.48",
            "submenu_id": submenu.id
            }
    db_obj = Dish(**dish)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@pytest.mark.usefixtures("create_menu", "create_submenu", "create_dish")
def test_get_dishes_list():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    count_dishes = db.query(Dish).filter_by(submenu_id=submenu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list) == True
    assert len(response.json()) == count_dishes


def test_get_dish():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    dish = db.query(Dish).filter_by(submenu_id=submenu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(dish.id)
    assert response.json()["title"] == dish.title
    assert response.json()["description"] == dish.description
    assert response.json()["price"] == dish.price


def test_get_dish_not_found():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/1111"
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "dish not found"


def test_create_dish():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    count_dishes = db.query(Dish).filter_by(submenu_id=submenu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    data = {}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New dish"}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New dish",
            "description": "Description dish", "price": "23.50"}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_201_CREATED
    count_dishes_new = db.query(Dish).filter_by(submenu_id=submenu.id).count()
    assert count_dishes + 1 == count_dishes_new
    assert isinstance(response.json(), dict) == True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert isinstance(response.json()["id"], str) == True


def test_update_dish():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    dish = db.query(Dish).filter_by(submenu_id=submenu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    data = {"title": "New title"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New title",
            "description": "New_description", "price": "50.00"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict) == True
    assert isinstance(response.json()["id"], str) == True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]


def test_update_dish_not_found():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/1111"
    data = {"title": "New title",
            "description": "New_description", "price": "23.50"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "dish not found"


def test_delete_dish():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    dish = db.query(Dish).filter_by(submenu_id=submenu.id).first()
    count_dishes = db.query(Dish).filter_by(submenu_id=submenu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = client.delete(url)
    count_dishes_new = db.query(Dish).filter_by(submenu_id=submenu.id).count()
    assert response.status_code == HTTP_200_OK
    assert count_dishes == count_dishes_new + 1
    assert response.json()["status"] == True
    assert response.json()["message"] == "The dish has been deleted"

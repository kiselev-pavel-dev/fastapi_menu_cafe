import json

import pytest
from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.models.models import Menu, SubMenu

from .conf_db_test import app, override_get_db

client = TestClient(app=app)
db = next(override_get_db())


@pytest.fixture(autouse=True)
def create_fixtures():
    menu = {
        "title": "Тестовое меню",
        "description": "Описание тестового меню",
    }
    db_obj = Menu(**menu)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    menu = db.query(Menu).first()
    submenu = {
        "title": "Тестовое подменю",
        "description": "Описание тестового подменю",
        "menu_id": menu.id,
    }
    db_obj = SubMenu(**submenu)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def test_get_submenus_list():
    menu = db.query(Menu).first()
    count_submenus = db.query(SubMenu).filter_by(menu_id=menu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == count_submenus


def test_get_submenu():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(submenu.id)
    assert response.json()["title"] == submenu.title
    assert response.json()["description"] == submenu.description


def test_get_submenu_not_found():
    menu = db.query(Menu).first()
    url = f"/api/v1/menus/{menu.id}/submenus/1111"
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "submenu not found"


def test_create_submenu():
    menu = db.query(Menu).first()
    count_submenus = db.query(SubMenu).filter_by(menu_id=menu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus"
    data = {}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New submenu"}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New submenu", "description": "Description submenu"}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_201_CREATED
    count_submenus_new = db.query(SubMenu).filter_by(menu_id=menu.id).count()
    assert count_submenus + 1 == count_submenus_new
    assert isinstance(response.json(), dict) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert isinstance(response.json()["id"], str) is True


def test_update_submenu():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    data = {"title": "New title"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New title", "description": "New_description"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict) is True
    assert isinstance(response.json()["id"], str) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]


def test_update_submenu_not_found():
    menu = db.query(Menu).first()
    url = f"/api/v1/menus/{menu.id}/submenus/1111"
    data = {"title": "New title", "description": "New_description"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "submenu not found"


def test_delete_submenu():
    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(menu_id=menu.id).first()
    count_submenus = db.query(SubMenu).filter_by(menu_id=menu.id).count()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = client.delete(url)
    count_submenus_new = db.query(SubMenu).filter_by(menu_id=menu.id).count()
    assert response.status_code == HTTP_200_OK
    assert count_submenus == count_submenus_new + 1
    assert response.json()["status"] is True
    assert response.json()["message"] == "The submenu has been deleted"

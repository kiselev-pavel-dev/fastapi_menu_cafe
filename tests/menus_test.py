import json

import pytest
from fastapi.testclient import TestClient
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_404_NOT_FOUND,
                              HTTP_422_UNPROCESSABLE_ENTITY)

from src.models.models import Menu

from .conf_db_test import app, override_get_db

client = TestClient(app=app)
db = next(override_get_db())


@pytest.fixture(autouse=True)
def create_menu():
    menu = {"title": "Тестовое меню", "description": "Описание тестового меню"}
    db_obj = Menu(**menu)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def test_get_list_menus():
    count_menu = db.query(Menu).count()
    url = "/api/v1/menus"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == count_menu
    assert isinstance(response.json(), list) == True


def test_get_menu():
    menu = db.query(Menu).first()
    url = f"/api/v1/menus/{menu.id}"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(menu.id)
    assert response.json()["title"] == menu.title
    assert response.json()["description"] == menu.description


def test_get_menu_not_found():
    url = "/api/v1/menus/1111"
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "menu not found"


def test_create_menu():
    url = "/api/v1/menus"
    count_menu = db.query(Menu).count()
    data = {}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "Test"}
    response = client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "Test title", "description": "Test description"}
    response = client.post(url, data=json.dumps(data))
    count_menu_new = db.query(Menu).count()
    assert response.status_code == HTTP_201_CREATED
    assert count_menu_new == count_menu + 1
    assert isinstance(response.json(), dict) == True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert isinstance(response.json()["id"], str) == True


def test_update_menu():
    menu = db.query(Menu).first()
    url = f"/api/v1/menus/{menu.id}"
    data = {"title": "New title"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New title", "description": "New_description"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict) == True
    assert isinstance(response.json()["id"], str) == True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]


def test_update_menu_not_found():
    url = "/api/v1/menus/1111"
    data = {"title": "New title", "description": "New_description"}
    response = client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "menu not found"


def test_delete_menu():
    menu = db.query(Menu).first()
    count_menus = db.query(Menu).count()
    url = f"/api/v1/menus/{menu.id}"
    response = client.delete(url)
    count_menus_new = db.query(Menu).count()
    assert response.status_code == HTTP_200_OK
    assert count_menus == count_menus_new + 1
    assert response.json()["status"] == True
    assert response.json()["message"] == "The menu has been deleted"

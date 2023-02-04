import json

import pytest
from sqlalchemy import func, select
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.models.models import Menu


@pytest.mark.asyncio
async def test_get_list_menus(client, create_menu, db):
    statement = select(func.count(Menu.id))
    result = await db.execute(statement)
    count = result.scalar()
    url = "/api/v1/menus"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == count
    assert isinstance(response.json(), list) is True


@pytest.mark.asyncio
async def test_get_menu(menu_data, client, create_menu):
    id = menu_data["id"]
    url = f"/api/v1/menus/{id}"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(menu_data["id"])
    assert response.json()["title"] == menu_data["title"]
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio
async def test_get_menu_not_found(client):
    url = "/api/v1/menus/1111"
    response = await client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "menu not found"


@pytest.mark.asyncio
async def test_create_menu(db, client):
    url = "/api/v1/menus"
    statement = select(func.count(Menu.id))
    result = await db.execute(statement)
    count_menus = result.scalar()
    data = {}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "Test"}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "Test title", "description": "Test description"}
    response = await client.post(url, data=json.dumps(data))
    statement = select(func.count(Menu.id))
    result = await db.execute(statement)
    count_menus_new = result.scalar()
    assert response.status_code == HTTP_201_CREATED
    assert count_menus_new == count_menus + 1
    assert isinstance(response.json(), dict) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert isinstance(response.json()["id"], str) is True


@pytest.mark.asyncio
async def test_update_menu(create_menu, db, client):
    menu = create_menu
    url = f"/api/v1/menus/{menu.id}"
    data = {"title": "New title"}
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New title", "description": "New_description"}
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict) is True
    assert isinstance(response.json()["id"], str) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]


@pytest.mark.asyncio
async def test_update_menu_not_found(client):
    url = "/api/v1/menus/1111"
    data = {"title": "New title", "description": "New_description"}
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "menu not found"


@pytest.mark.asyncio
async def test_delete_menu(client, create_menu, db):
    menu = create_menu
    statement = select(func.count(Menu.id))
    result = await db.execute(statement)
    count_menus = result.scalar()
    url = f"/api/v1/menus/{menu.id}"
    response = await client.delete(url)
    statement = select(func.count(Menu.id))
    result = await db.execute(statement)
    count_menus_new = result.scalar()
    assert response.status_code == HTTP_200_OK
    assert count_menus == count_menus_new + 1
    assert response.json()["status"] is True
    assert response.json()["message"] == "The menu has been deleted"
    response = await client.delete(url)
    assert response.status_code == HTTP_404_NOT_FOUND

import json

import pytest
from sqlalchemy import func, select
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.models.models import SubMenu


@pytest.mark.asyncio
async def test_get_submenus_list(client, create_menu, db, create_submenu):
    menu = create_menu
    statement = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
    result = await db.execute(statement)
    count_submenus = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == count_submenus


@pytest.mark.asyncio
async def test_get_submenu(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(submenu.id)
    assert response.json()["title"] == submenu.title
    assert response.json()["description"] == submenu.description


@pytest.mark.asyncio
async def test_get_submenu_not_found(db, client, create_menu):
    menu = create_menu
    url = f"/api/v1/menus/{menu.id}/submenus/1111"
    response = await client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "submenu not found"


@pytest.mark.asyncio
async def test_create_submenu(db, client, create_menu):
    menu = create_menu
    statement = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
    result = await db.execute(statement)
    count_submenus = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus"
    data = {}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New submenu"}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New submenu", "description": "Description submenu"}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_201_CREATED
    statement = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
    result = await db.execute(statement)
    count_submenus_new = result.scalar()
    assert count_submenus + 1 == count_submenus_new
    assert isinstance(response.json(), dict) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert isinstance(response.json()["id"], str) is True


@pytest.mark.asyncio
async def test_update_submenu(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
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
async def test_update_submenu_not_found(client, create_menu):
    menu = create_menu
    url = f"/api/v1/menus/{menu.id}/submenus/1111"
    data = {"title": "New title", "description": "New_description"}
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "submenu not found"


@pytest.mark.asyncio
async def test_delete_submenu(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    statement = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
    result = await db.execute(statement)
    count_submenus = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = await client.delete(url)
    statement = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
    result = await db.execute(statement)
    count_submenus_new = result.scalar()
    assert response.status_code == HTTP_200_OK
    assert count_submenus == count_submenus_new + 1
    assert response.json()["status"] is True
    assert response.json()["message"] == "The submenu has been deleted"

import json

import pytest
from sqlalchemy import func, select
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.models.models import Dish


@pytest.mark.asyncio
async def test_get_dishes_list(db, client, create_menu, create_submenu, create_dish):
    menu = create_menu
    submenu = create_submenu
    statement = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
    result = await db.execute(statement)
    count_dishes = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == count_dishes


@pytest.mark.asyncio
async def test_get_dish(db, client, create_menu, create_submenu, create_dish):
    menu = create_menu
    submenu = create_submenu
    dish = create_dish
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = await client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == str(dish.id)
    assert response.json()["title"] == dish.title
    assert response.json()["description"] == dish.description
    assert response.json()["price"] == dish.price


@pytest.mark.asyncio
async def test_get_dish_not_found(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/1111"
    response = await client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "dish not found"


@pytest.mark.asyncio
async def test_create_dish(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    statement = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
    result = await db.execute(statement)
    count_dishes = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    data = {}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {"title": "New dish"}
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {
        "title": "New dish",
        "description": "Description dish",
        "price": "23.50",
    }
    response = await client.post(url, data=json.dumps(data))
    assert response.status_code == HTTP_201_CREATED
    statement = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
    result = await db.execute(statement)
    count_dishes_new = result.scalar()
    assert count_dishes + 1 == count_dishes_new
    assert isinstance(response.json(), dict) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert isinstance(response.json()["id"], str) is True


@pytest.mark.asyncio
async def test_update_dish(db, client, create_menu, create_submenu, create_dish):
    menu = create_menu
    submenu = create_submenu
    dish = create_dish
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    data = {"title": "New title"}
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    data = {
        "title": "New title",
        "description": "New_description",
        "price": "50.00",
    }
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict) is True
    assert isinstance(response.json()["id"], str) is True
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]


@pytest.mark.asyncio
async def test_update_dish_not_found(db, client, create_menu, create_submenu):
    menu = create_menu
    submenu = create_submenu
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/1111"
    data = {
        "title": "New title",
        "description": "New_description",
        "price": "23.50",
    }
    response = await client.patch(url, data=json.dumps(data))
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "dish not found"


@pytest.mark.asyncio
async def test_delete_dish(db, client, create_menu, create_submenu, create_dish):
    menu = create_menu
    submenu = create_submenu
    dish = create_dish
    statement = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
    result = await db.execute(statement)
    count_dishes = result.scalar()
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = await client.delete(url)
    statement = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
    result = await db.execute(statement)
    count_dishes_new = result.scalar()
    assert response.status_code == HTTP_200_OK
    assert count_dishes == count_dishes_new + 1
    assert response.json()["status"] is True
    assert response.json()["message"] == "The dish has been deleted"

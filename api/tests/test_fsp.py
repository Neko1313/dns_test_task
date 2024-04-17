from sqlalchemy import insert, select
from httpx import AsyncClient

from models.fsp import Cities

from conftest import client, async_session_maker


async def test_get_cities(ac: AsyncClient):
    response = await ac.get("/cities")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_add_city_1(ac: AsyncClient):
    response = await ac.post("/cities", json={"name": "TestCity_1"})
    assert response.status_code == 200
    assert "id" in response.json()


async def test_add_road(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(Cities.id).where(Cities.name == "SoDo")
        city_1 = await session.execute(query)
        city_1_id = city_1.scalar_one()

        query = select(Cities.id).where(Cities.name == "Redmond")
        city_2 = await session.execute(query)
        city_2_id = city_2.scalar_one()

    response = await ac.post(
        "/road",
        json={
            "from_city_id": city_1_id,
            "to_city_id": city_2_id,
            "distance": 19,
        },
    )
    assert response.status_code == 200
    assert "id" in response.json()


async def test_find_shortest_path(ac: AsyncClient):
    response = await ac.get("/cities/SoDo/findShortestPath?to=Redmond")
    assert response.status_code == 200
    assert "distance" in response.json()["result"]

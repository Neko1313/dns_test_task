import heapq
from typing import List

from src.schemas.fsp import (
    CitiesSchemaAdd,
    CitiesSchema,
    RoutesSchema,
    RoutesSchemaAdd,
)
from src.utils.unitofwork import IUnitOfWork


class CitiesService:
    async def add_cities(
        self, uow: IUnitOfWork, cities: CitiesSchemaAdd
    ) -> None | int:
        cities_dict = cities.model_dump()
        async with uow:
            cities_id = await uow.cities.add_one(cities_dict)
            await uow.commit()
            return cities_id

    async def get_cities(self, uow: IUnitOfWork) -> List[CitiesSchema]:
        async with uow:
            cities = await uow.cities.find_all()
            return cities

    async def shortest_path(
        self, uow: IUnitOfWork, start_city_name: str, end_city_name: str
    ) -> None | int:
        async with uow:
            cities = await uow.cities.find_all()
            routes = await uow.routes.find_all()

            city_dict = {city.name: city.id for city in cities}
            graph = {city.id: [] for city in cities}

            for route in routes:
                graph[route.from_city_id].append(
                    (route.to_city_id, route.distance)
                )

            if (
                start_city_name not in city_dict
                or end_city_name not in city_dict
            ):
                return None

            # Инициализация для алгоритма Дейкстры
            start_id = city_dict[start_city_name]
            end_id = city_dict[end_city_name]
            min_heap = [(0, start_id)]
            shortest_paths = {city.id: float("inf") for city in cities}
            shortest_paths[start_id] = 0
            visited = set()

            while min_heap:
                current_distance, current_city_id = heapq.heappop(min_heap)

                if current_city_id in visited:
                    continue

                if current_city_id == end_id:
                    return current_distance

                visited.add(current_city_id)

                for neighbor, weight in graph[current_city_id]:
                    if neighbor in visited:
                        continue

                    distance = current_distance + weight
                    if distance < shortest_paths[neighbor]:
                        shortest_paths[neighbor] = distance
                        heapq.heappush(min_heap, (distance, neighbor))

            return None


class CitiesService:
    async def add_cities(
        self, uow: IUnitOfWork, cities: RoutesSchemaAdd
    ) -> None | int:
        cities_dict = cities.model_dump()
        async with uow:
            road_id = await uow.routes.add_one(cities_dict)
            if road_id is None:
                uow.rollback()
                return None

            await uow.commit()
            return road_id

    async def get_cities(self, uow: IUnitOfWork) -> List[RoutesSchema]:
        async with uow:
            cities = await uow.routes.find_all()
            return cities

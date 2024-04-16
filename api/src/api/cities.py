from typing import List
from fastapi import APIRouter, HTTPException

from src.api.dependencies import UOWDep
from src.services.fsp import CitiesService
from src.schemas.fsp import CitiesSchemaAdd, CitiesSchemaAddResult, CitiesSchemaPathResult, CitiesSchemaPath, CitiesSchema

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.get("")
async def get_cities(
    uow: UOWDep,
) -> List[CitiesSchema]:
    """
    Получение всех городов
    """

    cities = await CitiesService().get_cities(uow)
    return cities


@router.get("/{city}/findShortestPath")
async def get_count_path(
    city: str,
    to: str,
    uow: UOWDep,
) -> CitiesSchemaPath:
    """
    Получение пути из города A в город B
    """
    
    distance = await CitiesService().shortest_path(uow, city, to)
    if distance is None:
        raise HTTPException(status_code=404, detail="City or Route not found")

    return CitiesSchemaPath(
        city=city,
        result=CitiesSchemaPathResult(
            distance=distance,
            targetCity=to,
        ),
    )


@router.post("")
async def add_cities(
    city: CitiesSchemaAdd,
    uow: UOWDep,
) -> CitiesSchemaAddResult:
    """
    Добавление нового города
    """

    city_id = await CitiesService().add_cities(uow, city)
    return CitiesSchemaAddResult(id=city_id)

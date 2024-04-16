from typing import List
from fastapi import APIRouter, HTTPException

from src.api.dependencies import UOWDep
from src.services.fsp import CitiesService
from src.schemas.fsp import RoutesSchema, RoutesSchemaAdd, RoutesSchemaAddResult

router = APIRouter(
    prefix="/road",
    tags=["Road"],
)


@router.get("")
async def get_road(
    uow: UOWDep,
) -> List[RoutesSchema]:
    """
    Получение всех маршруты
    """

    road = await CitiesService().get_cities(uow)
    return road


@router.post("")
async def add_road(
    city: RoutesSchemaAdd,
    uow: UOWDep,
) -> RoutesSchemaAddResult:
    """
    Добавление нового маршрута
    """
    road_id = await CitiesService().add_cities(uow, city)
    if road_id is None:
        raise HTTPException(status_code=404, detail="City not found")

    return RoutesSchemaAddResult(id=road_id)

from typing import List
from fastapi import APIRouter, HTTPException

from services.fsp import RoutesService
from api.dependencies import UOWDep
from schemas.fsp import (
    RoutesSchema,
    RoutesSchemaAdd,
    RoutesSchemaAddResult,
)

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

    road = await RoutesService().get_cities(uow)
    return road


@router.post("")
async def add_road(
    rout: RoutesSchemaAdd,
    uow: UOWDep,
) -> RoutesSchemaAddResult:
    """
    Добавление нового маршрута
    """
    road_id = await RoutesService().add_cities(uow, rout)
    if road_id is None:
        raise HTTPException(status_code=404, detail="City not found")

    return RoutesSchemaAddResult(id=road_id)

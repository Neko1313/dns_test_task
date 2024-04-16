from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound

from src.model.fsp import Cities, Routes
from src.utils.repository import SQLAlchemyRepository


class CitiesRepository(SQLAlchemyRepository):
    model = Cities

    async def add_one(self, data: dict) -> int:
        query = select(self.model.id).where(self.model.name == data["name"])
        try:
            res = await self.session.execute(query)
            city_id = res.scalar_one()
            return city_id
        except NoResultFound:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()


class RoutesRepository(SQLAlchemyRepository):
    model = Routes

    async def add_one(self, data: dict) -> None | int:
        query_1 = select(Cities.id).where(Cities.id == data["from_city_id"])
        query_2 = select(Cities.id).where(Cities.id == data["to_city_id"])

        is_from_city_id = False
        is_to_city_id = False
        try:
            res_1 = await self.session.execute(query_1)
            from_city_id = res_1.scalar_one()
            is_from_city_id = True
        except NoResultFound:
            return None

        try:
            res_2 = await self.session.execute(query_2)
            to_city_id = res_2.scalar_one()
            is_to_city_id = True
        except NoResultFound:
            return None

        if is_from_city_id and is_to_city_id:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()

        return None

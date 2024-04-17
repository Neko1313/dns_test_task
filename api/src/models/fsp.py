from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres import Base
from schemas.fsp import CitiesSchema, RoutesSchema


class Cities(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    def to_read_model(self) -> CitiesSchema:
        return CitiesSchema(
            id=self.id,
            name=self.name,
        )


class Routes(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    to_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    distance: Mapped[int] = mapped_column(Integer)

    def to_read_model(self) -> RoutesSchema:
        return RoutesSchema(
            id=self.id,
            from_city_id=self.from_city_id,
            to_city_id=self.to_city_id,
            distance=self.distance,
        )

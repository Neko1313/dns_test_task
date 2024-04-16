from typing import Optional

from pydantic import BaseModel


class CitiesSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoutesSchema(BaseModel):
    id: int
    from_city_id: int
    to_city_id: int
    distance: int

    class Config:
        from_attributes = True


class RoutesSchemaAddResult(BaseModel):
    id: int
    
class RoutesSchemaAdd(BaseModel):
    from_city_id: int
    to_city_id: int
    distance: int


class CitiesSchemaAdd(BaseModel):
    name: str


class CitiesSchemaAddResult(BaseModel):
    id: int


class CitiesSchemaPathResult(BaseModel):
    distance: int
    targetCity: str


class CitiesSchemaPath(BaseModel):
    city: str
    result: CitiesSchemaPathResult

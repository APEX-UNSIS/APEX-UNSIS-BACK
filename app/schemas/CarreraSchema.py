from typing import Optional

from pydantic import BaseModel


class CarreraBase(BaseModel):
    id_carrera: str
    nombre_carrera: str


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    nombre_carrera: Optional[str] = None


class Carrera(CarreraBase):
    class Config:
        from_attributes = True
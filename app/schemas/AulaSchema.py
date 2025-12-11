from typing import Optional

from pydantic import BaseModel


class AulaBase(BaseModel):
    id_aula: str
    nombre_aula: str
    capacidad: int
    is_disable: bool = False


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):
    nombre_aula: Optional[str] = None
    capacidad: Optional[int] = None
    is_disable: Optional[bool] = None


class Aula(AulaBase):
    class Config:
        orm_mode = True
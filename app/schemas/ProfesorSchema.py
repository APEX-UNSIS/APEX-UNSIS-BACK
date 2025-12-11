from typing import Optional

from pydantic import BaseModel


class ProfesorBase(BaseModel):
    id_profesor: str
    nombre_profesor: str
    is_disable: bool = False


class ProfesorCreate(ProfesorBase):
    pass


class ProfesorUpdate(BaseModel):
    nombre_profesor: Optional[str] = None
    is_disable: Optional[bool] = None


class Profesor(ProfesorBase):
    class Config:
        orm_mode = True
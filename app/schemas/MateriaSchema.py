from typing import Optional

from pydantic import BaseModel


class MateriaBase(BaseModel):
    id_materia: str
    nombre_materia: str


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(BaseModel):
    nombre_materia: Optional[str] = None


class Materia(MateriaBase):
    class Config:
        orm_mode = True
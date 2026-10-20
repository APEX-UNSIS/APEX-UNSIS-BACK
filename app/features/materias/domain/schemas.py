from typing import Optional

from pydantic import BaseModel


class MateriaBase(BaseModel):
    id_materia: str
    nombre_materia: str
    es_academia: Optional[bool] = False
    tipo_examen: Optional[str] = 'plataforma'  # 'escrito' o 'plataforma'


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(BaseModel):
    nombre_materia: Optional[str] = None
    es_academia: Optional[bool] = None
    tipo_examen: Optional[str] = None


class Materia(MateriaBase):
    class Config:
        from_attributes = True
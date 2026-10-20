from typing import Optional

from pydantic import BaseModel

from app.schemas.CarreraSchema import Carrera


class GrupoEscolarBase(BaseModel):
    id_grupo: str
    nombre_grupo: str
    numero_alumnos: int
    id_carrera: str


class GrupoEscolarCreate(GrupoEscolarBase):
    pass


class GrupoEscolarUpdate(BaseModel):
    nombre_grupo: Optional[str] = None
    numero_alumnos: Optional[int] = None
    id_carrera: Optional[str] = None


class GrupoEscolar(GrupoEscolarBase):
    carrera: Optional[Carrera] = None

    class Config:
        from_attributes = True
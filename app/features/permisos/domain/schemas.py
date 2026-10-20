from typing import Optional

from pydantic import BaseModel

from app.features.materias.domain.schemas import Materia
from app.features.profesores.domain.schemas import Profesor


class PermisoSinodalBase(BaseModel):
    id_regla: str
    id_profesor: str
    id_materia: str


class PermisoSinodalCreate(PermisoSinodalBase):
    pass


class PermisoSinodalUpdate(BaseModel):
    id_profesor: Optional[str] = None
    id_materia: Optional[str] = None


class PermisoSinodal(PermisoSinodalBase):
    profesor: Optional[Profesor] = None
    materia: Optional[Materia] = None

    class Config:
        from_attributes = True
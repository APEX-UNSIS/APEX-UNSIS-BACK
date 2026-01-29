from datetime import time
from typing import Optional

from pydantic import BaseModel

from app.schemas.AulaSchema import Aula
from app.schemas.GrupoEscolarSchema import GrupoEscolar
from app.schemas.MateriaSchema import Materia
from app.schemas.PeriodoAcademicoSchema import PeriodoAcademico
from app.schemas.ProfesorSchema import Profesor


class HorarioClaseBase(BaseModel):
    id_horario_clase: str
    id_periodo: str
    id_materia: str
    id_grupo: str
    id_profesor: str
    id_aula: str
    dia_semana: int
    hora_inicio: time
    hora_fin: time


class HorarioClaseCreate(HorarioClaseBase):
    pass


class HorarioClaseUpdate(BaseModel):
    id_periodo: Optional[str] = None
    id_materia: Optional[str] = None
    id_grupo: Optional[str] = None
    id_profesor: Optional[str] = None
    id_aula: Optional[str] = None
    dia_semana: Optional[int] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None


class HorarioClase(HorarioClaseBase):
    periodo: Optional[PeriodoAcademico] = None
    materia: Optional[Materia] = None
    grupo: Optional[GrupoEscolar] = None
    profesor: Optional[Profesor] = None
    aula: Optional[Aula] = None

    class Config:
        from_attributes = True
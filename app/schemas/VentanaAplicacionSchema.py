from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.schemas.PeriodoAcademicoSchema import PeriodoAcademico
from app.schemas.TipoEvaluacionSchema import TipoEvaluacion


class VentanaAplicacionBase(BaseModel):
    id_ventana: str
    id_periodo: str
    id_evaluacion: str
    fecha_inicio_examenes: date
    fecha_fin_examenes: date


class VentanaAplicacionCreate(VentanaAplicacionBase):
    pass


class VentanaAplicacionUpdate(BaseModel):
    id_periodo: Optional[str] = None
    id_evaluacion: Optional[str] = None
    fecha_inicio_examenes: Optional[date] = None
    fecha_fin_examenes: Optional[date] = None


class VentanaAplicacion(VentanaAplicacionBase):
    periodo: Optional[PeriodoAcademico] = None
    evaluacion: Optional[TipoEvaluacion] = None

    class Config:
        from_attributes = True
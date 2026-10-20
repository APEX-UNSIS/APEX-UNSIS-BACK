from datetime import date
from typing import List, Optional, Dict
from pydantic import BaseModel


class GenerarCalendarioRequest(BaseModel):
    fecha_inicio: date
    id_evaluacion: str  # Parcial 1, 2, 3, Ordinario
    dias_inhabiles: Optional[List[date]] = []  # Días donde no se aplicarán exámenes


class GenerarCalendarioResponse(BaseModel):
    solicitudes_creadas: int
    conflictos: List[str]
    advertencias: List[str]
    periodo_determinado: Optional[str] = None
    semestre_determinado: Optional[str] = None  # 2025-2026A o 2026B


class RechazarCalendarioRequest(BaseModel):
    id_carrera: str
    id_periodo: str
    id_evaluacion: str
    motivo_rechazo: str


class CalendarioCarreraResponse(BaseModel):
    id_carrera: str
    nombre_carrera: str
    id_periodo: str
    nombre_periodo: Optional[str]
    id_evaluacion: str
    nombre_evaluacion: Optional[str]
    jefe_carrera: Optional[str]
    fecha_envio: Optional[date]
    total_examenes: int
    estado: str  # 'pendiente', 'aprobado', 'rechazado'
    observaciones: Optional[str] = None
    examenes: List[Dict]

from datetime import date
from typing import List, Optional
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

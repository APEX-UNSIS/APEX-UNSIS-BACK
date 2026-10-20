from typing import List

from app.features.asignaciones_sinodales.domain.models import AsignacionSinodal
from app.features.asignaciones_sinodales.infrastructure.repository import AsignacionSinodalRepository
from app.features.asignaciones_sinodales.domain.schemas import AsignacionSinodalCreate, AsignacionSinodalUpdate
from app.core.base_service import BaseService


class AsignacionSinodalService(BaseService[AsignacionSinodal, AsignacionSinodalCreate, AsignacionSinodalUpdate]):
    def __init__(self, repository: AsignacionSinodalRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_solicitud(self, id_horario: str) -> List[AsignacionSinodal]:
        return self.repository.get_by_solicitud(id_horario)

    def get_by_profesor(self, id_profesor: str) -> List[AsignacionSinodal]:
        return self.repository.get_by_profesor(id_profesor)
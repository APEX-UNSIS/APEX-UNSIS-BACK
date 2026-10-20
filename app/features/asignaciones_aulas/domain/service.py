from typing import List

from app.features.asignaciones_aulas.domain.models import AsignacionAula
from app.features.asignaciones_aulas.infrastructure.repository import AsignacionAulaRepository
from app.features.asignaciones_aulas.domain.schemas import AsignacionAulaCreate, AsignacionAulaUpdate
from app.core.base_service import BaseService


class AsignacionAulaService(BaseService[AsignacionAula, AsignacionAulaCreate, AsignacionAulaUpdate]):
    def __init__(self, repository: AsignacionAulaRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_solicitud(self, id_horario: str) -> List[AsignacionAula]:
        return self.repository.get_by_solicitud(id_horario)

    def get_by_aula(self, id_aula: str) -> List[AsignacionAula]:
        return self.repository.get_by_aula(id_aula)

    def get_by_profesor_aplicador(self, id_profesor: str) -> List[AsignacionAula]:
        return self.repository.get_by_profesor_aplicador(id_profesor)
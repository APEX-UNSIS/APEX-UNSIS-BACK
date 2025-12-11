from typing import List

from app.models.AsignacionAula import AsignacionAula
from app.repositories.AsignacionAulaRepository import AsignacionAulaRepository
from app.schemas.AsignacionAulaSchema import AsignacionAulaCreate, AsignacionAulaUpdate
from app.services.base_service import BaseService


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
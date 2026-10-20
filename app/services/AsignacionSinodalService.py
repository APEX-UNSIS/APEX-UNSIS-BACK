from typing import List

from app.models.AsignacionSinodal import AsignacionSinodal
from app.repositories.AsignacionSinodalRepository import AsignacionSinodalRepository
from app.schemas.AsignacionSinodalSchema import AsignacionSinodalCreate, AsignacionSinodalUpdate
from app.services.base_service import BaseService


class AsignacionSinodalService(BaseService[AsignacionSinodal, AsignacionSinodalCreate, AsignacionSinodalUpdate]):
    def __init__(self, repository: AsignacionSinodalRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_solicitud(self, id_horario: str) -> List[AsignacionSinodal]:
        return self.repository.get_by_solicitud(id_horario)

    def get_by_profesor(self, id_profesor: str) -> List[AsignacionSinodal]:
        return self.repository.get_by_profesor(id_profesor)
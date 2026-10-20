from typing import List
from datetime import date

from app.models.SolicitudExamen import SolicitudExamen
from app.repositories.SolicitudRepository import SolicitudRepository
from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
from app.schemas.SolicitudExamenSchema import SolicitudExamenCreate, SolicitudExamenUpdate
from app.services.base_service import BaseService


class SolicitudService(BaseService[SolicitudExamen, SolicitudExamenCreate, SolicitudExamenUpdate]):
    def __init__(self, repository: SolicitudRepository):
        super().__init__(repository)
        self.repository = repository

    def get_with_relations(self, id_horario: str) -> SolicitudExamen:
        return self.repository.get_with_relations(id_horario)

    def get_by_estado(self, estado: EstadoSolicitud, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.repository.get_by_estado(estado, skip, limit)

    def get_by_fecha(self, fecha: date, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.repository.get_by_fecha(fecha, skip, limit)

    def get_by_periodo(self, id_periodo: str, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.repository.get_by_periodo(id_periodo, skip, limit)
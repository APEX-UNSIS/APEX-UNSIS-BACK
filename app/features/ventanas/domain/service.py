from typing import Optional

from app.features.ventanas.domain.models import VentanaAplicacion
from app.features.ventanas.infrastructure.repository import VentanaRepository
from app.features.ventanas.domain.schemas import VentanaAplicacionCreate, VentanaAplicacionUpdate
from app.core.base_service import BaseService


class VentanaService(BaseService[VentanaAplicacion, VentanaAplicacionCreate, VentanaAplicacionUpdate]):
    def __init__(self, repository: VentanaRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_periodo_evaluacion(self, id_periodo: str, id_evaluacion: str) -> Optional[VentanaAplicacion]:
        return self.repository.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
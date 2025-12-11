from typing import Optional

from app.models.VentanaAplicacion import VentanaAplicacion
from app.repositories.VentanaRepository import VentanaRepository
from app.schemas.VentanaAplicacionSchema import VentanaAplicacionCreate, VentanaAplicacionUpdate
from app.services.base_service import BaseService


class VentanaService(BaseService[VentanaAplicacion, VentanaAplicacionCreate, VentanaAplicacionUpdate]):
    def __init__(self, repository: VentanaRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_periodo_evaluacion(self, id_periodo: str, id_evaluacion: str) -> Optional[VentanaAplicacion]:
        return self.repository.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
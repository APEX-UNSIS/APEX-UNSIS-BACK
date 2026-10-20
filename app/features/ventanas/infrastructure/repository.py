from typing import List, Optional
from sqlalchemy.orm import Session

from app.features.ventanas.domain.models import VentanaAplicacion
from app.core.base_repository import BaseRepository
from app.features.ventanas.domain.schemas import VentanaAplicacionCreate, VentanaAplicacionUpdate


class VentanaRepository(BaseRepository[VentanaAplicacion, VentanaAplicacionCreate, VentanaAplicacionUpdate]):
    def __init__(self, db: Session):
        super().__init__(VentanaAplicacion, db)

    def get_by_id(self, id_ventana: str) -> Optional[VentanaAplicacion]:
        return self.db.query(VentanaAplicacion).filter(VentanaAplicacion.id_ventana == id_ventana).first()

    def get_by_periodo_evaluacion(self, id_periodo: str, id_evaluacion: str) -> Optional[VentanaAplicacion]:
        return self.db.query(VentanaAplicacion).filter(
            VentanaAplicacion.id_periodo == id_periodo,
            VentanaAplicacion.id_evaluacion == id_evaluacion
        ).first()
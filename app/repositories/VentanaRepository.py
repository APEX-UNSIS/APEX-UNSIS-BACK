from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.VentanaAplicacion import VentanaAplicacion
from app.repositories.base_repository import BaseRepository
from app.schemas.VentanaAplicacionSchema import VentanaAplicacionCreate, VentanaAplicacionUpdate


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
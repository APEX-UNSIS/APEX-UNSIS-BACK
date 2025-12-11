from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import date

from app.models.SolicitudExamen import SolicitudExamen
from app.repositories.base_repository import BaseRepository
from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
from app.schemas.SolicitudExamenSchema import SolicitudExamenCreate, SolicitudExamenUpdate


class SolicitudRepository(BaseRepository[SolicitudExamen, SolicitudExamenCreate, SolicitudExamenUpdate]):
    def __init__(self, db: Session):
        super().__init__(SolicitudExamen, db)

    def get_by_id(self, id_horario: str) -> Optional[SolicitudExamen]:
        return self.db.query(SolicitudExamen).filter(SolicitudExamen.id_horario == id_horario).first()

    def get_with_relations(self, id_horario: str) -> Optional[SolicitudExamen]:
        return self.db.query(SolicitudExamen).options(
            joinedload(SolicitudExamen.periodo),
            joinedload(SolicitudExamen.evaluacion),
            joinedload(SolicitudExamen.materia)
        ).filter(SolicitudExamen.id_horario == id_horario).first()

    def get_by_estado(self, estado: EstadoSolicitud, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.db.query(SolicitudExamen).filter(
            SolicitudExamen.estado == estado.value
        ).offset(skip).limit(limit).all()

    def get_by_fecha(self, fecha: date, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.db.query(SolicitudExamen).filter(
            SolicitudExamen.fecha_examen == fecha
        ).offset(skip).limit(limit).all()

    def get_by_periodo(self, id_periodo: str, skip: int = 0, limit: int = 100) -> List[SolicitudExamen]:
        return self.db.query(SolicitudExamen).filter(
            SolicitudExamen.id_periodo == id_periodo
        ).offset(skip).limit(limit).all()
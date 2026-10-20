from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import date, time

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

    def get_by_periodo_evaluacion(self, id_periodo: str, id_evaluacion: str) -> List[SolicitudExamen]:
        return self.db.query(SolicitudExamen).filter(
            SolicitudExamen.id_periodo == id_periodo,
            SolicitudExamen.id_evaluacion == id_evaluacion
        ).all()

    def get_by_fecha_hora_aula(self, fecha: date, hora_inicio: time, hora_fin: time, id_aula: str) -> List[SolicitudExamen]:
        """Obtiene solicitudes que tienen conflicto con una aula en fecha/hora específica"""
        from app.models.AsignacionAula import AsignacionAula
        return self.db.query(SolicitudExamen).join(
            AsignacionAula, SolicitudExamen.id_horario == AsignacionAula.id_horario
        ).filter(
            SolicitudExamen.fecha_examen == fecha,
            SolicitudExamen.estado != 2,  # No rechazadas
            AsignacionAula.id_aula == id_aula,
            # Verificar que haya solapamiento en horarios
            SolicitudExamen.hora_inicio < hora_fin,
            SolicitudExamen.hora_fin > hora_inicio
        ).all()
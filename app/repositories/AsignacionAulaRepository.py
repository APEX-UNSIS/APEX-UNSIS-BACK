from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, time

from app.models.AsignacionAula import AsignacionAula
from app.repositories.base_repository import BaseRepository
from app.schemas.AsignacionAulaSchema import AsignacionAulaCreate, AsignacionAulaUpdate


class AsignacionAulaRepository(BaseRepository[AsignacionAula, AsignacionAulaCreate, AsignacionAulaUpdate]):
    def __init__(self, db: Session):
        super().__init__(AsignacionAula, db)

    def get_by_id(self, id_examen_aula: str) -> Optional[AsignacionAula]:
        return self.db.query(AsignacionAula).filter(AsignacionAula.id_examen_aula == id_examen_aula).first()

    def get_by_solicitud(self, id_horario: str) -> List[AsignacionAula]:
        return self.db.query(AsignacionAula).filter(
            AsignacionAula.id_horario == id_horario
        ).all()

    def get_by_aula(self, id_aula: str) -> List[AsignacionAula]:
        return self.db.query(AsignacionAula).filter(
            AsignacionAula.id_aula == id_aula
        ).all()

    def get_by_profesor_aplicador(self, id_profesor: str) -> List[AsignacionAula]:
        return self.db.query(AsignacionAula).filter(
            AsignacionAula.id_profesor_aplicador == id_profesor
        ).all()

    def get_by_aula_fecha_hora(self, id_aula: str, fecha, hora_inicio: time, hora_fin: time) -> List[AsignacionAula]:
        """Verifica si un aula está ocupada en una fecha/hora específica"""
        from app.models.SolicitudExamen import SolicitudExamen
        return self.db.query(AsignacionAula).join(
            SolicitudExamen, AsignacionAula.id_horario == SolicitudExamen.id_horario
        ).filter(
            AsignacionAula.id_aula == id_aula,
            SolicitudExamen.fecha_examen == fecha,
            SolicitudExamen.estado != 2,  # No rechazadas
            SolicitudExamen.hora_inicio < hora_fin,
            SolicitudExamen.hora_fin > hora_inicio
        ).all()
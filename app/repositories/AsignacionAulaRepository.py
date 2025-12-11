from typing import List, Optional
from sqlalchemy.orm import Session

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
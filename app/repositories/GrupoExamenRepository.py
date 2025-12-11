from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.GrupoExamen import GrupoExamen
from app.repositories.base_repository import BaseRepository
from app.schemas.GrupoExamenSchema import GrupoExamenCreate, GrupoExamenUpdate


class GrupoExamenRepository(BaseRepository[GrupoExamen, GrupoExamenCreate, GrupoExamenUpdate]):
    def __init__(self, db: Session):
        super().__init__(GrupoExamen, db)

    def get_by_id(self, id_examen_grupo: str) -> Optional[GrupoExamen]:
        return self.db.query(GrupoExamen).filter(GrupoExamen.id_examen_grupo == id_examen_grupo).first()

    def get_by_solicitud(self, id_horario: str) -> List[GrupoExamen]:
        return self.db.query(GrupoExamen).filter(
            GrupoExamen.id_horario == id_horario
        ).all()

    def get_by_grupo(self, id_grupo: str) -> List[GrupoExamen]:
        return self.db.query(GrupoExamen).filter(
            GrupoExamen.id_grupo == id_grupo
        ).all()
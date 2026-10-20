from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.features.grupos.domain.models import GrupoEscolar
from app.core.base_repository import BaseRepository
from app.features.grupos.domain.schemas import GrupoEscolarCreate, GrupoEscolarUpdate


class GrupoRepository(BaseRepository[GrupoEscolar, GrupoEscolarCreate, GrupoEscolarUpdate]):
    def __init__(self, db: Session):
        super().__init__(GrupoEscolar, db)

    def get_by_id(self, id_grupo: str) -> Optional[GrupoEscolar]:
        return self.db.query(GrupoEscolar).filter(GrupoEscolar.id_grupo == id_grupo).first()

    def get_with_carrera(self, id_grupo: str) -> Optional[GrupoEscolar]:
        return self.db.query(GrupoEscolar).options(
            joinedload(GrupoEscolar.carrera)
        ).filter(GrupoEscolar.id_grupo == id_grupo).first()

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[GrupoEscolar]:
        return self.db.query(GrupoEscolar).filter(
            GrupoEscolar.id_carrera == id_carrera
        ).offset(skip).limit(limit).all()
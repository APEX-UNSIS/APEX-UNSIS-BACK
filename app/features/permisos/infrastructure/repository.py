from typing import List, Optional
from sqlalchemy.orm import Session

from app.features.permisos.domain.models import PermisoSinodal
from app.core.base_repository import BaseRepository
from app.features.permisos.domain.schemas import PermisoSinodalCreate, PermisoSinodalUpdate


class PermisoRepository(BaseRepository[PermisoSinodal, PermisoSinodalCreate, PermisoSinodalUpdate]):
    def __init__(self, db: Session):
        super().__init__(PermisoSinodal, db)

    def get_by_id(self, id_regla: str) -> Optional[PermisoSinodal]:
        return self.db.query(PermisoSinodal).filter(PermisoSinodal.id_regla == id_regla).first()

    def get_by_profesor_materia(self, id_profesor: str, id_materia: str) -> Optional[PermisoSinodal]:
        return self.db.query(PermisoSinodal).filter(
            PermisoSinodal.id_profesor == id_profesor,
            PermisoSinodal.id_materia == id_materia
        ).first()

    def get_by_profesor(self, id_profesor: str) -> List[PermisoSinodal]:
        return self.db.query(PermisoSinodal).filter(
            PermisoSinodal.id_profesor == id_profesor
        ).all()

    def get_by_materia(self, id_materia: str) -> List[PermisoSinodal]:
        return self.db.query(PermisoSinodal).filter(
            PermisoSinodal.id_materia == id_materia
        ).all()
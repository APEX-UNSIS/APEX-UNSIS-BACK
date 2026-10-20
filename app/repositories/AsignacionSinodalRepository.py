from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.AsignacionSinodal import AsignacionSinodal
from app.repositories.base_repository import BaseRepository
from app.schemas.AsignacionSinodalSchema import AsignacionSinodalCreate, AsignacionSinodalUpdate


class AsignacionSinodalRepository(BaseRepository[AsignacionSinodal, AsignacionSinodalCreate, AsignacionSinodalUpdate]):
    def __init__(self, db: Session):
        super().__init__(AsignacionSinodal, db)

    def get_by_id(self, id_examen_sinodal: str) -> Optional[AsignacionSinodal]:
        return self.db.query(AsignacionSinodal).filter(AsignacionSinodal.id_examen_sinodal == id_examen_sinodal).first()

    def get_by_solicitud(self, id_horario: str) -> List[AsignacionSinodal]:
        return self.db.query(AsignacionSinodal).filter(
            AsignacionSinodal.id_horario == id_horario
        ).all()

    def get_by_profesor(self, id_profesor: str) -> List[AsignacionSinodal]:
        return self.db.query(AsignacionSinodal).filter(
            AsignacionSinodal.id_profesor == id_profesor
        ).all()
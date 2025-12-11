from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.HorarioClase import HorarioClase
from app.repositories.base_repository import BaseRepository
from app.schemas.HorarioClaseSchema import HorarioClaseCreate, HorarioClaseUpdate


class HorarioRepository(BaseRepository[HorarioClase, HorarioClaseCreate, HorarioClaseUpdate]):
    def __init__(self, db: Session):
        super().__init__(HorarioClase, db)

    def get_by_id(self, id_horario: str) -> Optional[HorarioClase]:
        return self.db.query(HorarioClase).filter(HorarioClase.id_horario_clase == id_horario).first()

    def get_with_relations(self, id_horario: str) -> Optional[HorarioClase]:
        return self.db.query(HorarioClase).options(
            joinedload(HorarioClase.periodo),
            joinedload(HorarioClase.materia),
            joinedload(HorarioClase.grupo),
            joinedload(HorarioClase.profesor),
            joinedload(HorarioClase.aula)
        ).filter(HorarioClase.id_horario_clase == id_horario).first()

    def get_by_profesor(self, id_profesor: str, skip: int = 0, limit: int = 100) -> List[HorarioClase]:
        return self.db.query(HorarioClase).filter(
            HorarioClase.id_profesor == id_profesor
        ).offset(skip).limit(limit).all()

    def get_by_grupo(self, id_grupo: str, skip: int = 0, limit: int = 100) -> List[HorarioClase]:
        return self.db.query(HorarioClase).filter(
            HorarioClase.id_grupo == id_grupo
        ).offset(skip).limit(limit).all()
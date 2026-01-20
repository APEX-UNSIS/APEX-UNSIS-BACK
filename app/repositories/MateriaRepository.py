from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Materia import Materia
from app.repositories.base_repository import BaseRepository
from app.schemas.MateriaSchema import MateriaCreate, MateriaUpdate


class MateriaRepository(BaseRepository[Materia, MateriaCreate, MateriaUpdate]):
    def __init__(self, db: Session):
        super().__init__(Materia, db)

    def get_by_id(self, id_materia: str) -> Optional[Materia]:
        return self.db.query(Materia).filter(Materia.id_materia == id_materia).first()

    def get_by_nombre(self, nombre: str) -> Optional[Materia]:
        return self.db.query(Materia).filter(Materia.nombre_materia == nombre).first()

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[Materia]:
        """Obtiene materias por carrera a través de horarios y grupos"""
        from app.models.HorarioClase import HorarioClase
        from app.models.GrupoEscolar import GrupoEscolar
        return self.db.query(Materia).join(
            HorarioClase, Materia.id_materia == HorarioClase.id_materia
        ).join(
            GrupoEscolar, HorarioClase.id_grupo == GrupoEscolar.id_grupo
        ).filter(
            GrupoEscolar.id_carrera == id_carrera
        ).distinct().offset(skip).limit(limit).all()
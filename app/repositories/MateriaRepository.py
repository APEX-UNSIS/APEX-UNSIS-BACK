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

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100, id_periodo: Optional[str] = None, id_grupo: Optional[str] = None) -> List[Materia]:
        """Obtiene materias por carrera a través de horarios y grupos, con filtros opcionales por periodo y grupo"""
        from app.models.HorarioClase import HorarioClase
        from app.models.GrupoEscolar import GrupoEscolar
        
        query = self.db.query(Materia).join(
            HorarioClase, Materia.id_materia == HorarioClase.id_materia
        ).join(
            GrupoEscolar, HorarioClase.id_grupo == GrupoEscolar.id_grupo
        ).filter(
            GrupoEscolar.id_carrera == id_carrera
        )
        
        # Filtrar por periodo si se especifica
        if id_periodo:
            query = query.filter(HorarioClase.id_periodo == id_periodo)
        
        # Filtrar por grupo si se especifica
        if id_grupo:
            query = query.filter(HorarioClase.id_grupo == id_grupo)
        
        return query.distinct().offset(skip).limit(limit).all()
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Profesor import Profesor
from app.repositories.base_repository import BaseRepository
from app.schemas.ProfesorSchema import ProfesorCreate, ProfesorUpdate


class ProfesorRepository(BaseRepository[Profesor, ProfesorCreate, ProfesorUpdate]):
    def __init__(self, db: Session):
        super().__init__(Profesor, db)

    def get_by_id(self, id_profesor: str) -> Optional[Profesor]:
        return self.db.query(Profesor).filter(Profesor.id_profesor == id_profesor).first()

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.db.query(Profesor).filter(
            Profesor.is_disable == False
        ).offset(skip).limit(limit).all()

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[Profesor]:
        """Obtiene profesores que imparten clases en una carrera específica"""
        from app.models.HorarioClase import HorarioClase
        from app.models.GrupoEscolar import GrupoEscolar
        return self.db.query(Profesor).join(
            HorarioClase, Profesor.id_profesor == HorarioClase.id_profesor
        ).join(
            GrupoEscolar, HorarioClase.id_grupo == GrupoEscolar.id_grupo
        ).filter(
            GrupoEscolar.id_carrera == id_carrera,
            Profesor.is_disable == False
        ).distinct().offset(skip).limit(limit).all()

    def get_sinodales_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[Profesor]:
        """Obtiene todos los profesores de una carrera que pueden ser sinodales"""
        from app.models.HorarioClase import HorarioClase
        from app.models.GrupoEscolar import GrupoEscolar
        
        print(f"[SINODALES] Iniciando búsqueda de sinodales para carrera {id_carrera}")
        
        # Obtener TODOS los profesores que imparten clases en la carrera
        # Estos son los profesores que pueden ser sinodales
        profesores = self.db.query(Profesor).join(
            HorarioClase, Profesor.id_profesor == HorarioClase.id_profesor
        ).join(
            GrupoEscolar, HorarioClase.id_grupo == GrupoEscolar.id_grupo
        ).filter(
            GrupoEscolar.id_carrera == id_carrera,
            Profesor.is_disable == False
        ).distinct().offset(skip).limit(limit).all()
        
        print(f"[SINODALES] Profesores encontrados para carrera {id_carrera}: {len(profesores)}")
        
        return profesores
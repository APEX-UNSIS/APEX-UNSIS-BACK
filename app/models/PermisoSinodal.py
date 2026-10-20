from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class PermisoSinodal(Base):
    __tablename__ = 'permisos_sinodales_por_materia'

    id_regla = Column(String(20), primary_key=True)
    id_profesor = Column(String(20), ForeignKey('profesores.id_profesor'))
    id_materia = Column(String(20), ForeignKey('materias.id_materia'))

    profesor = relationship("Profesor", back_populates="permisos_sinodales")
    materia = relationship("Materia", back_populates="permisos_sinodales")
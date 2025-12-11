from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Materia(Base):
    __tablename__ = 'materias'

    id_materia = Column(String(20), primary_key=True)
    nombre_materia = Column(String(50))

    horarios_clase = relationship("HorarioClase", back_populates="materia")
    permisos_sinodales = relationship("PermisoSinodal", back_populates="materia")
    solicitudes_examen = relationship("SolicitudExamen", back_populates="materia")
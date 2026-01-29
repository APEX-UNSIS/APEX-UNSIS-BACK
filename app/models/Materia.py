from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Materia(Base):
    __tablename__ = 'materias'

    id_materia = Column(String(20), primary_key=True)
    nombre_materia = Column(String(50))
    es_academia = Column(Boolean, default=False)  # True si es academia, False si es materia regular
    tipo_examen = Column(String(20), default='plataforma')  # 'escrito' o 'plataforma'

    horarios_clase = relationship("HorarioClase", back_populates="materia")
    permisos_sinodales = relationship("PermisoSinodal", back_populates="materia")
    solicitudes_examen = relationship("SolicitudExamen", back_populates="materia")
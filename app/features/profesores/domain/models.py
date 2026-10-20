from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Profesor(Base):
    __tablename__ = 'profesores'

    id_profesor = Column(String(20), primary_key=True)
    nombre_profesor = Column(String(60))
    is_disable = Column(Boolean, default=False)

    horarios_clase = relationship("HorarioClase", back_populates="profesor")
    permisos_sinodales = relationship("PermisoSinodal", back_populates="profesor")
    aplicaciones_examen = relationship("AsignacionAula", back_populates="profesor_aplicador",
                                       foreign_keys="AsignacionAula.id_profesor_aplicador")
    asignaciones_sinodales = relationship("AsignacionSinodal", back_populates="profesor")
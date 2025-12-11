from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AsignacionSinodal(Base):
    __tablename__ = 'asignacion_sinodales'

    id_examen_sinodal = Column(String(20), primary_key=True)
    id_horario = Column(String(20), ForeignKey('solicitudes_de_examen.id_horario'))
    id_profesor = Column(String(20), ForeignKey('profesores.id_profesor'))

    solicitud = relationship("SolicitudExamen", back_populates="sinodales_asignados")
    profesor = relationship("Profesor", back_populates="asignaciones_sinodales")
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AsignacionAula(Base):
    __tablename__ = 'asignacion_aulas_y_aplicadores'

    id_examen_aula = Column(String(20), primary_key=True)
    id_horario = Column(String(20), ForeignKey('solicitudes_de_examen.id_horario'))
    id_aula = Column(String(20), ForeignKey('aulas.id_aula'))
    id_profesor_aplicador = Column(String(20), ForeignKey('profesores.id_profesor'))

    solicitud = relationship("SolicitudExamen", back_populates="aulas_asignadas")
    aula = relationship("Aula", back_populates="asignaciones_examen")
    profesor_aplicador = relationship("Profesor", back_populates="aplicaciones_examen",
                                      foreign_keys=[id_profesor_aplicador])
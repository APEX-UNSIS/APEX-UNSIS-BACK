from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class PeriodoAcademico(Base):
    __tablename__ = 'periodos_academicos'

    id_periodo = Column(String(20), primary_key=True)
    nombre_periodo = Column(String(30))

    horarios_clase = relationship("HorarioClase", back_populates="periodo")
    ventanas_aplicacion = relationship("VentanaAplicacion", back_populates="periodo")
    solicitudes_examen = relationship("SolicitudExamen", back_populates="periodo")
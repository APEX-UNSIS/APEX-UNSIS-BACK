from sqlalchemy import Column, String, ForeignKey, Date, Time, Integer, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class SolicitudExamen(Base):
    __tablename__ = 'solicitudes_de_examen'

    id_horario = Column(String(20), primary_key=True)
    id_periodo = Column(String(20), ForeignKey('periodos_academicos.id_periodo'))
    id_evaluacion = Column(String(20), ForeignKey('tipos_de_evaluacion.id_evaluacion'))
    id_materia = Column(String(20), ForeignKey('materias.id_materia'))
    fecha_examen = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    estado = Column(Integer, default=0)  # 0: pendiente, 1: aprobado, 2: rechazado; Maybe hacerlo un Enum
    motivo_rechazo = Column(String(255), nullable=True)
    is_manualmente_editado = Column(Boolean, default=False)

    periodo = relationship("PeriodoAcademico", back_populates="solicitudes_examen")
    evaluacion = relationship("TipoEvaluacion", back_populates="solicitudes_examen")
    materia = relationship("Materia", back_populates="solicitudes_examen")
    grupos_examen = relationship("GrupoExamen", back_populates="solicitud")
    aulas_asignadas = relationship("AsignacionAula", back_populates="solicitud")
    sinodales_asignados = relationship("AsignacionSinodal", back_populates="solicitud")

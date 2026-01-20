from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(String(50), primary_key=True)
    nombre_usuario = Column(String(100), nullable=False)
    id_carrera = Column(String(20), ForeignKey('carreras.id_carrera'), nullable=True)
    contraseña = Column(String(255), nullable=False)  # Almacenará el hash de la contraseña
    rol = Column(String(20), nullable=False)  # 'admin', 'jefe', 'servicios'
    is_active = Column(Boolean, default=True)

    # Relación con Carrera (lazy loading para evitar problemas de importación circular)
    # carrera = relationship("Carrera", backref="usuarios", lazy="select")

from enum import Enum


class EstadoSolicitud(int, Enum):
    PENDIENTE = 0
    APROBADO = 1
    RECHAZADO = 2
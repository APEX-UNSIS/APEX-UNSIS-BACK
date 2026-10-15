"""
Ejemplo de cómo proteger endpoints con autenticación JWT
Este archivo muestra diferentes formas de aplicar autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import (
    get_current_active_user,
    require_admin,
    require_roles,
    require_jefe_or_admin
)
from app.schemas.UsuarioSchema import UsuarioResponse

# Crear el router
router = APIRouter(
    prefix="/ejemplo",
    tags=["ejemplo protegido"]
)


# EJEMPLO 1: Endpoint público (sin protección)
@router.get("/publico")
def endpoint_publico():
    """Cualquiera puede acceder a este endpoint sin autenticación"""
    return {
        "mensaje": "Este endpoint es público",
        "requiere_auth": False
    }


# EJEMPLO 2: Endpoint que requiere estar autenticado (cualquier usuario)
@router.get("/protegido")
def endpoint_protegido(
    current_user: UsuarioResponse = Depends(get_current_active_user)
):
    """Solo usuarios autenticados pueden acceder"""
    return {
        "mensaje": f"Hola {current_user.nombre_usuario}",
        "tu_rol": current_user.rol,
        "requiere_auth": True
    }


# EJEMPLO 3: Endpoint solo para administradores
@router.delete("/eliminar-todo")
def endpoint_solo_admin(
    current_user: UsuarioResponse = Depends(require_admin)
):
    """Solo administradores pueden acceder"""
    return {
        "mensaje": "Acción crítica ejecutada",
        "ejecutado_por": current_user.nombre_usuario,
        "rol": current_user.rol
    }


# EJEMPLO 4: Endpoint para múltiples roles específicos
@router.post("/aprobar-solicitud")
def aprobar_solicitud(
    solicitud_id: int,
    current_user: UsuarioResponse = Depends(require_roles(["admin", "jefe"]))
):
    """Solo admin y jefe pueden aprobar solicitudes"""
    return {
        "mensaje": f"Solicitud {solicitud_id} aprobada",
        "aprobada_por": current_user.nombre_usuario,
        "rol": current_user.rol
    }


# EJEMPLO 5: Endpoint con lógica condicional según el rol
@router.get("/datos-sensibles")
def obtener_datos_sensibles(
    current_user: UsuarioResponse = Depends(get_current_active_user)
):
    """Todos pueden acceder pero ven diferentes datos según su rol"""
    
    # Datos base que todos pueden ver
    respuesta = {
        "usuario": current_user.nombre_usuario,
        "mensaje": "Acceso concedido"
    }
    
    # Los admins ven todo
    if current_user.rol == "admin":
        respuesta["datos_completos"] = {
            "total_usuarios": 150,
            "total_solicitudes": 300,
            "configuracion_sistema": "..."
        }
    
    # Los jefes ven datos de su carrera
    elif current_user.rol == "jefe":
        respuesta["datos_carrera"] = {
            "id_carrera": current_user.id_carrera,
            "solicitudes_pendientes": 10
        }
    
    # Servicios ve datos básicos
    elif current_user.rol == "servicios":
        respuesta["datos_servicios"] = {
            "solicitudes_asignadas": 5
        }
    
    return respuesta


# EJEMPLO 6: Proteger todo un router con dependencias
router_protegido = APIRouter(
    prefix="/admin-area",
    tags=["admin"],
    dependencies=[Depends(require_admin)]  # Todas las rutas requieren admin
)

@router_protegido.get("/estadisticas")
def estadisticas_admin():
    """Automáticamente requiere admin por el router"""
    return {"total_usuarios": 100, "activos": 95}

@router_protegido.get("/configuracion")
def configuracion_admin():
    """También requiere admin automáticamente"""
    return {"modo": "producción", "debug": False}


# EJEMPLO 7: Validación adicional en el endpoint
@router.get("/mi-carrera/{carrera_id}")
def datos_carrera(
    carrera_id: str,
    current_user: UsuarioResponse = Depends(get_current_active_user)
):
    """Solo el jefe de esa carrera o admin puede ver los datos"""
    
    # Admin puede ver cualquier carrera
    if current_user.rol == "admin":
        return {
            "carrera_id": carrera_id,
            "datos": "Datos completos de la carrera"
        }
    
    # Jefe solo puede ver su carrera
    elif current_user.rol == "jefe":
        if current_user.id_carrera != carrera_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta carrera"
            )
        return {
            "carrera_id": carrera_id,
            "datos": "Datos de tu carrera"
        }
    
    # Otros roles no tienen acceso
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver datos de carreras"
        )


# EJEMPLO 8: Obtener información del usuario actual
@router.get("/mi-perfil")
def mi_perfil(
    current_user: UsuarioResponse = Depends(get_current_active_user)
):
    """El usuario puede ver su propio perfil"""
    return {
        "perfil": {
            "id": current_user.id_usuario,
            "nombre": current_user.nombre_usuario,
            "email": current_user.email,
            "rol": current_user.rol,
            "carrera": current_user.id_carrera,
            "activo": current_user.is_active,
            "creado": current_user.created_at,
            "ultimo_login": current_user.last_login
        }
    }


# EJEMPLO 9: Operación que modifica datos del usuario
@router.put("/actualizar-perfil")
def actualizar_perfil(
    nombre_usuario: str,
    current_user: UsuarioResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """El usuario puede actualizar su propio perfil"""
    # Aquí iría la lógica para actualizar en la BD
    return {
        "mensaje": "Perfil actualizado",
        "nuevo_nombre": nombre_usuario,
        "usuario": current_user.id_usuario
    }


# EJEMPLO 10: Listar usuarios (con restricciones por rol)
@router.get("/usuarios", response_model=List[dict])
def listar_usuarios(
    current_user: UsuarioResponse = Depends(require_jefe_or_admin)
):
    """Admin ve todos, jefe solo de su carrera"""
    
    # Simulación - en realidad consultarías la BD
    if current_user.rol == "admin":
        return [
            {"id": "user1", "nombre": "Usuario 1"},
            {"id": "user2", "nombre": "Usuario 2"}
        ]
    else:  # jefe
        return [
            {"id": "user1", "nombre": "Usuario de mi carrera"}
        ]

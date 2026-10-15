"""
Middleware y dependencias de autenticación para proteger rutas
"""
from typing import List
from fastapi import Depends, HTTPException, status
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.UsuarioSchema import UsuarioResponse


def require_roles(allowed_roles: List[str]):
    """
    Dependencia para requerir que el usuario tenga uno de los roles especificados
    
    Uso:
        @router.get("/admin-only", dependencies=[Depends(require_roles(["admin"]))])
        def admin_endpoint():
            return {"message": "Solo admin"}
    
    Args:
        allowed_roles: Lista de roles permitidos ['admin', 'jefe', 'servicios']
    """
    def role_checker(current_user: UsuarioResponse = Depends(get_current_user)) -> UsuarioResponse:
        if current_user.rol not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos suficientes. Se requiere uno de estos roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


def require_admin(current_user: UsuarioResponse = Depends(get_current_user)) -> UsuarioResponse:
    """
    Dependencia para requerir rol de administrador
    
    Uso:
        @router.delete("/users/{id}", dependencies=[Depends(require_admin)])
        def delete_user(id: str):
            return {"message": "Usuario eliminado"}
    """
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user


def require_jefe_or_admin(current_user: UsuarioResponse = Depends(get_current_user)) -> UsuarioResponse:
    """
    Dependencia para requerir rol de jefe o administrador
    """
    if current_user.rol not in ["admin", "jefe"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de jefe o administrador"
        )
    return current_user


def get_current_active_user(current_user: UsuarioResponse = Depends(get_current_user)) -> UsuarioResponse:
    """
    Verifica que el usuario esté activo
    
    Uso:
        @router.get("/profile")
        def get_profile(current_user: UsuarioResponse = Depends(get_current_active_user)):
            return current_user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Usuario inactivo"
        )
    return current_user

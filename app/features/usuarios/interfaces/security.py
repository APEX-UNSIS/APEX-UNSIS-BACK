"""
Dependencias de autenticación (JWT) y autorización (control de roles).

Único punto de entrada para `Depends(...)` de seguridad en los routers:
`get_current_user`, `require_admin`, `require_roles`, etc.
"""
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.features.usuarios.domain.schemas import UsuarioResponse
from app.features.usuarios.domain.service import UsuarioService
from app.features.usuarios.infrastructure.repository import UsuarioRepository

settings = get_settings()

# Configuración JWT
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 días

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    repository = UsuarioRepository(db)
    return UsuarioService(repository)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UsuarioResponse:
    """
    Obtiene el usuario actual desde el token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    service = get_usuario_service(db)
    usuario = service.get(username)
    if usuario is None:
        raise credentials_exception

    return UsuarioResponse.model_validate(usuario)


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

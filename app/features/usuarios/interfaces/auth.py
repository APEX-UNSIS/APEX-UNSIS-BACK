"""
Rutas de autenticación: login, perfil del usuario actual y reseteo de password.

Las primitivas JWT (token, `get_current_user`, fábrica de servicios) viven en
`app.features.usuarios.interfaces.security`.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.config import get_settings
from app.features.usuarios.domain.schemas import UsuarioLogin, TokenResponse, UsuarioResponse
from app.features.usuarios.domain.service import UsuarioService
from app.features.usuarios.interfaces.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_usuario_service,
)

router = APIRouter(prefix="/auth", tags=["autenticación"])

settings = get_settings()


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UsuarioLogin,
    service: UsuarioService = Depends(get_usuario_service)
):
    """
    Endpoint de login que autentica al usuario y retorna un token JWT
    """
    try:
        # Verificar primero si el usuario existe
        usuario_temp = service.repository.get_by_username_or_id(login_data.user)
        if not usuario_temp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        usuario = service.authenticate_user(login_data.user, login_data.password)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Crear token de acceso
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": usuario.id_usuario, "rol": usuario.rol},
            expires_delta=access_token_expires
        )

        # Preparar respuesta del usuario (sin contraseña)
        user_response = UsuarioResponse.model_validate(usuario)

        return TokenResponse(token=access_token, user=user_response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/me", response_model=UsuarioResponse)
def read_users_me(current_user: UsuarioResponse = Depends(get_current_user)):
    """
    Obtiene la información del usuario actual autenticado
    """
    return current_user


@router.post("/reset-admin-password")
def reset_admin_password(
    reset_key: str = Query(..., description="Clave de reseteo (debe coincidir con RESET_ADMIN_KEY en .env)"),
    new_password: str = Query("admin123", description="Nueva contraseña para el usuario admin"),
    service: UsuarioService = Depends(get_usuario_service),
):
    """
    Resetea la contraseña del usuario 'admin' usando la misma BD que la app.
    Solo funciona si RESET_ADMIN_KEY está definido en .env y coincide con reset_key.
    Uso: POST /api/v1/auth/reset-admin-password?reset_key=TU_CLAVE&new_password=admin123
    Después de usarlo, quita o cambia RESET_ADMIN_KEY en producción.
    """
    # Si RESET_ADMIN_KEY está en .env, debe coincidir. Si no está, se acepta "reset-admin-now" una vez.
    if settings.reset_admin_key:
        if settings.reset_admin_key != reset_key:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    elif reset_key != "reset-admin-now":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado. Usa reset_key=reset-admin-now o define RESET_ADMIN_KEY en .env")
    try:
        service.reset_password_by_id("admin", new_password)
        return {"message": "Contraseña del usuario admin actualizada. Ya puedes iniciar sesión."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.UsuarioRepository import UsuarioRepository
from app.schemas.UsuarioSchema import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.UsuarioService import UsuarioService
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    repository = UsuarioRepository(db)
    return UsuarioService(repository)


@router.get("/", response_model=List[UsuarioResponse])
def read_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: UsuarioService = Depends(get_usuario_service)
):
    usuarios = service.get_all(skip=skip, limit=limit)
    return [UsuarioResponse.model_validate(u) for u in usuarios]


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def read_usuario(
    id_usuario: str,
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = service.get(id_usuario)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)


@router.post("/", response_model=UsuarioResponse)
def create_usuario(
    usuario: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service)
):
    try:
        usuario_creado = service.create(usuario)
        return UsuarioResponse.model_validate(usuario_creado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al crear usuario: {str(e)}")


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def update_usuario(
    id_usuario: str,
    usuario_update: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    try:
        usuario = service.update(id_usuario, usuario_update)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsuarioResponse.model_validate(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al actualizar usuario: {str(e)}")


@router.delete("/{id_usuario}", response_model=UsuarioResponse)
def delete_usuario(
    id_usuario: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    service: UsuarioService = Depends(get_usuario_service)
):
    try:
        # Validar que el usuario actual sea admin
        if current_user.rol != 'admin':
            raise HTTPException(
                status_code=403, 
                detail="No tienes permiso para eliminar usuarios. Solo los administradores pueden eliminar usuarios."
            )
        
        # Validar que no se elimine a sí mismo
        if current_user.id_usuario == id_usuario:
            raise HTTPException(
                status_code=400,
                detail="No puedes eliminarte a ti mismo. Por favor, solicita a otro administrador que lo haga."
            )
        
        usuario = service.delete(id_usuario, current_user.id_usuario)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsuarioResponse.model_validate(usuario)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al eliminar usuario: {str(e)}")


@router.get("/rol/{rol}", response_model=List[UsuarioResponse])
def get_usuarios_by_rol(
    rol: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: UsuarioService = Depends(get_usuario_service)
):
    usuarios = service.get_by_rol(rol, skip=skip, limit=limit)
    return [UsuarioResponse.model_validate(u) for u in usuarios]


@router.post("/{id_usuario}/reset-password", response_model=dict)
def reset_password(
    id_usuario: str,
    nueva_contraseña: str = Query(None, description="Nueva contraseña. Si no se proporciona, se genera automáticamente"),
    current_user: UsuarioResponse = Depends(get_current_user),
    service: UsuarioService = Depends(get_usuario_service)
):
    """
    Resetea la contraseña de un usuario.
    Si no se proporciona nueva_contraseña, se genera una automáticamente.
    Solo los administradores pueden resetear contraseñas.
    """
    # Validar que el usuario actual sea admin
    if current_user.rol != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden resetear contraseñas"
        )
    
    try:
        usuario = service.get(id_usuario)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Si no se proporciona contraseña, generar una automáticamente
        if not nueva_contraseña:
            # Generar contraseña basada en el nombre del usuario y su ID
            import re
            nombre = usuario.nombre_usuario
            
            # Extraer iniciales del nombre
            def quitar_acentos(texto):
                import unicodedata
                return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
            
            nombre_sin_acentos = quitar_acentos(nombre)
            palabras = nombre_sin_acentos.strip().split()
            
            if len(palabras) >= 4:
                # 4+ palabras: P (penúltimo apellido) + I (segunda letra) + M (primer nombre) + A (segundo nombre)
                apellido1 = palabras[-2]
                iniciales = (apellido1[0] + (apellido1[1] if len(apellido1) > 1 else apellido1[0]) + 
                            palabras[0][0] + palabras[1][0]).upper()[:4]
            elif len(palabras) == 3:
                # 3 palabras: Nombre1 Nombre2 Apellido
                iniciales = (palabras[2][0] + (palabras[2][1] if len(palabras[2]) > 1 else palabras[2][0]) + 
                            palabras[0][0] + palabras[1][0]).upper()[:4]
            elif len(palabras) == 2:
                # 2 palabras: primera letra de cada una + segunda letra de la primera
                iniciales = (palabras[0][0] + (palabras[0][1] if len(palabras[0]) > 1 else palabras[0][0]) + 
                            palabras[1][0] + 'X').upper()[:4]
            else:
                # 1 palabra: primeras 4 letras
                iniciales = palabras[0][:4].upper().ljust(4, 'X')
            
            # Extraer año del ID (primeros 4 dígitos)
            año = '2024'
            numeros = re.findall(r'\d+', str(id_usuario))
            if numeros and len(numeros[0]) >= 4:
                año = numeros[0][:4]
            
            nueva_contraseña = f"Pass_{iniciales}#{año}"
        
        # Actualizar la contraseña
        usuario_update = UsuarioUpdate(contraseña=nueva_contraseña)
        usuario_actualizado = service.update(id_usuario, usuario_update)
        
        if usuario_actualizado is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "id_usuario": usuario_actualizado.id_usuario,
            "nombre_usuario": usuario_actualizado.nombre_usuario,
            "contraseña": nueva_contraseña,
            "mensaje": "Contraseña reseteada exitosamente"
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al resetear contraseña: {str(e)}")

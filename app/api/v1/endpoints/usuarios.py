from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.UsuarioRepository import UsuarioRepository
from app.schemas.UsuarioSchema import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.UsuarioService import UsuarioService

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


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def update_usuario(
    id_usuario: str,
    usuario_update: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = service.update(id_usuario, usuario_update)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)


@router.delete("/{id_usuario}", response_model=UsuarioResponse)
def delete_usuario(
    id_usuario: str,
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = service.delete(id_usuario)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)


@router.get("/rol/{rol}", response_model=List[UsuarioResponse])
def get_usuarios_by_rol(
    rol: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: UsuarioService = Depends(get_usuario_service)
):
    usuarios = service.get_by_rol(rol, skip=skip, limit=limit)
    return [UsuarioResponse.model_validate(u) for u in usuarios]

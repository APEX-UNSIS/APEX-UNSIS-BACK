from typing import Dict, List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.CalendarioExamenService import CalendarioExamenService
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.UsuarioSchema import UsuarioResponse
from app.schemas.CalendarioSchema import GenerarCalendarioRequest, GenerarCalendarioResponse

router = APIRouter(prefix="/calendario", tags=["calendario"])


@router.post("/generar", response_model=GenerarCalendarioResponse)
def generar_calendario_examenes(
    request: GenerarCalendarioRequest,
    eliminar_existentes: bool = False,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera un calendario de exámenes para la carrera del jefe logueado.
    
    Genera 5 días de exámenes comenzando desde fecha_inicio (excluyendo días inhábiles y fines de semana).
    El periodo y semestre se determinan automáticamente según la fecha_inicio:
    - Octubre-Enero: Semestre A (ej: 2025-2026A)
    - Marzo-Julio: Semestre B (ej: 2026B)
    
    Args:
        request: Datos para generar el calendario:
            - fecha_inicio: Fecha de inicio (se generan 5 días hábiles)
            - id_evaluacion: ID del tipo de evaluación (Parcial 1, 2, 3, Ordinario)
            - dias_inhabiles: Lista opcional de fechas donde no se aplicarán exámenes
        eliminar_existentes: Si True, elimina solicitudes existentes antes de generar
    
    Returns:
        GenerarCalendarioResponse con información del proceso
    """
    # Validar que el usuario sea jefe de carrera y tenga carrera asignada
    if current_user.rol != 'jefe':
        raise HTTPException(
            status_code=403,
            detail="Solo los jefes de carrera pueden generar calendarios de exámenes"
        )
    
    if not current_user.id_carrera:
        raise HTTPException(
            status_code=400,
            detail="El usuario no tiene una carrera asignada"
        )
    
    try:
        servicio = CalendarioExamenService(db)
        resultado = servicio.generar_calendario_examenes(
            id_carrera=current_user.id_carrera,
            fecha_inicio=request.fecha_inicio,
            id_evaluacion=request.id_evaluacion,
            dias_inhabiles=request.dias_inhabiles or [],
            eliminar_existentes=eliminar_existentes
        )
        
        return GenerarCalendarioResponse(**resultado)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar calendario: {str(e)}")


@router.get("/verificar", response_model=Dict)
def verificar_calendario_existente(
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verifica si existe un calendario de exámenes para la carrera del jefe logueado.
    
    Returns:
        Dict con información: {
            'existe': bool,
            'mensaje': str
        }
    """
    if current_user.rol != 'jefe':
        raise HTTPException(
            status_code=403,
            detail="Solo los jefes de carrera pueden verificar calendarios"
        )
    
    if not current_user.id_carrera:
        raise HTTPException(
            status_code=400,
            detail="El usuario no tiene una carrera asignada"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.HorarioRepository import HorarioRepository
    
    solicitud_repo = SolicitudRepository(db)
    horario_repo = HorarioRepository(db)
    
    # Obtener todas las solicitudes que pertenecen a materias de esta carrera
    horarios_carrera = horario_repo.get_by_carrera(current_user.id_carrera)
    if not horarios_carrera:
        return {
            'existe': False,
            'mensaje': 'No hay horarios registrados para esta carrera'
        }
    
    materias_carrera = set(h.id_materia for h in horarios_carrera)
    todas_solicitudes = solicitud_repo.get_all()
    
    solicitudes_carrera = [
        s for s in todas_solicitudes 
        if s.id_materia in materias_carrera
    ]
    
    if solicitudes_carrera:
        return {
            'existe': True,
            'mensaje': f'Existen {len(solicitudes_carrera)} solicitudes de examen para esta carrera',
            'total_solicitudes': len(solicitudes_carrera)
        }
    else:
        return {
            'existe': False,
            'mensaje': 'No existe un calendario de exámenes generado para esta carrera'
        }


@router.get("/obtener", response_model=List[Dict])
def obtener_calendario_carrera(
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las solicitudes de examen de la carrera del jefe logueado
    con información completa (materia, grupos, aula, profesor, etc.)
    
    Returns:
        Lista de solicitudes con información completa
    """
    if current_user.rol != 'jefe':
        raise HTTPException(
            status_code=403,
            detail="Solo los jefes de carrera pueden obtener calendarios"
        )
    
    if not current_user.id_carrera:
        raise HTTPException(
            status_code=400,
            detail="El usuario no tiene una carrera asignada"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.HorarioRepository import HorarioRepository
    from app.repositories.GrupoExamenRepository import GrupoExamenRepository
    from app.repositories.AsignacionAulaRepository import AsignacionAulaRepository
    from sqlalchemy.orm import joinedload
    
    solicitud_repo = SolicitudRepository(db)
    horario_repo = HorarioRepository(db)
    grupo_examen_repo = GrupoExamenRepository(db)
    asignacion_aula_repo = AsignacionAulaRepository(db)
    
    # Obtener horarios de la carrera
    horarios_carrera = horario_repo.get_by_carrera(current_user.id_carrera)
    if not horarios_carrera:
        print(f"[DEBUG] No hay horarios para la carrera {current_user.id_carrera}")
        return []
    
    materias_carrera = set(h.id_materia for h in horarios_carrera)
    print(f"[DEBUG] Materias de la carrera {current_user.id_carrera}: {len(materias_carrera)} materias")
    
    # Obtener solicitudes con relaciones cargadas
    from app.models.SolicitudExamen import SolicitudExamen
    todas_solicitudes = db.query(SolicitudExamen).options(
        joinedload(SolicitudExamen.materia),
        joinedload(SolicitudExamen.periodo),
        joinedload(SolicitudExamen.evaluacion)
    ).all()
    
    print(f"[DEBUG] Total de solicitudes en BD: {len(todas_solicitudes)}")
    
    # Filtrar solicitudes de la carrera
    solicitudes_carrera = [
        s for s in todas_solicitudes 
        if s.id_materia in materias_carrera
    ]
    
    print(f"[DEBUG] Solicitudes filtradas para carrera {current_user.id_carrera}: {len(solicitudes_carrera)}")
    
    # Construir respuesta con información completa
    resultado = []
    for solicitud in solicitudes_carrera:
        try:
            # Obtener grupos asociados con relación cargada
            from app.models.GrupoExamen import GrupoExamen
            grupos_examen = db.query(GrupoExamen).options(
                joinedload(GrupoExamen.grupo)
            ).filter(GrupoExamen.id_horario == solicitud.id_horario).all()
            
            grupos = []
            for ge in grupos_examen:
                if ge.grupo:
                    grupos.append(ge.grupo.nombre_grupo)
                else:
                    grupos.append(ge.id_grupo)
            
            # Solo incluir solicitudes que tengan grupos asociados
            # Si no hay grupos, la solicitud no está completa y no debe mostrarse
            if not grupos:
                continue
            
            # Obtener aula asignada con relaciones cargadas
            from app.models.AsignacionAula import AsignacionAula
            asignaciones_aula = db.query(AsignacionAula).options(
                joinedload(AsignacionAula.aula),
                joinedload(AsignacionAula.profesor_aplicador)
            ).filter(AsignacionAula.id_horario == solicitud.id_horario).all()
            
            aula = None
            profesor_aplicador = None
            if asignaciones_aula and len(asignaciones_aula) > 0:
                if asignaciones_aula[0].aula:
                    aula = asignaciones_aula[0].aula.nombre_aula
                if asignaciones_aula[0].profesor_aplicador:
                    profesor_aplicador = asignaciones_aula[0].profesor_aplicador.nombre_profesor
            
            # Formatear fecha y hora
            fecha_str = solicitud.fecha_examen.strftime('%d/%m/%Y') if solicitud.fecha_examen else None
            hora_str = None
            if solicitud.hora_inicio and solicitud.hora_fin:
                hora_inicio_str = solicitud.hora_inicio.strftime('%H:%M')
                hora_fin_str = solicitud.hora_fin.strftime('%H:%M')
                hora_str = f"{hora_inicio_str}-{hora_fin_str}"
            
            resultado.append({
                'id_horario': solicitud.id_horario,
                'materia': solicitud.materia.nombre_materia if solicitud.materia else None,
                'grupos': grupos if grupos else [],
                'profesor': profesor_aplicador,
                'fecha': fecha_str,
                'hora': hora_str,
                'aula': aula,
                'estado': solicitud.estado,
                'periodo': solicitud.periodo.nombre_periodo if solicitud.periodo else None,
                'evaluacion': solicitud.evaluacion.nombre_evaluacion if solicitud.evaluacion else None
            })
        except Exception as e:
            # Si hay un error con una solicitud, continuar con las demás
            print(f"Error procesando solicitud {solicitud.id_horario}: {str(e)}")
            continue
    
    # Ordenar por fecha
    resultado.sort(key=lambda x: x['fecha'] if x['fecha'] else '')
    
    return resultado

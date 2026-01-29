from typing import Dict, List, Optional
from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.CalendarioExamenService import CalendarioExamenService
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.UsuarioSchema import UsuarioResponse
from app.schemas.CalendarioSchema import (
    GenerarCalendarioRequest, 
    GenerarCalendarioResponse,
    RechazarCalendarioRequest
)

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
    
    IMPORTANTE: Si ya existe un calendario para el mismo periodo y evaluación, se eliminará
    automáticamente antes de generar el nuevo para evitar duplicados.
    
    Args:
        request: Datos para generar el calendario:
            - fecha_inicio: Fecha de inicio (se generan 5 días hábiles)
            - id_evaluacion: ID del tipo de evaluación (Parcial 1, 2, 3, Ordinario)
            - dias_inhabiles: Lista opcional de fechas donde no se aplicarán exámenes
        eliminar_existentes: (Deprecated) Ya no se usa, siempre se eliminan los existentes del mismo periodo/evaluación
    
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
    
    # Obtener todas las solicitudes que pertenecen a materias de esta carrera (sin límite)
    horarios_carrera = horario_repo.get_by_carrera(current_user.id_carrera, skip=0, limit=10000)
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
    
    # Obtener horarios de la carrera (sin límite para obtener todos)
    horarios_carrera = horario_repo.get_by_carrera(current_user.id_carrera, skip=0, limit=10000)
    if not horarios_carrera:
        print(f"[DEBUG] No hay horarios para la carrera {current_user.id_carrera}")
        return []
    
    materias_carrera = set(h.id_materia for h in horarios_carrera)
    # Mapa (id_materia, id_grupo, id_periodo) -> horario (primer slot por dia_semana, hora_inicio) para aula y profesor titular del horario de clases
    horario_por_materia_grupo_periodo = {}
    for h in horarios_carrera:
        if not h.id_materia or not h.id_grupo or not h.id_periodo:
            continue
        key = (h.id_materia, h.id_grupo, h.id_periodo)
        if key not in horario_por_materia_grupo_periodo:
            horario_por_materia_grupo_periodo[key] = h
        else:
            actual = horario_por_materia_grupo_periodo[key]
            d_a = actual.dia_semana if actual.dia_semana is not None else 99
            d_h = h.dia_semana if h.dia_semana is not None else 99
            if (d_h, h.hora_inicio or time(23, 59)) < (d_a, actual.hora_inicio or time(23, 59)):
                horario_por_materia_grupo_periodo[key] = h
    
    print(f"[DEBUG] Horarios de la carrera {current_user.id_carrera}: {len(horarios_carrera)} horarios, mapa materia-grupo-periodo: {len(horario_por_materia_grupo_periodo)}")
    
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
    
    # Obtener aula asignada al examen (fallback si no hay horario)
    from app.models.AsignacionAula import AsignacionAula
    from collections import defaultdict
    
    # Contar (fecha, hora, id_aula) para detectar conflictos (misma aula misma fecha/hora)
    cuenta_aula_fecha_hora = defaultdict(int)
    for s in solicitudes_carrera:
        asig = db.query(AsignacionAula).filter(AsignacionAula.id_horario == s.id_horario).first()
        if asig and asig.id_aula and s.fecha_examen and s.hora_inicio:
            key = (s.fecha_examen, s.hora_inicio, asig.id_aula)
            cuenta_aula_fecha_hora[key] += 1
    
    # Construir respuesta: una fila por (solicitud, grupo) con grupo, materia, maestro titular, fecha, hora, aula
    resultado = []
    for solicitud in solicitudes_carrera:
        try:
            from app.models.GrupoExamen import GrupoExamen
            grupos_examen = db.query(GrupoExamen).options(
                joinedload(GrupoExamen.grupo)
            ).filter(GrupoExamen.id_horario == solicitud.id_horario).all()
            
            if not grupos_examen:
                continue
            
            asignaciones_aula = db.query(AsignacionAula).options(
                joinedload(AsignacionAula.aula),
                joinedload(AsignacionAula.profesor_aplicador)
            ).filter(AsignacionAula.id_horario == solicitud.id_horario).all()
            aula_fallback = None
            if asignaciones_aula and asignaciones_aula[0].aula:
                aula_fallback = asignaciones_aula[0].aula.nombre_aula
            
            fecha_str = solicitud.fecha_examen.strftime('%d/%m/%Y') if solicitud.fecha_examen else None
            hora_str = None
            if solicitud.hora_inicio and solicitud.hora_fin:
                hora_str = f"{solicitud.hora_inicio.strftime('%H:%M')}-{solicitud.hora_fin.strftime('%H:%M')}"
            
            for ge in grupos_examen:
                id_grupo = ge.id_grupo
                nombre_grupo = ge.grupo.nombre_grupo if ge.grupo else id_grupo
                key_h = (solicitud.id_materia, id_grupo, solicitud.id_periodo)
                h_clase = horario_por_materia_grupo_periodo.get(key_h)
                # Profesor del horario de clases; aula en blanco si no hay asignación (paso 1: ver todo sin aula)
                if h_clase:
                    profesor_display = h_clase.profesor.nombre_profesor if h_clase.profesor else None
                else:
                    profesor_display = None
                if not profesor_display and asignaciones_aula and asignaciones_aula[0].profesor_aplicador:
                    profesor_display = asignaciones_aula[0].profesor_aplicador.nombre_profesor
                # Aula: asignada, del horario o en blanco (pendiente)
                id_aula_sol = asignaciones_aula[0].id_aula if asignaciones_aula else None
                if asignaciones_aula and asignaciones_aula[0].aula:
                    aula_display = asignaciones_aula[0].aula.nombre_aula
                elif h_clase and h_clase.aula:
                    aula_display = h_clase.aula.nombre_aula
                else:
                    aula_display = ''
                aula_conflicto = False
                if id_aula_sol and solicitud.fecha_examen and solicitud.hora_inicio:
                    key = (solicitud.fecha_examen, solicitud.hora_inicio, id_aula_sol)
                    aula_conflicto = cuenta_aula_fecha_hora.get(key, 0) > 1
                if not id_aula_sol:
                    aula_conflicto = True  # Aula pendiente (ej. área salud): marcar en rojo
                
                resultado.append({
                    'id_horario': solicitud.id_horario,
                    'id_materia': solicitud.id_materia,
                    'asignatura': solicitud.id_materia,
                    'materia': solicitud.materia.nombre_materia if solicitud.materia else None,
                    'grupo': nombre_grupo,
                    'id_grupo': id_grupo,
                    'grupos': [nombre_grupo],
                    'profesor': profesor_display,
                    'fecha': fecha_str,
                    'hora': hora_str,
                    'aula': aula_display,
                    'aula_conflicto': aula_conflicto,
                    'estado': solicitud.estado,
                    'periodo': solicitud.periodo.nombre_periodo if solicitud.periodo else None,
                    'id_periodo': solicitud.id_periodo,
                    'evaluacion': solicitud.evaluacion.nombre_evaluacion if solicitud.evaluacion else None,
                    'id_evaluacion': solicitud.id_evaluacion,
                    'motivo_rechazo': solicitud.motivo_rechazo
                })
        except Exception as e:
            print(f"Error procesando solicitud {solicitud.id_horario}: {str(e)}")
            continue
    
    # Ordenar por asignatura (id_materia) ascendente, luego por grupo (como en API materias)
    resultado.sort(key=lambda x: (x.get('id_materia') or '', x.get('grupo') or ''))
    
    return resultado


@router.post("/enviar", response_model=Dict)
def enviar_calendario_servicios_escolares(
    id_periodo: str = Query(..., description="ID del periodo académico"),
    id_evaluacion: str = Query(..., description="ID del tipo de evaluación"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía el calendario de exámenes de la carrera a Servicios Escolares para revisión.
    Cambia el estado de todas las solicitudes del periodo y evaluación a PENDIENTE.
    
    Args:
        id_periodo: ID del periodo académico
        id_evaluacion: ID del tipo de evaluación
    
    Returns:
        Dict con información del proceso
    """
    if current_user.rol != 'jefe':
        raise HTTPException(
            status_code=403,
            detail="Solo los jefes de carrera pueden enviar calendarios"
        )
    
    if not current_user.id_carrera:
        raise HTTPException(
            status_code=400,
            detail="El usuario no tiene una carrera asignada"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.HorarioRepository import HorarioRepository
    from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
    from app.schemas.SolicitudExamenSchema import SolicitudExamenUpdate
    
    solicitud_repo = SolicitudRepository(db)
    horario_repo = HorarioRepository(db)
    
    # Obtener horarios de la carrera
    horarios_carrera = horario_repo.get_by_carrera(current_user.id_carrera, skip=0, limit=10000)
    materias_carrera = set(h.id_materia for h in horarios_carrera if h.id_periodo == id_periodo)
    
    # Obtener solicitudes del periodo y evaluación
    solicitudes = solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
    
    # Filtrar solo las de la carrera del jefe
    solicitudes_carrera = [
        s for s in solicitudes 
        if s.id_materia in materias_carrera
    ]
    
    if not solicitudes_carrera:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron exámenes para enviar. Asegúrate de haber generado el calendario primero."
        )
    
    # Cambiar estado a PENDIENTE (0) y limpiar motivo_rechazo
    actualizadas = 0
    for solicitud in solicitudes_carrera:
        update_data = SolicitudExamenUpdate(
            estado=EstadoSolicitud.PENDIENTE,
            motivo_rechazo=None
        )
        solicitud_repo.update(solicitud.id_horario, update_data)
        actualizadas += 1
    
    db.commit()
    
    return {
        'mensaje': f'Calendario enviado a Servicios Escolares exitosamente',
        'solicitudes_enviadas': actualizadas,
        'periodo': id_periodo,
        'evaluacion': id_evaluacion
    }


@router.get("/servicios-escolares", response_model=List[Dict])
def obtener_calendarios_servicios_escolares(
    estado: Optional[str] = Query(None, description="Filtrar por estado: 'pendiente', 'aprobado', 'rechazado'"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los calendarios agrupados por carrera para Servicios Escolares.
    Optimizado: una sola query con joinedload y batch de carreras/jefes (sin N+1).
    """
    if current_user.rol != 'servicios':
        raise HTTPException(
            status_code=403,
            detail="Solo Servicios Escolares puede acceder a esta información"
        )
    
    from app.models.SolicitudExamen import SolicitudExamen
    from app.models.GrupoExamen import GrupoExamen
    from app.models.AsignacionAula import AsignacionAula
    from app.models.Carrera import Carrera
    from app.models.Usuario import Usuario
    from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
    from sqlalchemy.orm import joinedload

    # Una sola query con todas las relaciones necesarias (evita N+1)
    query = db.query(SolicitudExamen).options(
        joinedload(SolicitudExamen.materia),
        joinedload(SolicitudExamen.periodo),
        joinedload(SolicitudExamen.evaluacion),
        joinedload(SolicitudExamen.grupos_examen).joinedload(GrupoExamen.grupo),
        joinedload(SolicitudExamen.aulas_asignadas).joinedload(AsignacionAula.aula),
        joinedload(SolicitudExamen.aulas_asignadas).joinedload(AsignacionAula.profesor_aplicador),
    )
    if estado:
        estado_map = {
            'pendiente': EstadoSolicitud.PENDIENTE,
            'aprobado': EstadoSolicitud.APROBADO,
            'rechazado': EstadoSolicitud.RECHAZADO
        }
        if estado in estado_map:
            query = query.filter(SolicitudExamen.estado == estado_map[estado])

    todas_solicitudes = query.all()

    # Recoger id_carrera únicos para cargar carreras y jefes en batch
    id_carreras = set()
    for s in todas_solicitudes:
        if s.grupos_examen:
            ge = s.grupos_examen[0]
            if ge and ge.grupo:
                id_carreras.add(ge.grupo.id_carrera)

    carrera_map = {}
    jefe_map = {}
    if id_carreras:
        carreras = db.query(Carrera).filter(Carrera.id_carrera.in_(id_carreras)).all()
        carrera_map = {c.id_carrera: c.nombre_carrera for c in carreras}
        jefes = db.query(Usuario).filter(
            Usuario.id_carrera.in_(id_carreras),
            Usuario.rol == 'jefe'
        ).all()
        jefe_map = {j.id_carrera: j.nombre_usuario for j in jefes}

    calendarios_por_carrera = {}
    for solicitud in todas_solicitudes:
        if not solicitud.grupos_examen or not solicitud.grupos_examen[0].grupo:
            continue
        id_carrera = solicitud.grupos_examen[0].grupo.id_carrera
        clave = f"{id_carrera}-{solicitud.id_periodo}-{solicitud.id_evaluacion}"

        if clave not in calendarios_por_carrera:
            calendarios_por_carrera[clave] = {
                'id_carrera': id_carrera,
                'nombre_carrera': carrera_map.get(id_carrera, id_carrera),
                'id_periodo': solicitud.id_periodo,
                'nombre_periodo': solicitud.periodo.nombre_periodo if solicitud.periodo else None,
                'id_evaluacion': solicitud.id_evaluacion,
                'nombre_evaluacion': solicitud.evaluacion.nombre_evaluacion if solicitud.evaluacion else None,
                'jefe_carrera': jefe_map.get(id_carrera),
                'fecha_envio': None,
                'estado': 'pendiente' if solicitud.estado == EstadoSolicitud.PENDIENTE else
                         'aprobado' if solicitud.estado == EstadoSolicitud.APROBADO else 'rechazado',
                'observaciones': solicitud.motivo_rechazo,
                'examenes': []
            }

        grupos = [ge.grupo.nombre_grupo for ge in solicitud.grupos_examen if ge.grupo]
        aula = None
        profesor = None
        if solicitud.aulas_asignadas:
            a0 = solicitud.aulas_asignadas[0]
            aula = a0.aula.nombre_aula if a0.aula else None
            profesor = a0.profesor_aplicador.nombre_profesor if a0.profesor_aplicador else None

        fecha_str = solicitud.fecha_examen.strftime('%d/%m/%Y') if solicitud.fecha_examen else None
        hora_str = None
        if solicitud.hora_inicio and solicitud.hora_fin:
            hora_str = f"{solicitud.hora_inicio.strftime('%H:%M')}-{solicitud.hora_fin.strftime('%H:%M')}"

        calendarios_por_carrera[clave]['examenes'].append({
            'id_horario': solicitud.id_horario,
            'materia': solicitud.materia.nombre_materia if solicitud.materia else None,
            'grupos': grupos,
            'profesor': profesor,
            'fecha': fecha_str,
            'hora': hora_str,
            'aula': aula,
            'estado': 'pendiente' if solicitud.estado == EstadoSolicitud.PENDIENTE else
                     'aprobado' if solicitud.estado == EstadoSolicitud.APROBADO else 'rechazado'
        })

    resultado = []
    for calendario in calendarios_por_carrera.values():
        calendario['total_examenes'] = len(calendario['examenes'])
        estados = [e['estado'] for e in calendario['examenes']]
        if all(e == 'aprobado' for e in estados):
            calendario['estado'] = 'aprobado'
        elif any(e == 'rechazado' for e in estados):
            calendario['estado'] = 'rechazado'
        elif any(e == 'pendiente' for e in estados):
            calendario['estado'] = 'pendiente'
        resultado.append(calendario)

    if estado:
        resultado = [c for c in resultado if c['estado'] == estado]

    return resultado


@router.post("/aprobar-masivo", response_model=Dict)
def aprobar_calendario_masivo(
    id_carrera: str = Query(..., description="ID de la carrera"),
    id_periodo: str = Query(..., description="ID del periodo académico"),
    id_evaluacion: str = Query(..., description="ID del tipo de evaluación"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Aprueba todas las solicitudes de examen de una carrera, periodo y evaluación.
    
    Args:
        id_carrera: ID de la carrera
        id_periodo: ID del periodo académico
        id_evaluacion: ID del tipo de evaluación
    
    Returns:
        Dict con información del proceso
    """
    if current_user.rol != 'servicios':
        raise HTTPException(
            status_code=403,
            detail="Solo Servicios Escolares puede aprobar calendarios"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.HorarioRepository import HorarioRepository
    from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
    from app.schemas.SolicitudExamenSchema import SolicitudExamenUpdate
    
    solicitud_repo = SolicitudRepository(db)
    horario_repo = HorarioRepository(db)
    
    # Obtener horarios de la carrera
    horarios_carrera = horario_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
    materias_carrera = set(h.id_materia for h in horarios_carrera if h.id_periodo == id_periodo)
    
    # Obtener solicitudes del periodo y evaluación
    solicitudes = solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
    
    # Filtrar solo las de la carrera
    solicitudes_carrera = [
        s for s in solicitudes 
        if s.id_materia in materias_carrera
    ]
    
    if not solicitudes_carrera:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron exámenes para aprobar"
        )
    
    # Cambiar estado a APROBADO (1) y limpiar motivo_rechazo
    aprobadas = 0
    for solicitud in solicitudes_carrera:
        update_data = SolicitudExamenUpdate(
            estado=EstadoSolicitud.APROBADO,
            motivo_rechazo=None
        )
        solicitud_repo.update(solicitud.id_horario, update_data)
        aprobadas += 1
    
    db.commit()
    
    return {
        'mensaje': f'Calendario aprobado exitosamente',
        'solicitudes_aprobadas': aprobadas,
        'carrera': id_carrera,
        'periodo': id_periodo,
        'evaluacion': id_evaluacion
    }


@router.post("/rechazar-masivo", response_model=Dict)
def rechazar_calendario_masivo(
    request: RechazarCalendarioRequest,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rechaza todas las solicitudes de examen de una carrera, periodo y evaluación con comentarios.
    
    Args:
        id_carrera: ID de la carrera
        id_periodo: ID del periodo académico
        id_evaluacion: ID del tipo de evaluación
        motivo_rechazo: Motivo del rechazo/comentarios
    
    Returns:
        Dict con información del proceso
    """
    if current_user.rol != 'servicios':
        raise HTTPException(
            status_code=403,
            detail="Solo Servicios Escolares puede rechazar calendarios"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.HorarioRepository import HorarioRepository
    from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
    from app.schemas.SolicitudExamenSchema import SolicitudExamenUpdate
    
    solicitud_repo = SolicitudRepository(db)
    horario_repo = HorarioRepository(db)
    
    # Obtener horarios de la carrera
    horarios_carrera = horario_repo.get_by_carrera(request.id_carrera, skip=0, limit=10000)
    materias_carrera = set(h.id_materia for h in horarios_carrera if h.id_periodo == request.id_periodo)
    
    # Obtener solicitudes del periodo y evaluación
    solicitudes = solicitud_repo.get_by_periodo_evaluacion(request.id_periodo, request.id_evaluacion)
    
    # Filtrar solo las de la carrera
    solicitudes_carrera = [
        s for s in solicitudes 
        if s.id_materia in materias_carrera
    ]
    
    if not solicitudes_carrera:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron exámenes para rechazar"
        )
    
    # Cambiar estado a RECHAZADO (2) y agregar motivo
    rechazadas = 0
    for solicitud in solicitudes_carrera:
        update_data = SolicitudExamenUpdate(
            estado=EstadoSolicitud.RECHAZADO,
            motivo_rechazo=request.motivo_rechazo
        )
        solicitud_repo.update(solicitud.id_horario, update_data)
        rechazadas += 1
    
    db.commit()
    
    return {
        'mensaje': f'Calendario rechazado y regresado al jefe de carrera',
        'solicitudes_rechazadas': rechazadas,
        'carrera': request.id_carrera,
        'periodo': request.id_periodo,
        'evaluacion': request.id_evaluacion,
        'motivo_rechazo': request.motivo_rechazo
    }

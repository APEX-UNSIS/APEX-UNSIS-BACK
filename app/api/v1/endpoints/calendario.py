from typing import Dict, List, Optional
from datetime import date
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
    grupos_unicos_horarios = set()
    for h in horarios_carrera:
        if h.id_grupo:
            grupos_unicos_horarios.add(h.id_grupo)
    print(f"[DEBUG] Horarios de la carrera {current_user.id_carrera}: {len(horarios_carrera)} horarios, {len(materias_carrera)} materias únicas, {len(grupos_unicos_horarios)} grupos únicos en horarios")
    
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
                print(f"[DEBUG] Solicitud {solicitud.id_horario} no tiene grupos asociados, se omite")
                continue
            
            print(f"[DEBUG] Solicitud {solicitud.id_horario} tiene {len(grupos)} grupos asociados: {grupos}")
            
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
                'id_periodo': solicitud.id_periodo,
                'evaluacion': solicitud.evaluacion.nombre_evaluacion if solicitud.evaluacion else None,
                'id_evaluacion': solicitud.id_evaluacion,
                'motivo_rechazo': solicitud.motivo_rechazo
            })
        except Exception as e:
            # Si hay un error con una solicitud, continuar con las demás
            print(f"Error procesando solicitud {solicitud.id_horario}: {str(e)}")
            continue
    
    # Ordenar por fecha
    resultado.sort(key=lambda x: x['fecha'] if x['fecha'] else '')
    
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
    
    Args:
        estado: Filtrar por estado (opcional)
    
    Returns:
        Lista de calendarios agrupados por carrera con información completa
    """
    if current_user.rol != 'servicios':
        raise HTTPException(
            status_code=403,
            detail="Solo Servicios Escolares puede acceder a esta información"
        )
    
    from app.repositories.SolicitudRepository import SolicitudRepository
    from app.repositories.CarreraRepository import CarreraRepository
    from app.repositories.UsuarioRepository import UsuarioRepository
    from app.repositories.GrupoExamenRepository import GrupoExamenRepository
    from app.repositories.AsignacionAulaRepository import AsignacionAulaRepository
    from app.repositories.HorarioRepository import HorarioRepository
    from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
    from sqlalchemy.orm import joinedload
    
    solicitud_repo = SolicitudRepository(db)
    carrera_repo = CarreraRepository(db)
    usuario_repo = UsuarioRepository(db)
    grupo_examen_repo = GrupoExamenRepository(db)
    asignacion_aula_repo = AsignacionAulaRepository(db)
    horario_repo = HorarioRepository(db)
    
    # Obtener todas las solicitudes
    from app.models.SolicitudExamen import SolicitudExamen
    query = db.query(SolicitudExamen).options(
        joinedload(SolicitudExamen.materia),
        joinedload(SolicitudExamen.periodo),
        joinedload(SolicitudExamen.evaluacion)
    )
    
    # Filtrar por estado si se especifica
    if estado:
        estado_map = {
            'pendiente': EstadoSolicitud.PENDIENTE,
            'aprobado': EstadoSolicitud.APROBADO,
            'rechazado': EstadoSolicitud.RECHAZADO
        }
        if estado in estado_map:
            query = query.filter(SolicitudExamen.estado == estado_map[estado])
    
    todas_solicitudes = query.all()
    
    # Agrupar por carrera, periodo y evaluación
    calendarios_por_carrera = {}
    
    for solicitud in todas_solicitudes:
        # Obtener la carrera a través de los grupos
        from app.models.GrupoExamen import GrupoExamen
        grupos_examen = db.query(GrupoExamen).options(
            joinedload(GrupoExamen.grupo)
        ).filter(GrupoExamen.id_horario == solicitud.id_horario).first()
        
        if not grupos_examen or not grupos_examen.grupo:
            continue
        
        id_carrera = grupos_examen.grupo.id_carrera
        clave = f"{id_carrera}-{solicitud.id_periodo}-{solicitud.id_evaluacion}"
        
        if clave not in calendarios_por_carrera:
            carrera = carrera_repo.get_by_id(id_carrera)
            # Buscar jefe de carrera
            from app.models.Usuario import Usuario
            jefe = db.query(Usuario).filter(
                Usuario.id_carrera == id_carrera,
                Usuario.rol == 'jefe'
            ).first()
            jefe_nombre = jefe.nombre_usuario if jefe else None
            
            calendarios_por_carrera[clave] = {
                'id_carrera': id_carrera,
                'nombre_carrera': carrera.nombre_carrera if carrera else id_carrera,
                'id_periodo': solicitud.id_periodo,
                'nombre_periodo': solicitud.periodo.nombre_periodo if solicitud.periodo else None,
                'id_evaluacion': solicitud.id_evaluacion,
                'nombre_evaluacion': solicitud.evaluacion.nombre_evaluacion if solicitud.evaluacion else None,
                'jefe_carrera': jefe_nombre,
                'fecha_envio': None,  # TODO: Agregar campo fecha_envio si es necesario
                'estado': 'pendiente' if solicitud.estado == EstadoSolicitud.PENDIENTE else 
                         'aprobado' if solicitud.estado == EstadoSolicitud.APROBADO else 'rechazado',
                'observaciones': solicitud.motivo_rechazo,
                'examenes': []
            }
        
        # Obtener grupos asociados
        grupos_examen_list = db.query(GrupoExamen).options(
            joinedload(GrupoExamen.grupo)
        ).filter(GrupoExamen.id_horario == solicitud.id_horario).all()
        
        grupos = []
        for ge in grupos_examen_list:
            if ge.grupo:
                grupos.append(ge.grupo.nombre_grupo)
        
        # Obtener aula y profesor
        from app.models.AsignacionAula import AsignacionAula
        asignaciones_aula = db.query(AsignacionAula).options(
            joinedload(AsignacionAula.aula),
            joinedload(AsignacionAula.profesor_aplicador)
        ).filter(AsignacionAula.id_horario == solicitud.id_horario).all()
        
        aula = None
        profesor = None
        if asignaciones_aula and len(asignaciones_aula) > 0:
            if asignaciones_aula[0].aula:
                aula = asignaciones_aula[0].aula.nombre_aula
            if asignaciones_aula[0].profesor_aplicador:
                profesor = asignaciones_aula[0].profesor_aplicador.nombre_profesor
        
        # Formatear fecha y hora
        fecha_str = solicitud.fecha_examen.strftime('%d/%m/%Y') if solicitud.fecha_examen else None
        hora_str = None
        if solicitud.hora_inicio and solicitud.hora_fin:
            hora_inicio_str = solicitud.hora_inicio.strftime('%H:%M')
            hora_fin_str = solicitud.hora_fin.strftime('%H:%M')
            hora_str = f"{hora_inicio_str}-{hora_fin_str}"
        
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
    
    # Convertir a lista y agregar total_examenes
    resultado = []
    for calendario in calendarios_por_carrera.values():
        calendario['total_examenes'] = len(calendario['examenes'])
        # Determinar estado general (si todos están aprobados, está aprobado, etc.)
        estados = [e['estado'] for e in calendario['examenes']]
        if all(e == 'aprobado' for e in estados):
            calendario['estado'] = 'aprobado'
        elif any(e == 'rechazado' for e in estados):
            calendario['estado'] = 'rechazado'
        elif any(e == 'pendiente' for e in estados):
            calendario['estado'] = 'pendiente'
        resultado.append(calendario)
    
    # Filtrar por estado si se especifica
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

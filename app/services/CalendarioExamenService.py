from typing import List, Dict, Optional, Tuple
from datetime import date, time, timedelta
from collections import defaultdict
from sqlalchemy.orm import Session
import hashlib
import uuid

from app.models.HorarioClase import HorarioClase
from app.models.SolicitudExamen import SolicitudExamen
from app.models.GrupoExamen import GrupoExamen
from app.models.AsignacionAula import AsignacionAula
from app.models.AsignacionSinodal import AsignacionSinodal
from app.repositories.HorarioRepository import HorarioRepository
from app.repositories.SolicitudRepository import SolicitudRepository
from app.repositories.VentanaRepository import VentanaRepository
from app.repositories.AulaRepository import AulaRepository
from app.repositories.GrupoRepository import GrupoRepository
from app.repositories.GrupoExamenRepository import GrupoExamenRepository
from app.repositories.AsignacionAulaRepository import AsignacionAulaRepository
from app.repositories.AsignacionSinodalRepository import AsignacionSinodalRepository
from app.repositories.PermisoRepository import PermisoRepository
from app.repositories.ProfesorRepository import ProfesorRepository
from app.repositories.PeriodoRepository import PeriodoRepository
from app.schemas.SolicitudExamenSchema import SolicitudExamenCreate
from app.schemas.GrupoExamenSchema import GrupoExamenCreate
from app.schemas.AsignacionAulaSchema import AsignacionAulaCreate
from app.schemas.AsignacionSinodalSchema import AsignacionSinodalCreate
from app.schemas.VentanaAplicacionSchema import VentanaAplicacionCreate
from app.models.VentanaAplicacion import VentanaAplicacion


class CalendarioExamenService:
    """
    Servicio para generar calendarios de exámenes automáticamente.
    """
    
    # Horarios estándar para exámenes (8:00-10:00, 10:00-12:00, etc.)
    HORARIOS_EXAMEN = [
        (time(8, 0), time(10, 0)),
        (time(10, 0), time(12, 0)),
        (time(12, 0), time(14, 0)),
        (time(14, 0), time(16, 0)),
        (time(16, 0), time(18, 0)),
    ]
    
    def __init__(self, db: Session):
        self.db = db
        self.horario_repo = HorarioRepository(db)
        self.solicitud_repo = SolicitudRepository(db)
        self.ventana_repo = VentanaRepository(db)
        self.aula_repo = AulaRepository(db)
        self.grupo_repo = GrupoRepository(db)
        self.grupo_examen_repo = GrupoExamenRepository(db)
        self.asignacion_aula_repo = AsignacionAulaRepository(db)
        self.asignacion_sinodal_repo = AsignacionSinodalRepository(db)
        self.permiso_repo = PermisoRepository(db)
        self.profesor_repo = ProfesorRepository(db)
    
    def determinar_periodo_semestre(self, fecha_inicio: date) -> Tuple[str, str, str]:
        """
        Determina el periodo y semestre según la fecha de inicio.
        
        Reglas:
        - Si fecha_inicio está entre Oct 1 - Feb 20: Semestre A (2025-2026A)
          - Oct-Dic del año actual: periodo año-2 (Agosto-Diciembre)
          - Ene-Feb del año siguiente: periodo año-1 (Enero-Junio)
        - Si fecha_inicio está entre Mar 1 - Jul 31: Semestre B (añoB)
          - Mar-Jul del año actual: periodo año-1 (Enero-Junio)
        
        Returns:
            Tuple[id_periodo, semestre_str, nombre_periodo]
        """
        periodo_repo = PeriodoRepository(self.db)
        
        año = fecha_inicio.year
        mes = fecha_inicio.month
        
        # Determinar periodo según la fecha
        id_periodos_posibles = []
        
        if mes >= 10:  # Octubre, Noviembre, Diciembre
            # Oct-Dic pertenece al periodo "año-2" (Agosto-Diciembre)
            id_periodos_posibles = [f"{año}-2"]
            semestre_str = f"{año}-{año+1}A"
        elif mes <= 2:  # Enero, Febrero
            # Ene-Feb puede pertenecer al periodo anterior "año-1-2" o "año-1" (si no existe el anterior)
            # Basado en el semestre A que va de Oct a Feb, debería ser "año-1-2"
            id_periodos_posibles = [f"{año-1}-2", f"{año}-1"]  # Intentar primero el anterior, luego el actual
            semestre_str = f"{año-1}-{año}A"
        elif 3 <= mes <= 7:  # Marzo a Julio
            # Mar-Jul pertenece al periodo "año-1" (Enero-Junio)
            id_periodos_posibles = [f"{año}-1"]
            semestre_str = f"{año}B"
        else:  # Agosto, Septiembre
            # Ago-Sep pertenece al periodo "año-2" (Agosto-Diciembre)
            id_periodos_posibles = [f"{año}-2"]
            semestre_str = f"{año}B"
        
        # Buscar el periodo en la base de datos (probar todas las opciones posibles)
        for id_periodo_calc in id_periodos_posibles:
            periodo = periodo_repo.get_by_id(id_periodo_calc)
            if periodo:
                return (periodo.id_periodo, semestre_str, periodo.nombre_periodo)
        
        # Si no se encuentra, buscar por año en nombre_periodo como fallback
        periodos = periodo_repo.get_all()
        for p in periodos:
            if str(año) in p.nombre_periodo or str(año-1) in p.nombre_periodo:
                return (p.id_periodo, semestre_str, p.nombre_periodo)
        
        # Si no se encuentra ningún periodo, lanzar error con información útil
        periodos_disponibles = [p.id_periodo for p in periodo_repo.get_all()]
        raise ValueError(
            f"No se encontró un periodo académico para la fecha {fecha_inicio}. "
            f"Periodos intentados: {', '.join(id_periodos_posibles)}, Semestre: {semestre_str}. "
            f"Periodos disponibles en la base de datos: {', '.join(periodos_disponibles)}. "
            f"Por favor, asegúrate de que exista un periodo apropiado para esta fecha."
        )
    
    def generar_calendario_examenes(
        self, 
        id_carrera: str, 
        fecha_inicio: date,
        id_evaluacion: str,
        dias_inhabiles: List[date] = None,
        eliminar_existentes: bool = False
    ) -> Dict:
        """
        Genera un calendario de exámenes para una carrera específica.
        
        Args:
            id_carrera: ID de la carrera
            fecha_inicio: Fecha de inicio (se generan 5 días de exámenes)
            id_evaluacion: ID del tipo de evaluación (Parcial 1, 2, 3, Ordinario)
            dias_inhabiles: Lista de fechas donde no se aplicarán exámenes
            eliminar_existentes: Si True, elimina solicitudes existentes antes de generar
        
        Returns:
            Dict con información del proceso: {
                'solicitudes_creadas': int,
                'conflictos': List[str],
                'advertencias': List[str],
                'periodo_determinado': str,
                'semestre_determinado': str
            }
        """
        if dias_inhabiles is None:
            dias_inhabiles = []
        
        try:
            # 1. Determinar periodo y semestre según fecha_inicio
            id_periodo, semestre_str, nombre_periodo = self.determinar_periodo_semestre(fecha_inicio)
            
            # 2. Validar o crear ventana de aplicación
            ventana = self.ventana_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            if not ventana:
                # Crear ventana automáticamente si no existe
                # La ventana se crea con fecha_inicio como inicio y 3 semanas de duración
                fecha_fin = fecha_inicio + timedelta(days=21)  # 3 semanas después
                id_ventana = f"VENT-{id_periodo}-{id_evaluacion}"
                
                ventana_data = VentanaAplicacionCreate(
                    id_ventana=id_ventana,
                    id_periodo=id_periodo,
                    id_evaluacion=id_evaluacion,
                    fecha_inicio_examenes=fecha_inicio,
                    fecha_fin_examenes=fecha_fin
                )
                
                ventana = VentanaAplicacion(**ventana_data.dict())
                self.db.add(ventana)
                self.db.flush()
            
            # 3. Eliminar solicitudes existentes de la carrera si se solicita
            if eliminar_existentes:
                solicitudes_existentes = self.solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
                horarios_carrera = self.horario_repo.get_by_carrera(id_carrera)
                horarios_carrera_ids = [h.id_materia for h in horarios_carrera if h.id_periodo == id_periodo]
                for solicitud in solicitudes_existentes:
                    if solicitud.id_materia in horarios_carrera_ids:
                        self._eliminar_solicitud_completa(solicitud.id_horario)
                self.db.commit()
            
            # 4. Obtener horarios de la carrera para el periodo
            horarios_carrera = self.horario_repo.get_by_carrera(id_carrera)
            horarios_periodo = [h for h in horarios_carrera if h.id_periodo == id_periodo]
            
            if not horarios_periodo:
                # Hacer commit de la ventana creada antes de retornar
                self.db.commit()
                return {
                    'solicitudes_creadas': 0,
                    'conflictos': [],
                    'advertencias': ['No hay horarios registrados para esta carrera en el periodo seleccionado'],
                    'periodo_determinado': nombre_periodo,
                    'semestre_determinado': semestre_str
                }
            
            # 5. Agrupar por materia
            materias_grupos = self._agrupar_materias_grupos(horarios_periodo)
            
            # 6. Obtener recursos disponibles
            aulas_disponibles = self.aula_repo.get_disponibles()
            asignaciones_existentes = self._obtener_asignaciones_en_ventana(ventana)
            
            # 7. Calcular días disponibles (5 días hábiles, excluyendo días inhábiles)
            dias_disponibles = self._calcular_dias_disponibles(fecha_inicio, dias_inhabiles, ventana)
            
            if len(dias_disponibles) < len(materias_grupos):
                advertencias = [f"Hay {len(materias_grupos)} materias pero solo {len(dias_disponibles)} días disponibles"]
            else:
                advertencias = []
            
            # 8. Generar solicitudes para cada materia (una por día)
            solicitudes_creadas = 0
            conflictos = []
            materia_dia_index = 0
            
            for id_materia, grupos_info in materias_grupos.items():
                if materia_dia_index >= len(dias_disponibles):
                    conflictos.append(f"Materia {grupos_info['nombre']}: No hay días disponibles")
                    continue
                
                fecha_examen = dias_disponibles[materia_dia_index]
                
                resultado = self._crear_solicitud_examen_fecha(
                    id_materia=id_materia,
                    grupos_info=grupos_info,
                    id_periodo=id_periodo,
                    id_evaluacion=id_evaluacion,
                    fecha_examen=fecha_examen,
                    aulas_disponibles=aulas_disponibles,
                    asignaciones_existentes=asignaciones_existentes
                )
                
                if resultado['exito']:
                    solicitudes_creadas += 1
                    materia_dia_index += 1
                else:
                    conflictos.append(f"Materia {grupos_info['nombre']} (día {fecha_examen}): {resultado['error']}")
            
            self.db.commit()
            
            return {
                'solicitudes_creadas': solicitudes_creadas,
                'conflictos': conflictos,
                'advertencias': advertencias,
                'periodo_determinado': nombre_periodo,
                'semestre_determinado': semestre_str
            }
            
        except ValueError as e:
            # ValueError ya tiene un mensaje descriptivo, solo hacer rollback y relanzar
            self.db.rollback()
            raise
        except Exception as e:
            # Para otras excepciones, hacer rollback y lanzar un error descriptivo
            self.db.rollback()
            import traceback
            error_details = traceback.format_exc()
            print(f"Error inesperado al generar calendario: {error_details}")
            raise ValueError(f"Error al generar calendario: {str(e)}")
    
    def _calcular_dias_disponibles(self, fecha_inicio: date, dias_inhabiles: List[date], ventana) -> List[date]:
        """
        Calcula los días disponibles para exámenes (5 días hábiles, excluyendo días inhábiles).
        """
        dias_disponibles = []
        fecha_actual = fecha_inicio
        dias_inhabiles_set = set(dias_inhabiles)
        
        # Asegurar que fecha_inicio esté dentro de la ventana
        if fecha_actual < ventana.fecha_inicio_examenes:
            fecha_actual = ventana.fecha_inicio_examenes
        elif fecha_actual > ventana.fecha_fin_examenes:
            fecha_actual = ventana.fecha_inicio_examenes
        
        # Buscar 5 días disponibles
        while len(dias_disponibles) < 5 and fecha_actual <= ventana.fecha_fin_examenes:
            # Excluir sábados (5) y domingos (6)
            if fecha_actual.weekday() < 5 and fecha_actual not in dias_inhabiles_set:
                dias_disponibles.append(fecha_actual)
            
            fecha_actual += timedelta(days=1)
        
        return dias_disponibles
    
    def _agrupar_materias_grupos(self, horarios: List[HorarioClase]) -> Dict:
        """
        Agrupa horarios por materia y extrae información de grupos.
        """
        materias_dict = {}
        
        for horario in horarios:
            id_materia = horario.id_materia
            if id_materia not in materias_dict:
                materias_dict[id_materia] = {
                    'nombre': horario.materia.nombre_materia if horario.materia else 'Sin nombre',
                    'grupos': [],
                    'total_alumnos': 0,
                    'horario_referencia': horario  # Usar el primer horario como referencia
                }
            
            grupo_info = {
                'id_grupo': horario.id_grupo,
                'nombre': horario.grupo.nombre_grupo if horario.grupo else horario.id_grupo,
                'numero_alumnos': horario.grupo.numero_alumnos if horario.grupo else 0,
                'horario': horario
            }
            
            # Evitar duplicados
            if grupo_info['id_grupo'] not in [g['id_grupo'] for g in materias_dict[id_materia]['grupos']]:
                materias_dict[id_materia]['grupos'].append(grupo_info)
                materias_dict[id_materia]['total_alumnos'] += grupo_info['numero_alumnos']
        
        return materias_dict
    
    def _obtener_asignaciones_en_ventana(self, ventana) -> Dict:
        """
        Obtiene todas las asignaciones de aula existentes en la ventana.
        Retorna un diccionario: {(fecha, hora_inicio, id_aula): solicitud_id}
        """
        solicitudes = self.solicitud_repo.get_by_periodo_evaluacion(
            ventana.id_periodo, 
            ventana.id_evaluacion
        )
        
        asignaciones_dict = {}
        for solicitud in solicitudes:
            if solicitud.fecha_examen and ventana.fecha_inicio_examenes <= solicitud.fecha_examen <= ventana.fecha_fin_examenes:
                aulas_asignadas = self.asignacion_aula_repo.get_by_solicitud(solicitud.id_horario)
                for asignacion in aulas_asignadas:
                    key = (solicitud.fecha_examen, solicitud.hora_inicio, asignacion.id_aula)
                    asignaciones_dict[key] = solicitud.id_horario
        
        return asignaciones_dict
    
    def _crear_solicitud_examen_fecha(
        self,
        id_materia: str,
        grupos_info: Dict,
        id_periodo: str,
        id_evaluacion: str,
        fecha_examen: date,
        aulas_disponibles: List,
        asignaciones_existentes: Dict
    ) -> Dict:
        """
        Crea una solicitud de examen para una materia en una fecha específica.
        """
        try:
            # 1. Determinar hora (usar horario del horario regular o estándar)
            hora_inicio, hora_fin = self._encontrar_hora_disponible(
                grupos_info['horario_referencia'],
                fecha_examen,
                grupos_info['total_alumnos'],
                aulas_disponibles,
                asignaciones_existentes
            )
            
            if not hora_inicio or not hora_fin:
                return {
                    'exito': False,
                    'error': 'No se encontró hora disponible para la fecha especificada'
                }
            
            # 2. Generar ID único para la solicitud
            id_horario = self._generar_id_solicitud(id_periodo, id_evaluacion, id_materia)
            
            # 3. Crear solicitud de examen
            solicitud_data = SolicitudExamenCreate(
                id_horario=id_horario,
                id_periodo=id_periodo,
                id_evaluacion=id_evaluacion,
                id_materia=id_materia,
                fecha_examen=fecha_examen,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado=0  # Pendiente
            )
            
            solicitud = SolicitudExamen(**solicitud_data.dict())
            self.db.add(solicitud)
            self.db.flush()
            
            # 4. Asociar grupos (ID compacto para caber en VARCHAR(20))
            for grupo_info in grupos_info['grupos']:
                hash_input = f"{id_horario}-{grupo_info['id_grupo']}"
                hash_obj = hashlib.md5(hash_input.encode())
                id_examen_grupo = f"EG{hash_obj.hexdigest()[:18].upper()}"  # EG + 18 chars = 20 chars
                grupo_examen_data = GrupoExamenCreate(
                    id_examen_grupo=id_examen_grupo,
                    id_horario=id_horario,
                    id_grupo=grupo_info['id_grupo']
                )
                grupo_examen = GrupoExamen(**grupo_examen_data.dict())
                self.db.add(grupo_examen)
            
            # 5. Asignar aula y aplicador
            aula_aplicador = self._asignar_aula_y_aplicador(
                id_horario,
                fecha_examen,
                hora_inicio,
                hora_fin,
                grupos_info['total_alumnos'],
                aulas_disponibles,
                grupos_info['horario_referencia']
            )
            
            if not aula_aplicador:
                # Si no se puede asignar aula, eliminar la solicitud creada
                self.db.delete(solicitud)
                return {
                    'exito': False,
                    'error': 'No se encontró aula disponible con capacidad suficiente'
                }
            
            id_aula, id_aplicador = aula_aplicador
            
            # 6. Asignar sinodal
            sinodal = self._asignar_sinodal(
                id_horario,
                id_materia,
                fecha_examen,
                hora_inicio,
                hora_fin
            )
            
            # Actualizar asignaciones existentes para evitar conflictos
            asignaciones_existentes[(fecha_examen, hora_inicio, id_aula)] = id_horario
            
            return {
                'exito': True,
                'id_horario': id_horario
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                'exito': False,
                'error': str(e)
            }
    
    def _crear_solicitud_examen(
        self,
        id_materia: str,
        grupos_info: Dict,
        id_periodo: str,
        id_evaluacion: str,
        ventana,
        aulas_disponibles: List,
        asignaciones_existentes: Dict
    ) -> Dict:
        """
        Crea una solicitud de examen para una materia.
        """
        try:
            # 1. Determinar fecha y hora
            fecha_hora = self._encontrar_slot_disponible(
                grupos_info['horario_referencia'],
                ventana,
                grupos_info['total_alumnos'],
                aulas_disponibles,
                asignaciones_existentes
            )
            
            if not fecha_hora:
                return {
                    'exito': False,
                    'error': 'No se encontró slot disponible en la ventana de aplicación'
                }
            
            fecha, hora_inicio, hora_fin = fecha_hora
            
            # 2. Generar ID único para la solicitud
            id_horario = self._generar_id_solicitud(id_periodo, id_evaluacion, id_materia)
            
            # 3. Crear solicitud de examen
            solicitud_data = SolicitudExamenCreate(
                id_horario=id_horario,
                id_periodo=id_periodo,
                id_evaluacion=id_evaluacion,
                id_materia=id_materia,
                fecha_examen=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado=0  # Pendiente
            )
            
            solicitud = SolicitudExamen(**solicitud_data.dict())
            self.db.add(solicitud)
            self.db.flush()
            
            # 4. Asociar grupos
            for grupo_info in grupos_info['grupos']:
                id_examen_grupo = f"{id_horario}-{grupo_info['id_grupo']}"
                grupo_examen_data = GrupoExamenCreate(
                    id_examen_grupo=id_examen_grupo,
                    id_horario=id_horario,
                    id_grupo=grupo_info['id_grupo']
                )
                grupo_examen = GrupoExamen(**grupo_examen_data.dict())
                self.db.add(grupo_examen)
            
            # 5. Asignar aula y aplicador
            aula_aplicador = self._asignar_aula_y_aplicador(
                id_horario,
                fecha_examen,
                hora_inicio,
                hora_fin,
                grupos_info['total_alumnos'],
                aulas_disponibles,
                grupos_info['horario_referencia']
            )
            
            if not aula_aplicador:
                # Si no se puede asignar aula, eliminar la solicitud creada
                self.db.delete(solicitud)
                return {
                    'exito': False,
                    'error': 'No se encontró aula disponible con capacidad suficiente'
                }
            
            id_aula, id_aplicador = aula_aplicador
            
            # 6. Asignar sinodal
            sinodal = self._asignar_sinodal(
                id_horario,
                id_materia,
                fecha_examen,
                hora_inicio,
                hora_fin
            )
            
            # Actualizar asignaciones existentes para evitar conflictos
            asignaciones_existentes[(fecha_examen, hora_inicio, id_aula)] = id_horario
            
            return {
                'exito': True,
                'id_horario': id_horario
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                'exito': False,
                'error': str(e)
            }
    
    def _encontrar_hora_disponible(
        self,
        horario_referencia: HorarioClase,
        fecha_examen: date,
        total_alumnos: int,
        aulas_disponibles: List,
        asignaciones_existentes: Dict
    ) -> Optional[Tuple[time, time]]:
        """
        Encuentra una hora disponible para el examen en la fecha especificada.
        Intenta primero con el horario regular, luego con horarios estándar.
        """
        # Intentar primero con el horario regular si el día de la semana coincide
        if fecha_examen.weekday() == horario_referencia.dia_semana:
            hora_inicio = horario_referencia.hora_inicio
            hora_fin = horario_referencia.hora_fin
            
            aula_disponible = self._buscar_aula_disponible(
                fecha_examen,
                hora_inicio,
                hora_fin,
                total_alumnos,
                aulas_disponibles,
                asignaciones_existentes
            )
            
            if aula_disponible:
                return (hora_inicio, hora_fin)
        
        # Si no funciona con el horario regular, intentar con horarios estándar
        for hora_inicio, hora_fin in self.HORARIOS_EXAMEN:
            aula_disponible = self._buscar_aula_disponible(
                fecha_examen,
                hora_inicio,
                hora_fin,
                total_alumnos,
                aulas_disponibles,
                asignaciones_existentes
            )
            
            if aula_disponible:
                return (hora_inicio, hora_fin)
        
        return None
    
    def _buscar_aula_disponible(
        self,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        capacidad_necesaria: int,
        aulas_disponibles: List,
        asignaciones_existentes: Dict
    ) -> Optional[str]:
        """
        Busca un aula disponible que cumpla con la capacidad y no tenga conflictos.
        """
        for aula in aulas_disponibles:
            if aula.capacidad < capacidad_necesaria:
                continue
            
            # Verificar si está ocupada
            key = (fecha, hora_inicio, aula.id_aula)
            if key in asignaciones_existentes:
                continue
            
            # Verificar conflictos adicionales
            conflictos = self.asignacion_aula_repo.get_by_aula_fecha_hora(
                aula.id_aula,
                fecha,
                hora_inicio,
                hora_fin
            )
            
            if not conflictos:
                return aula.id_aula
        
        return None
    
    def _asignar_aula_y_aplicador(
        self,
        id_horario: str,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        total_alumnos: int,
        aulas_disponibles: List,
        horario_referencia: HorarioClase
    ) -> Optional[Tuple[str, str]]:
        """
        Asigna un aula y un aplicador para el examen.
        """
        aula_id = self._buscar_aula_disponible(
            fecha,
            hora_inicio,
            hora_fin,
            total_alumnos,
            aulas_disponibles,
            {}
        )
        
        if not aula_id:
            return None
        
        # Asignar aplicador (preferir el profesor titular, si está disponible)
        id_aplicador = horario_referencia.id_profesor
        
        # Verificar si el profesor está disponible
        asignaciones_profesor = self.asignacion_aula_repo.get_by_profesor_aplicador(id_aplicador)
        for asignacion in asignaciones_profesor:
            solicitud = self.solicitud_repo.get_by_id(asignacion.id_horario)
            if solicitud and solicitud.fecha_examen == fecha:
                if solicitud.hora_inicio < hora_fin and solicitud.hora_fin > hora_inicio:
                    # El profesor está ocupado, buscar otro
                    id_aplicador = self._buscar_aplicador_disponible(fecha, hora_inicio, hora_fin)
                    break
        
        if not id_aplicador:
            return None
        
        # Crear asignación de aula (ID compacto para caber en VARCHAR(20))
        hash_input = f"{id_horario}-{aula_id}"
        hash_obj = hashlib.md5(hash_input.encode())
        id_examen_aula = f"AA{hash_obj.hexdigest()[:18].upper()}"  # AA + 18 chars = 20 chars
        asignacion_data = AsignacionAulaCreate(
            id_examen_aula=id_examen_aula,
            id_horario=id_horario,
            id_aula=aula_id,
            id_profesor_aplicador=id_aplicador
        )
        
        asignacion = AsignacionAula(**asignacion_data.dict())
        self.db.add(asignacion)
        
        return (aula_id, id_aplicador)
    
    def _buscar_aplicador_disponible(self, fecha: date, hora_inicio: time, hora_fin: time) -> Optional[str]:
        """
        Busca un profesor aplicador disponible.
        """
        profesores_activos = self.profesor_repo.get_activos()
        
        for profesor in profesores_activos:
            asignaciones = self.asignacion_aula_repo.get_by_profesor_aplicador(profesor.id_profesor)
            
            ocupado = False
            for asignacion in asignaciones:
                solicitud = self.solicitud_repo.get_by_id(asignacion.id_horario)
                if solicitud and solicitud.fecha_examen == fecha:
                    if solicitud.hora_inicio < hora_fin and solicitud.hora_fin > hora_inicio:
                        ocupado = True
                        break
            
            if not ocupado:
                return profesor.id_profesor
        
        return None
    
    def _asignar_sinodal(
        self,
        id_horario: str,
        id_materia: str,
        fecha: date,
        hora_inicio: time,
        hora_fin: time
    ) -> Optional[str]:
        """
        Asigna un sinodal disponible para el examen.
        """
        # Obtener profesores con permiso sinodal para esta materia
        permisos = self.permiso_repo.get_by_materia(id_materia)
        
        if not permisos:
            return None
        
        # Verificar disponibilidad de cada sinodal
        for permiso in permisos:
            id_profesor = permiso.id_profesor
            
            # Verificar límite de 3 materias
            asignaciones_sinodal = self.asignacion_sinodal_repo.get_by_profesor(id_profesor)
            if len(asignaciones_sinodal) >= 3:
                continue
            
            # Verificar conflictos de horario
            ocupado = False
            for asignacion in asignaciones_sinodal:
                solicitud = self.solicitud_repo.get_by_id(asignacion.id_horario)
                if solicitud and solicitud.fecha_examen == fecha:
                    if solicitud.hora_inicio < hora_fin and solicitud.hora_fin > hora_inicio:
                        ocupado = True
                        break
            
            if not ocupado:
                # Asignar sinodal (ID compacto para caber en VARCHAR(20))
                hash_input = f"{id_horario}-{id_profesor}"
                hash_obj = hashlib.md5(hash_input.encode())
                id_examen_sinodal = f"ES{hash_obj.hexdigest()[:18].upper()}"  # ES + 18 chars = 20 chars
                asignacion_data = AsignacionSinodalCreate(
                    id_examen_sinodal=id_examen_sinodal,
                    id_horario=id_horario,
                    id_profesor=id_profesor
                )
                
                asignacion = AsignacionSinodal(**asignacion_data.dict())
                self.db.add(asignacion)
                
                return id_profesor
        
        return None
    
    def _generar_id_solicitud(self, id_periodo: str, id_evaluacion: str, id_materia: str) -> str:
        """
        Genera un ID único para la solicitud de examen.
        Formato compacto para caber en VARCHAR(20): EX{periodo}{eval}{materia}{hash}
        Ejemplo: EX20251E1M1A1B2C3D4 (20 caracteres)
        """
        # Formato compacto: EX + periodo sin guion + eval sin "EVAL" + materia sin "MAT" + hash de 7 chars
        periodo_compacto = id_periodo.replace('-', '')  # 2025-1 -> 20251
        eval_compacto = id_evaluacion.replace('EVAL', '') if id_evaluacion.startswith('EVAL') else id_evaluacion[-3:]  # EVAL001 -> 001
        materia_compacto = id_materia.replace('MAT', '') if id_materia.startswith('MAT') else id_materia[-3:]  # MAT001 -> 001
        
        # Generar hash único de 7 caracteres
        unique_string = f"{id_periodo}-{id_evaluacion}-{id_materia}-{uuid.uuid4()}"
        hash_obj = hashlib.md5(unique_string.encode())
        hash_hex = hash_obj.hexdigest()[:7].upper()  # 7 caracteres
        
        # Construir ID: EX + periodo(5) + eval(3) + materia(3) + hash(7) = 20 caracteres
        id_solicitud = f"EX{periodo_compacto}{eval_compacto}{materia_compacto}{hash_hex}"
        
        # Asegurar que no exceda 20 caracteres
        return id_solicitud[:20]
    
    def _eliminar_solicitud_completa(self, id_horario: str):
        """
        Elimina una solicitud y todas sus relaciones.
        """
        # Eliminar grupos de examen
        grupos = self.grupo_examen_repo.get_by_solicitud(id_horario)
        for grupo in grupos:
            self.db.delete(grupo)
        
        # Eliminar asignaciones de aula
        asignaciones_aula = self.asignacion_aula_repo.get_by_solicitud(id_horario)
        for asignacion in asignaciones_aula:
            self.db.delete(asignacion)
        
        # Eliminar asignaciones de sinodal
        asignaciones_sinodal = self.asignacion_sinodal_repo.get_by_solicitud(id_horario)
        for asignacion in asignaciones_sinodal:
            self.db.delete(asignacion)
        
        # Eliminar solicitud
        solicitud = self.solicitud_repo.get_by_id(id_horario)
        if solicitud:
            self.db.delete(solicitud)

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
from app.repositories.MateriaRepository import MateriaRepository
from app.repositories.CarreraRepository import CarreraRepository
from app.schemas.SolicitudExamenSchema import SolicitudExamenCreate
from app.schemas.GrupoExamenSchema import GrupoExamenCreate
from app.schemas.AsignacionAulaSchema import AsignacionAulaCreate
from app.schemas.AsignacionSinodalSchema import AsignacionSinodalCreate
from app.schemas.VentanaAplicacionSchema import VentanaAplicacionCreate
from app.models.VentanaAplicacion import VentanaAplicacion


class CalendarioExamenService:
    """
    Servicio para generar calendarios de exámenes automáticamente.
    Separa lógica: carreras sociales (Informática, Empresariales, Administración Pública, etc.)
    usan exámenes tal cual aparecen en los horarios (misma hora, mismo aula). Carreras de salud
    usan el algoritmo por posiciones (futuro).
    """
    
    # Carreras del área social: exámenes = horarios de clase (misma hora, misma aula)
    # Se identifica por id_carrera o por nombre_carrera (substring)
    CARRERAS_SOCIALES_IDS = frozenset({'LIC-CE'})  # Lic. Ciencias Empresariales; añadir LIC-IN, LIC-AP, etc.
    CARRERAS_SOCIALES_NOMBRES = (
        'informática', 'informatica',
        'empresariales',
        'administración pública', 'administracion publica',
        'administración municipal', 'administracion municipal',
    )
    
    # Horarios estándar para exámenes (8:00-10:00, 10:00-12:00, etc.) - usado solo para carreras no sociales
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
        self.materia_repo = MateriaRepository(db)
        self.carrera_repo = CarreraRepository(db)
    
    def _es_carrera_sociales(self, id_carrera: str) -> bool:
        """Determina si la carrera es del área social (exámenes = horarios de clase)."""
        if id_carrera and id_carrera in self.CARRERAS_SOCIALES_IDS:
            return True
        carrera = self.carrera_repo.get_by_id(id_carrera)
        if not carrera or not carrera.nombre_carrera:
            return False
        nombre_lower = carrera.nombre_carrera.strip().lower()
        return any(kw in nombre_lower for kw in self.CARRERAS_SOCIALES_NOMBRES)
    
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
            # Oct-Dic pertenece al periodo "año-2" (Agosto-Diciembre) o formato "año(año+1)A"
            id_periodos_posibles = [
                f"{año}-2",  # Formato largo: 2025-2
                f"{str(año)[-2:]}{str(año+1)[-2:]}A"  # Formato corto: 2526A
            ]
            semestre_str = f"{año}-{año+1}A"
        elif mes <= 2:  # Enero, Febrero
            # Ene-Feb puede pertenecer al periodo anterior "año-1-2" o "año-1" (si no existe el anterior)
            # Basado en el semestre A que va de Oct a Feb, debería ser "año-1-2" o formato "año-1(año)A"
            id_periodos_posibles = [
                f"{año-1}-2",  # Formato largo: 2025-2
                f"{año}-1",    # Formato largo alternativo: 2026-1
                f"{str(año-1)[-2:]}{str(año)[-2:]}A"  # Formato corto: 2526A
            ]
            semestre_str = f"{año-1}-{año}A"
        elif 3 <= mes <= 7:  # Marzo a Julio
            # Mar-Jul pertenece al periodo "año-1" (Enero-Junio) o formato "añoB"
            id_periodos_posibles = [
                f"{año}-1",  # Formato largo: 2026-1
                f"{str(año)[-2:]}B"  # Formato corto: 26B
            ]
            semestre_str = f"{año}B"
        else:  # Agosto, Septiembre
            # Ago-Sep pertenece al periodo "año-2" (Agosto-Diciembre) o formato "añoB"
            id_periodos_posibles = [
                f"{año}-2",  # Formato largo: 2025-2
                f"{str(año)[-2:]}B"  # Formato corto: 25B
            ]
            semestre_str = f"{año}B"
        
        # Buscar el periodo en la base de datos (probar todas las opciones posibles)
        for id_periodo_calc in id_periodos_posibles:
            periodo = periodo_repo.get_by_id(id_periodo_calc)
            if periodo:
                return (periodo.id_periodo, semestre_str, periodo.nombre_periodo)
        
        # Si no se encuentra, buscar por año en nombre_periodo o id_periodo como fallback
        periodos = periodo_repo.get_all()
        for p in periodos:
            # Buscar por año completo o últimos 2 dígitos en id_periodo o nombre_periodo
            año_2digitos = str(año)[-2:]
            año_anterior_2digitos = str(año-1)[-2:]
            
            if (str(año) in p.nombre_periodo or str(año-1) in p.nombre_periodo or 
                str(año) in p.id_periodo or str(año-1) in p.id_periodo or
                año_2digitos in p.id_periodo or año_anterior_2digitos in p.id_periodo):
                # Verificar que el formato coincida con el semestre esperado
                if (semestre_str.endswith('A') and 'A' in p.id_periodo.upper()) or \
                   (semestre_str.endswith('B') and 'B' in p.id_periodo.upper()):
                    return (p.id_periodo, semestre_str, p.nombre_periodo)
        
        # Si no se encuentra ningún periodo, lanzar error con información útil
        periodos_disponibles = [p.id_periodo for p in periodo_repo.get_all()]
        raise ValueError(
            f"No se encontró un periodo académico para la fecha {fecha_inicio}. "
            f"Periodos intentados: {', '.join(id_periodos_posibles)}, Semestre: {semestre_str}. "
            f"Periodos disponibles en la base de datos: {', '.join(periodos_disponibles)}. "
            f"Por favor, asegúrate de que exista un periodo apropiado para esta fecha."
        )
    
    def _generar_calendario_sociales(
        self,
        id_carrera: str,
        fecha_inicio: date,
        id_evaluacion: str,
        id_periodo: str,
        semestre_str: str,
        nombre_periodo: str,
        dias_inhabiles: List[date],
    ) -> Dict:
        """
        Genera calendario para carreras del área social (Informática, Empresariales, Administración Pública).
        Los exámenes se programan tal cual aparecen en los horarios: misma hora de clase, mismo aula,
        y se incluyen todos los grupos de la carrera.
        """
        try:
            # 1. Ventana de aplicación
            ventana = self.ventana_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            if not ventana:
                fecha_fin_base = fecha_inicio + timedelta(days=21)
                id_ventana = f"VENT-{id_periodo}-{id_evaluacion}"
                ventana_data = VentanaAplicacionCreate(
                    id_ventana=id_ventana,
                    id_periodo=id_periodo,
                    id_evaluacion=id_evaluacion,
                    fecha_inicio_examenes=fecha_inicio,
                    fecha_fin_examenes=fecha_fin_base
                )
                ventana = VentanaAplicacion(**ventana_data.dict())
                self.db.add(ventana)
                self.db.flush()
            elif fecha_inicio < ventana.fecha_inicio_examenes:
                ventana.fecha_inicio_examenes = fecha_inicio
                self.db.flush()
            
            # 2. Eliminar solicitudes existentes de esta carrera para periodo y evaluación
            horarios_carrera_temp = self.horario_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            horarios_carrera_ids = [h.id_materia for h in horarios_carrera_temp if h.id_periodo == id_periodo]
            solicitudes_existentes = self.solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            for solicitud in solicitudes_existentes:
                if solicitud.id_materia in horarios_carrera_ids:
                    self._eliminar_solicitud_completa(solicitud.id_horario)
            self.db.commit()
            
            # 3. Horarios de la carrera (periodo actual + referencia para grupos sin horario en periodo)
            horarios_carrera = self.horario_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            horarios_periodo = [h for h in horarios_carrera if h.id_periodo == id_periodo]
            grupos_unicos = set(h.id_grupo for h in horarios_periodo if h.id_grupo)
            grupos_carrera = self.grupo_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            grupos_ids_carrera = [g.id_grupo for g in grupos_carrera]
            grupos_sin_horarios = set(grupos_ids_carrera) - grupos_unicos
            
            horarios_otros_periodos = []
            for grupo_id in grupos_sin_horarios:
                horarios_grupo = self.horario_repo.get_by_grupo(grupo_id, skip=0, limit=10000)
                if not horarios_grupo:
                    continue
                horarios_por_materia = {}
                for h in horarios_grupo:
                    if not h.id_materia or not h.id_periodo:
                        continue
                    if h.id_materia not in horarios_por_materia:
                        horarios_por_materia[h.id_materia] = []
                    horarios_por_materia[h.id_materia].append(h)
                for id_materia, lista_h in horarios_por_materia.items():
                    ref = min(lista_h, key=lambda x: (x.dia_semana or 99, x.hora_inicio or time(23, 59)))
                    horarios_otros_periodos.append(ref)
            
            horarios_para_procesar = horarios_periodo + horarios_otros_periodos
            if not horarios_para_procesar:
                self.db.commit()
                return {
                    'solicitudes_creadas': 0,
                    'conflictos': [],
                    'advertencias': ['No hay horarios registrados para esta carrera en el periodo seleccionado'],
                    'periodo_determinado': nombre_periodo,
                    'semestre_determinado': semestre_str
                }
            
            # 4. Un slot por (materia, grupo): primer horario por (dia_semana, hora_inicio)
            # Así el examen queda con la misma hora y aula que la clase
            slots_sociales = {}  # (id_materia, id_grupo) -> { horario, grupo_info }
            materias_grupos = self._agrupar_materias_grupos(horarios_para_procesar)
            for id_materia, info in materias_grupos.items():
                for grupo_info in info['grupos']:
                    h = grupo_info.get('horario')
                    if not h or (h.hora_inicio is None or h.hora_fin is None):
                        continue
                    key = (id_materia, grupo_info['id_grupo'])
                    if key not in slots_sociales:
                        slots_sociales[key] = {
                            'horario': h,
                            'grupo_info': grupo_info,
                            'nombre_materia': info.get('nombre', id_materia),
                        }
                    else:
                        # Mantener el que tenga (dia_semana, hora_inicio) menor
                        actual = slots_sociales[key]['horario']
                        d_actual = actual.dia_semana if actual.dia_semana is not None else 99
                        d_nuevo = h.dia_semana if h.dia_semana is not None else 99
                        if (d_nuevo, h.hora_inicio) < (d_actual, actual.hora_inicio):
                            slots_sociales[key] = {'horario': h, 'grupo_info': grupo_info, 'nombre_materia': info.get('nombre', id_materia)}
            
            # 5. Días hábiles ascendentes desde fecha_inicio (un examen por día por grupo)
            grupos_unicos = {g for (_, g) in slots_sociales}
            max_materias_por_grupo = 10
            if grupos_unicos:
                max_materias_por_grupo = max(
                    sum(1 for (_, g) in slots_sociales if g == id_g) for id_g in grupos_unicos
                )
            dias_disponibles = self._calcular_dias_disponibles(
                fecha_inicio, dias_inhabiles, ventana,
                minimo_dias=max_materias_por_grupo
            )
            
            # 6. Por grupo: ordenar materias por id_materia (asignatura) ascendente y asignar fecha = dias_disponibles[posición]
            # id_grupo -> lista de (id_materia, slot) ordenada por id_materia
            por_grupo = defaultdict(list)
            for (id_materia, id_grupo), slot in slots_sociales.items():
                por_grupo[id_grupo].append((id_materia, slot))
            for id_grupo in por_grupo:
                por_grupo[id_grupo].sort(key=lambda x: x[0])  # por id_materia (asignatura) ascendente
            
            aulas_disponibles = self.aula_repo.get_disponibles(limit=500)
            salas_computo = self.aula_repo.get_salas_computo(limit=500)
            aulas_en_horarios_carrera = {h.id_aula for h in horarios_para_procesar if h.id_aula}
            asignaciones_existentes = self._obtener_asignaciones_en_ventana(ventana)
            
            solicitudes_creadas = 0
            conflictos = []
            advertencias = []
            
            for id_grupo in sorted(por_grupo.keys()):
                lista_slots = por_grupo[id_grupo]
                for posicion, (id_materia, slot) in enumerate(lista_slots):
                    if posicion >= len(dias_disponibles):
                        conflictos.append(f"Grupo {id_grupo} - {slot['nombre_materia']}: no hay más días disponibles (posición {posicion + 1})")
                        continue
                    fecha_examen = dias_disponibles[posicion]
                    h = slot['horario']
                    grupo_info = slot['grupo_info']
                    nombre_materia = slot['nombre_materia']
                    hora_inicio = h.hora_inicio
                    hora_fin = h.hora_fin
                    
                    materia = self.materia_repo.get_by_id(id_materia)
                    tipo_examen = (materia.tipo_examen or 'plataforma').strip().lower() if materia else 'plataforma'
                    id_aula = None
                    if tipo_examen == 'plataforma' and salas_computo:
                        id_aula = self._elegir_sala_computo_carrera(
                            fecha_examen, hora_inicio, hora_fin,
                            aulas_en_horarios_carrera, salas_computo,
                            asignaciones_existentes, grupo_info.get('numero_alumnos', 0)
                        )
                    
                    id_horario_grupo = self._generar_id_solicitud(id_periodo, id_evaluacion, f"{id_materia}-{id_grupo}")
                    resultado = self._crear_solicitud_examen_individual(
                        id_horario=id_horario_grupo,
                        id_materia=id_materia,
                        grupo_info=grupo_info,
                        horario_referencia=h,
                        id_periodo=id_periodo,
                        id_evaluacion=id_evaluacion,
                        fecha_examen=fecha_examen,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        id_aula=id_aula,
                        aulas_disponibles=aulas_disponibles,
                        asignaciones_existentes=asignaciones_existentes
                    )
                    if resultado['exito']:
                        solicitudes_creadas += 1
                    else:
                        conflictos.append(f"Grupo {id_grupo} - {nombre_materia}: {resultado.get('error', '')}")
            
            self.db.commit()
            return {
                'solicitudes_creadas': solicitudes_creadas,
                'conflictos': conflictos,
                'advertencias': advertencias,
                'periodo_determinado': nombre_periodo,
                'semestre_determinado': semestre_str
            }
        except Exception as e:
            self.db.rollback()
            import traceback
            print(f"[DEBUG] Error en _generar_calendario_sociales: {traceback.format_exc()}")
            raise ValueError(f"Error al generar calendario (sociales): {str(e)}")
    
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
        
        IMPORTANTE: Si ya existe un calendario para el mismo periodo y evaluación, se eliminará
        automáticamente antes de generar el nuevo para evitar duplicados.
        
        Args:
            id_carrera: ID de la carrera
            fecha_inicio: Fecha de inicio (se generan 5 días de exámenes)
            id_evaluacion: ID del tipo de evaluación (Parcial 1, 2, 3, Ordinario)
            dias_inhabiles: Lista de fechas donde no se aplicarán exámenes
            eliminar_existentes: (Deprecated) Ya no se usa, siempre se eliminan los existentes del mismo periodo/evaluación
        
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
            
            # 2. Carreras sociales: exámenes tal cual en horarios (misma hora, misma aula, todos los grupos)
            if self._es_carrera_sociales(id_carrera):
                return self._generar_calendario_sociales(
                    id_carrera=id_carrera,
                    fecha_inicio=fecha_inicio,
                    id_evaluacion=id_evaluacion,
                    id_periodo=id_periodo,
                    semestre_str=semestre_str,
                    nombre_periodo=nombre_periodo,
                    dias_inhabiles=dias_inhabiles,
                )
            
            # 3. Validar o crear ventana de aplicación (carreras no sociales, ej. salud)
            ventana = self.ventana_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            if not ventana:
                # Crear ventana automáticamente si no existe
                # La ventana se crea con fecha_inicio como inicio
                # Primero necesitamos saber cuántas materias hay para calcular la duración necesaria
                # Por ahora, creamos una ventana base y la extenderemos después si es necesario
                fecha_fin_base = fecha_inicio + timedelta(days=21)  # 3 semanas base
                id_ventana = f"VENT-{id_periodo}-{id_evaluacion}"
                
                ventana_data = VentanaAplicacionCreate(
                    id_ventana=id_ventana,
                    id_periodo=id_periodo,
                    id_evaluacion=id_evaluacion,
                    fecha_inicio_examenes=fecha_inicio,
                    fecha_fin_examenes=fecha_fin_base
                )
                
                ventana = VentanaAplicacion(**ventana_data.dict())
                self.db.add(ventana)
                self.db.flush()
                print(f"[DEBUG] Ventana creada: fecha_inicio_examenes={fecha_inicio}, fecha_fin_examenes={fecha_fin_base}")
            else:
                # Si la ventana ya existe, actualizar fecha_inicio_examenes si la fecha_inicio del usuario es anterior
                # Esto asegura que respetemos la fecha de inicio solicitada por el usuario
                if fecha_inicio < ventana.fecha_inicio_examenes:
                    print(f"[DEBUG] Ventana existente tiene fecha_inicio_examenes={ventana.fecha_inicio_examenes}, pero usuario solicitó {fecha_inicio}. Actualizando...")
                    ventana.fecha_inicio_examenes = fecha_inicio
                    self.db.flush()
                elif fecha_inicio > ventana.fecha_inicio_examenes:
                    print(f"[DEBUG] Ventana existente: fecha_inicio_examenes={ventana.fecha_inicio_examenes}, usuario solicitó {fecha_inicio} (posterior, se respetará)")
                else:
                    print(f"[DEBUG] Ventana existente: fecha_inicio_examenes={ventana.fecha_inicio_examenes} coincide con fecha_inicio solicitada")
            
            # 3. Eliminar solicitudes existentes de la carrera para el mismo periodo y evaluación
            # Por defecto, siempre eliminamos los existentes para evitar duplicados
            # Si eliminar_existentes es False, aún así eliminamos para el mismo periodo/evaluación
            solicitudes_existentes = self.solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            horarios_carrera_temp = self.horario_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            horarios_carrera_ids = [h.id_materia for h in horarios_carrera_temp if h.id_periodo == id_periodo]
            
            solicitudes_eliminadas = 0
            for solicitud in solicitudes_existentes:
                if solicitud.id_materia in horarios_carrera_ids:
                    self._eliminar_solicitud_completa(solicitud.id_horario)
                    solicitudes_eliminadas += 1
            
            if solicitudes_eliminadas > 0:
                self.db.commit()
            
            # 4. Obtener horarios de la carrera para el periodo (sin límite)
            horarios_carrera = self.horario_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            
            # Analizar periodos presentes en los horarios
            periodos_presentes = {}
            for h in horarios_carrera:
                if h.id_periodo:
                    if h.id_periodo not in periodos_presentes:
                        periodos_presentes[h.id_periodo] = []
                    periodos_presentes[h.id_periodo].append(h.id_grupo)
            
            print(f"[DEBUG] Periodos encontrados en horarios de carrera {id_carrera}: {list(periodos_presentes.keys())}")
            for periodo, grupos in periodos_presentes.items():
                grupos_unicos_periodo = set(grupos)
                print(f"[DEBUG]   Periodo {periodo}: {len(grupos_unicos_periodo)} grupos únicos")
            
            horarios_periodo = [h for h in horarios_carrera if h.id_periodo == id_periodo]
            
            print(f"[DEBUG] Horarios obtenidos: {len(horarios_carrera)} total, {len(horarios_periodo)} para periodo {id_periodo}")
            
            # Contar grupos únicos en los horarios
            grupos_unicos = set()
            for h in horarios_periodo:
                if h.id_grupo:
                    grupos_unicos.add(h.id_grupo)
            print(f"[DEBUG] Grupos únicos en horarios del periodo {id_periodo}: {len(grupos_unicos)} grupos - {sorted(grupos_unicos)}")
            
            # Verificar todos los grupos de la carrera
            grupos_carrera = self.grupo_repo.get_by_carrera(id_carrera, skip=0, limit=10000)
            grupos_ids_carrera = [g.id_grupo for g in grupos_carrera]
            grupos_sin_horarios = set(grupos_ids_carrera) - grupos_unicos
            print(f"[DEBUG] Total grupos en carrera {id_carrera}: {len(grupos_ids_carrera)}")
            if grupos_sin_horarios:
                print(f"[DEBUG] ⚠️ Grupos SIN horarios para periodo {id_periodo}: {sorted(grupos_sin_horarios)}")
            
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
            
            # 5. Incluir TODOS los grupos de la carrera, incluso si no tienen horarios para el periodo actual
            # Estrategia: 
            # 1. Para grupos con horarios del periodo actual: usar esos horarios
            # 2. Para grupos sin horarios del periodo actual: buscar sus horarios en otros periodos y usarlos como referencia
            grupos_con_horarios_periodo = set(grupos_unicos)
            grupos_sin_horarios_periodo_actual = grupos_sin_horarios
            
            # Buscar horarios de grupos que no tienen horarios para el periodo actual
            horarios_otros_periodos = []
            grupos_con_horarios_otros_periodos = set()
            
            if grupos_sin_horarios_periodo_actual:
                print(f"[DEBUG] Buscando horarios de {len(grupos_sin_horarios_periodo_actual)} grupos sin horarios para periodo {id_periodo}...")
                grupos_procesados = 0
                for grupo_id in grupos_sin_horarios_periodo_actual:
                    # Buscar cualquier horario de este grupo en cualquier periodo
                    horarios_grupo = self.horario_repo.get_by_grupo(grupo_id, skip=0, limit=10000)
                    if horarios_grupo:
                        grupos_procesados += 1
                        grupos_con_horarios_otros_periodos.add(grupo_id)
                        print(f"[DEBUG]   Grupo {grupo_id}: encontró {len(horarios_grupo)} horarios en otros periodos")
                        
                        # Agrupar por materia para incluir todas las materias del grupo
                        horarios_por_materia = {}
                        for h in horarios_grupo:
                            if h.id_materia and h.id_periodo:
                                if h.id_materia not in horarios_por_materia:
                                    horarios_por_materia[h.id_materia] = []
                                horarios_por_materia[h.id_materia].append(h)
                        
                        # Para cada materia, usar el horario del periodo más reciente
                        materias_incluidas = 0
                        for id_materia, horarios_materia in horarios_por_materia.items():
                            horarios_materia_sorted = sorted(horarios_materia, key=lambda h: h.id_periodo or '', reverse=True)
                            horario_referencia = horarios_materia_sorted[0]
                            # Usar el horario original tal cual - el código de agrupación acepta horarios de cualquier periodo
                            horarios_otros_periodos.append(horario_referencia)
                            materias_incluidas += 1
                            print(f"[DEBUG]     Materia {id_materia}: usando horario de periodo {horario_referencia.id_periodo}")
                        print(f"[DEBUG]   Grupo {grupo_id}: {materias_incluidas} materias incluidas")
                    else:
                        print(f"[DEBUG]   Grupo {grupo_id}: NO tiene horarios en ningún periodo")
                
                print(f"[DEBUG] Resumen: {grupos_procesados} de {len(grupos_sin_horarios_periodo_actual)} grupos encontraron horarios en otros periodos")
                
                print(f"[DEBUG]   Encontrados horarios de referencia para {len(grupos_con_horarios_otros_periodos)} grupos en otros periodos")
            
            grupos_sin_horarios_total = grupos_sin_horarios_periodo_actual - grupos_con_horarios_otros_periodos
            if grupos_sin_horarios_total:
                print(f"[DEBUG] ⚠️ {len(grupos_sin_horarios_total)} grupos NO tienen horarios en NINGÚN periodo: {sorted(list(grupos_sin_horarios_total))[:10]}{'...' if len(grupos_sin_horarios_total) > 10 else ''}")
            
            # Combinar horarios del periodo actual con horarios de referencia de otros periodos
            horarios_para_procesar = horarios_periodo + horarios_otros_periodos
            print(f"[DEBUG] Total horarios a procesar: {len(horarios_periodo)} del periodo {id_periodo} + {len(horarios_otros_periodos)} de referencia = {len(horarios_para_procesar)}")
            
            # 6. Agrupar por materia
            materias_grupos = self._agrupar_materias_grupos(horarios_para_procesar)
            
            # 7. Obtener recursos disponibles (aulas normales y salas de cómputo para plataforma)
            aulas_disponibles = self.aula_repo.get_disponibles(limit=500)
            salas_computo = self.aula_repo.get_salas_computo(limit=500)
            asignaciones_existentes = self._obtener_asignaciones_en_ventana(ventana)
            
            # 7. Reorganizar datos: agrupar por grupo y luego por materia
            # Esto nos permite asignar fechas por posición de examen
            grupos_materias = {}  # {id_grupo: [lista de materias ordenadas]}
            
            for id_materia, grupos_info in materias_grupos.items():
                for grupo_info in grupos_info['grupos']:
                    id_grupo = grupo_info['id_grupo']
                    if id_grupo not in grupos_materias:
                        grupos_materias[id_grupo] = []
                    grupos_materias[id_grupo].append({
                        'id_materia': id_materia,
                        'nombre': grupos_info['nombre'],
                        'grupo_info': grupo_info
                    })
            
            # Ordenar materias por id_materia para cada grupo (para tener un orden consistente)
            for id_grupo in grupos_materias:
                grupos_materias[id_grupo].sort(key=lambda x: x['id_materia'])
            
            # Encontrar el número máximo de materias que tiene cualquier grupo
            # Este será el número de días necesarios (uno por cada posición de examen)
            max_materias_por_grupo = max(len(materias) for materias in grupos_materias.values()) if grupos_materias else 0
            
            print(f"[DEBUG] Reorganización: {len(grupos_materias)} grupos únicos, máximo {max_materias_por_grupo} materias por grupo")
            
            # Calcular cuántos días hábiles necesitamos (un día por cada posición de examen)
            # Considerar que hay ~5 días hábiles por semana (lun-vie)
            dias_necesarios_estimados = max_materias_por_grupo
            semanas_necesarias = max(3, (dias_necesarios_estimados + 4) // 5)  # Redondear hacia arriba
            dias_totales_necesarios = semanas_necesarias * 7  # Días totales incluyendo fines de semana
            
            # Extender la ventana si es necesario
            fecha_fin_actual = ventana.fecha_fin_examenes
            fecha_fin_necesaria = fecha_inicio + timedelta(days=dias_totales_necesarios)
            
            if fecha_fin_necesaria > fecha_fin_actual:
                print(f"[DEBUG] Extendiendo ventana de {fecha_fin_actual} a {fecha_fin_necesaria} para acomodar {max_materias_por_grupo} posiciones de examen")
                ventana.fecha_fin_examenes = fecha_fin_necesaria
                self.db.flush()
            
            # Calcular días disponibles: necesitamos al menos un día por cada posición de examen
            dias_disponibles = self._calcular_dias_disponibles(fecha_inicio, dias_inhabiles, ventana, minimo_dias=max_materias_por_grupo)
            
            # Si aún no tenemos suficientes días, intentar extender más dentro de la ventana
            dias_inhabiles_set = set(dias_inhabiles) if dias_inhabiles else set()
            dias_extras_agregados = 0
            fecha_actual = dias_disponibles[-1] + timedelta(days=1) if dias_disponibles else fecha_inicio
            
            while len(dias_disponibles) < max_materias_por_grupo and fecha_actual <= ventana.fecha_fin_examenes:
                if fecha_actual.weekday() < 5 and fecha_actual not in dias_inhabiles_set:
                    dias_disponibles.append(fecha_actual)
                    dias_extras_agregados += 1
                    print(f"[DEBUG] Día adicional agregado: {fecha_actual} para acomodar {len(dias_disponibles)}/{max_materias_por_grupo} posiciones de examen")
                fecha_actual += timedelta(days=1)
            
            if len(dias_disponibles) < max_materias_por_grupo:
                advertencias = [f"Hay {max_materias_por_grupo} posiciones de examen pero solo {len(dias_disponibles)} días hábiles disponibles en la ventana (hasta {ventana.fecha_fin_examenes}). {max_materias_por_grupo - len(dias_disponibles)} posiciones pueden no tener examen programado."]
            else:
                advertencias = []
                if dias_extras_agregados > 0:
                    print(f"[DEBUG] Se agregaron {dias_extras_agregados} días adicionales para acomodar todas las {max_materias_por_grupo} posiciones de examen")
                print(f"[DEBUG] Total de días disponibles: {len(dias_disponibles)} para {max_materias_por_grupo} posiciones de examen")
            
            # 8. Generar solicitudes: asignar por posición de examen, no por materia
            # Día 1: Primer examen de TODOS los grupos (independientemente del semestre)
            # Día 2: Segundo examen de TODOS los grupos
            # etc.
            solicitudes_creadas = 0
            conflictos = []
            
            print(f"[DEBUG] Días disponibles: {len(dias_disponibles)}, necesarios: {max_materias_por_grupo}")
            
            # Asignar fechas por posición de examen (0, 1, 2, ...)
            # Reglas: misma materia → mismo día, misma hora; hora = horario de clases.
            # Plataforma → SALA DE CÓMPUTO (diferente por grupo); Escrito → aula del horario de clases (diferente por grupo).
            for posicion_examen in range(max_materias_por_grupo):
                if posicion_examen >= len(dias_disponibles):
                    conflictos.append(f"Posición de examen #{posicion_examen + 1}: No hay días disponibles (solo hay {len(dias_disponibles)} días disponibles en la ventana)")
                    continue
                
                fecha_examen = dias_disponibles[posicion_examen]
                print(f"[DEBUG] Asignando posición de examen #{posicion_examen + 1} para fecha {fecha_examen}")
                
                # Agrupar por id_materia: misma materia = mismo día, misma hora, distinta aula/sala
                por_materia = {}  # id_materia -> [(id_grupo, grupo_info, horario_clase), ...]
                for id_grupo, materias_grupo in grupos_materias.items():
                    if posicion_examen >= len(materias_grupo):
                        continue
                    materia_data = materias_grupo[posicion_examen]
                    id_materia = materia_data['id_materia']
                    grupo_info = materia_data['grupo_info']
                    horario_clase = grupo_info.get('horario')
                    if id_materia not in por_materia:
                        por_materia[id_materia] = []
                    por_materia[id_materia].append((id_grupo, grupo_info, horario_clase))
                
                for id_materia, lista_grupos in por_materia.items():
                    grupos_info = materias_grupos[id_materia]
                    nombre_materia = grupos_info.get('nombre', id_materia)
                    
                    # Tipo de examen: plataforma → sala de cómputo; escrito → aula del horario
                    materia = self.materia_repo.get_by_id(id_materia)
                    tipo_examen = (materia.tipo_examen or 'plataforma').strip().lower() if materia else 'plataforma'
                    
                    # Una sola hora para toda la materia (horario de clases del primer grupo con hora definida)
                    first_horario = next((h for _, _, h in lista_grupos if h and getattr(h, 'hora_inicio', None) and getattr(h, 'hora_fin', None)), None)
                    if not first_horario:
                        for _, grupo_info, h in lista_grupos:
                            conflictos.append(f"Grupo {grupo_info['id_grupo']} - Materia {nombre_materia} (posición #{posicion_examen + 1}): No tiene horario de clase con hora definida")
                        continue
                    hora_inicio = first_horario.hora_inicio
                    hora_fin = first_horario.hora_fin
                    
                    # Área salud: mostrar todo; aulas pendientes (id_aula=None). Si hay conflicto, se marca en rojo al mostrar.
                    id_aula = None  # Dejar pendiente
                    if tipo_examen == 'plataforma':
                        for (id_grupo, grupo_info, horario_clase) in lista_grupos:
                            id_horario_grupo = self._generar_id_solicitud(id_periodo, id_evaluacion, f"{id_materia}-{grupo_info['id_grupo']}")
                            resultado = self._crear_solicitud_examen_individual(
                                id_horario=id_horario_grupo,
                                id_materia=id_materia,
                                grupo_info=grupo_info,
                                horario_referencia=horario_clase or first_horario,
                                id_periodo=id_periodo,
                                id_evaluacion=id_evaluacion,
                                fecha_examen=fecha_examen,
                                hora_inicio=hora_inicio,
                                hora_fin=hora_fin,
                                id_aula=id_aula,
                                aulas_disponibles=aulas_disponibles,
                                asignaciones_existentes=asignaciones_existentes
                            )
                            if resultado['exito']:
                                solicitudes_creadas += 1
                                print(f"[DEBUG] Grupo {grupo_info['id_grupo']} (plataforma) materia {nombre_materia} (posición #{posicion_examen + 1}): {fecha_examen} {hora_inicio}-{hora_fin} [aula pendiente]")
                            else:
                                conflictos.append(f"Grupo {grupo_info['id_grupo']} - Materia {nombre_materia} (posición #{posicion_examen + 1}): {resultado['error']}")
                    else:
                        for (id_grupo, grupo_info, horario_clase) in lista_grupos:
                            if not horario_clase:
                                conflictos.append(f"Grupo {grupo_info['id_grupo']} - Materia {nombre_materia} (posición #{posicion_examen + 1}): No tiene horario de clase registrado")
                                continue
                            id_horario_grupo = self._generar_id_solicitud(id_periodo, id_evaluacion, f"{id_materia}-{grupo_info['id_grupo']}")
                            resultado = self._crear_solicitud_examen_individual(
                                id_horario=id_horario_grupo,
                                id_materia=id_materia,
                                grupo_info=grupo_info,
                                horario_referencia=horario_clase,
                                id_periodo=id_periodo,
                                id_evaluacion=id_evaluacion,
                                fecha_examen=fecha_examen,
                                hora_inicio=hora_inicio,
                                hora_fin=hora_fin,
                                id_aula=id_aula,
                                aulas_disponibles=aulas_disponibles,
                                asignaciones_existentes=asignaciones_existentes
                            )
                            if resultado['exito']:
                                solicitudes_creadas += 1
                                print(f"[DEBUG] Grupo {grupo_info['id_grupo']} (escrito) materia {nombre_materia} (posición #{posicion_examen + 1}): {fecha_examen} {hora_inicio}-{hora_fin} [aula pendiente]")
                            else:
                                conflictos.append(f"Grupo {grupo_info['id_grupo']} - Materia {nombre_materia} (posición #{posicion_examen + 1}): {resultado['error']}")
                
                print(f"[DEBUG] Posición de examen #{posicion_examen + 1} (fecha {fecha_examen}): procesadas {len(por_materia)} materias")
            
            self.db.commit()
            
            # Log final con resumen completo
            print(f"[DEBUG] ========== RESUMEN FINAL DE GENERACIÓN ==========")
            print(f"[DEBUG] Solicitudes creadas: {solicitudes_creadas}")
            print(f"[DEBUG] Conflictos: {len(conflictos)}")
            if conflictos:
                print(f"[DEBUG]   Detalles de conflictos:")
                for i, conflicto in enumerate(conflictos[:10], 1):
                    print(f"[DEBUG]     {i}. {conflicto}")
                if len(conflictos) > 10:
                    print(f"[DEBUG]     ... y {len(conflictos) - 10} más")
            print(f"[DEBUG] Advertencias: {len(advertencias)}")
            if advertencias:
                for advertencia in advertencias:
                    print(f"[DEBUG]   - {advertencia}")
            
            # Verificar cuántos grupos únicos se incluyeron en las solicitudes creadas
            solicitudes_creadas_objs = self.solicitud_repo.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
            grupos_en_solicitudes = set()
            for solicitud in solicitudes_creadas_objs:
                if solicitud.id_materia in materias_grupos:
                    grupos_materia = materias_grupos[solicitud.id_materia]['grupos']
                    for grupo_info in grupos_materia:
                        grupos_en_solicitudes.add(grupo_info['id_grupo'])
            print(f"[DEBUG] Grupos únicos incluidos en solicitudes creadas: {len(grupos_en_solicitudes)}")
            print(f"[DEBUG] IDs de grupos: {sorted(list(grupos_en_solicitudes))[:20]}{'...' if len(grupos_en_solicitudes) > 20 else ''}")
            print(f"[DEBUG] ================================================")
            
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
    
    def _calcular_dias_disponibles(self, fecha_inicio: date, dias_inhabiles: List[date], ventana, minimo_dias: int = 5) -> List[date]:
        """
        Calcula los días disponibles para exámenes (mínimo 5 días hábiles, excluyendo días inhábiles).
        Puede extenderse hasta el final de la ventana si es necesario.
        IMPORTANTE: La fecha_inicio debe ser el primer día disponible si es hábil.
        """
        dias_disponibles = []
        fecha_actual = fecha_inicio
        dias_inhabiles_set = set(dias_inhabiles) if dias_inhabiles else set()
        
        print(f"[DEBUG] _calcular_dias_disponibles: fecha_inicio={fecha_inicio}, ventana_inicio={ventana.fecha_inicio_examenes}, ventana_fin={ventana.fecha_fin_examenes}, minimo_dias={minimo_dias}")
        print(f"[DEBUG] Días inhábiles: {dias_inhabiles_set}")
        
        # Asegurar que fecha_inicio esté dentro de la ventana
        if fecha_actual < ventana.fecha_inicio_examenes:
            print(f"[DEBUG] fecha_inicio ({fecha_actual}) es anterior a ventana_inicio ({ventana.fecha_inicio_examenes}), ajustando...")
            fecha_actual = ventana.fecha_inicio_examenes
        elif fecha_actual > ventana.fecha_fin_examenes:
            print(f"[DEBUG] fecha_inicio ({fecha_actual}) es posterior a ventana_fin ({ventana.fecha_fin_examenes}), ajustando a ventana_inicio...")
            fecha_actual = ventana.fecha_inicio_examenes
        
        print(f"[DEBUG] Fecha inicial para búsqueda: {fecha_actual} (día de semana: {fecha_actual.weekday()}, 0=Lun, 6=Dom)")
        
        # Buscar días disponibles hasta el mínimo o hasta el final de la ventana
        # IMPORTANTE: Empezar desde fecha_actual (que puede ser fecha_inicio o ventana.fecha_inicio_examenes)
        while fecha_actual <= ventana.fecha_fin_examenes and len(dias_disponibles) < minimo_dias:
            # Excluir sábados (5) y domingos (6)
            es_dia_habil = fecha_actual.weekday() < 5
            es_dia_inhabil = fecha_actual in dias_inhabiles_set
            
            if es_dia_habil and not es_dia_inhabil:
                dias_disponibles.append(fecha_actual)
                print(f"[DEBUG] Día disponible agregado: {fecha_actual} (posición {len(dias_disponibles)})")
            else:
                razon = "fin de semana" if not es_dia_habil else "día inhábil"
                print(f"[DEBUG] Día excluido: {fecha_actual} ({razon})")
            
            fecha_actual += timedelta(days=1)
        
        print(f"[DEBUG] Total días disponibles encontrados: {len(dias_disponibles)} (mínimo requerido: {minimo_dias})")
        if dias_disponibles:
            print(f"[DEBUG] Primer día disponible: {dias_disponibles[0]}, Último día disponible: {dias_disponibles[-1]}")
        
        return dias_disponibles
    
    def _agrupar_materias_grupos(self, horarios: List[HorarioClase]) -> Dict:
        """
        Agrupa horarios por materia y extrae información de grupos.
        """
        materias_dict = {}
        
        for horario in horarios:
            if not horario.id_materia or not horario.id_grupo:
                continue  # Saltar horarios sin materia o grupo válido
                
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
                'horario': horario  # Guardar el horario de clase para usar su hora y aula
            }
            
            # Evitar duplicados por id_grupo, pero si ya existe, actualizar el horario si este tiene más información
            grupos_ids_existentes = [g['id_grupo'] for g in materias_dict[id_materia]['grupos']]
            if grupo_info['id_grupo'] not in grupos_ids_existentes:
                materias_dict[id_materia]['grupos'].append(grupo_info)
                materias_dict[id_materia]['total_alumnos'] += grupo_info['numero_alumnos']
            else:
                # Si el grupo ya existe, actualizar el horario si el nuevo tiene hora/aula y el anterior no
                grupo_existente = next((g for g in materias_dict[id_materia]['grupos'] if g['id_grupo'] == grupo_info['id_grupo']), None)
                if grupo_existente:
                    horario_actual = grupo_existente.get('horario')
                    # Preferir el horario que tenga hora_inicio y aula definidos
                    if horario_actual:
                        if (not horario_actual.hora_inicio or not horario_actual.id_aula) and horario.hora_inicio and horario.id_aula:
                            grupo_existente['horario'] = horario
                            print(f"[DEBUG] Actualizado horario para grupo {grupo_info['id_grupo']} con horario más completo")
        
        # Log para depuración
        total_grupos = sum(len(info['grupos']) for info in materias_dict.values())
        print(f"[DEBUG] _agrupar_materias_grupos: {len(materias_dict)} materias, {total_grupos} grupos únicos en total")
        grupos_por_materia_count = {}
        for id_materia, info in materias_dict.items():
            grupos_nombres = [g['nombre'] for g in info['grupos']]
            grupos_ids = [g['id_grupo'] for g in info['grupos']]
            print(f"[DEBUG]   Materia {id_materia} ({info['nombre']}): {len(info['grupos'])} grupos - IDs: {grupos_ids}, Nombres: {grupos_nombres}")
            grupos_por_materia_count[id_materia] = len(info['grupos'])
        
        print(f"[DEBUG] Resumen: {sum(grupos_por_materia_count.values())} grupos totales distribuidos en {len(materias_dict)} materias")
        
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
        asignaciones_existentes: Dict,
        horario_preferido_index: Optional[int] = None
    ) -> Dict:
        """
        Crea una solicitud de examen para una materia en una fecha específica.
        """
        try:
            # 1. Determinar hora (usar horario del horario regular o estándar)
            resultado_hora = self._encontrar_hora_disponible(
                grupos_info['horario_referencia'],
                fecha_examen,
                grupos_info['total_alumnos'],
                aulas_disponibles,
                asignaciones_existentes,
                horario_preferido_index
            )
            
            if resultado_hora is None:
                return {
                    'exito': False,
                    'error': 'No se encontró hora disponible para la fecha especificada'
                }
            
            hora_inicio, hora_fin = resultado_hora
            
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
            grupos_asociados = 0
            grupos_ids_asociados = []
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
                grupos_asociados += 1
                grupos_ids_asociados.append(grupo_info['id_grupo'])
            
            print(f"[DEBUG] Solicitud {id_horario} para materia {id_materia} ({grupos_info['nombre']}): {grupos_asociados} grupos asociados de {len(grupos_info['grupos'])} grupos en la materia")
            print(f"[DEBUG]   Grupos asociados: {grupos_ids_asociados}")
            
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
        asignaciones_existentes: Dict,
        horario_preferido_index: Optional[int] = None
    ) -> Optional[Tuple[time, time]]:
        """
        Encuentra una hora disponible para el examen en la fecha especificada.
        Si se proporciona horario_preferido_index, intenta usar ese horario específico primero.
        """
        # Si se especifica un horario preferido, intentar usarlo primero
        if horario_preferido_index is not None and 0 <= horario_preferido_index < len(self.HORARIOS_EXAMEN):
            hora_inicio, hora_fin = self.HORARIOS_EXAMEN[horario_preferido_index]
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
        # Si ya intentamos el preferido, saltarlo
        for idx, (hora_inicio, hora_fin) in enumerate(self.HORARIOS_EXAMEN):
            if horario_preferido_index is not None and idx == horario_preferido_index:
                continue  # Ya lo intentamos arriba
            
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
        Primero intenta aulas que cumplan exactamente la capacidad, luego permite flexibilidad.
        """
        # Ordenar aulas por capacidad (mayor primero)
        aulas_ordenadas = sorted(aulas_disponibles, key=lambda a: a.capacidad, reverse=True)
        
        # Primera pasada: buscar aulas que cumplan exactamente o excedan la capacidad
        for aula in aulas_ordenadas:
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
        
        # Segunda pasada: si no encontramos aula ideal, permitir aulas con capacidad
        # hasta 20% menor (para grupos grandes que pueden dividirse o ajustarse)
        capacidad_minima = max(1, int(capacidad_necesaria * 0.8))
        for aula in aulas_ordenadas:
            if aula.capacidad < capacidad_minima:
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
                print(f"[DEBUG] Aula {aula.id_aula} seleccionada con capacidad {aula.capacidad} (necesaria: {capacidad_necesaria}) - capacidad ligeramente menor aceptada")
                return aula.id_aula
        
        # Tercera pasada: si aún no encontramos aula, intentar con cualquier aula disponible
        # sin verificar capacidad (último recurso para evitar conflictos)
        for aula in aulas_ordenadas:
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
                print(f"[DEBUG] ⚠️ Aula {aula.id_aula} seleccionada con capacidad {aula.capacidad} (necesaria: {capacidad_necesaria}) - sin verificar capacidad (último recurso)")
                return aula.id_aula
        
        return None
    
    def _buscar_aula_disponible_para_grupo(
        self,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        capacidad_necesaria: int,
        aulas_disponibles: List,
        asignaciones_existentes: Dict,
        aulas_excluidas: set = None
    ) -> Optional[str]:
        """
        Busca un aula disponible para un grupo específico, excluyendo aulas ya usadas por otros grupos.
        """
        if aulas_excluidas is None:
            aulas_excluidas = set()
        
        # Ordenar aulas por capacidad (mayor primero)
        aulas_ordenadas = sorted(aulas_disponibles, key=lambda a: a.capacidad, reverse=True)
        
        # Primera pasada: buscar aulas que cumplan exactamente o excedan la capacidad
        for aula in aulas_ordenadas:
            if aula.id_aula in aulas_excluidas:
                continue  # Excluir aulas ya usadas por otros grupos
            
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
        
        # Segunda pasada: permitir aulas con capacidad hasta 20% menor
        capacidad_minima = max(1, int(capacidad_necesaria * 0.8))
        for aula in aulas_ordenadas:
            if aula.id_aula in aulas_excluidas:
                continue
            
            if aula.capacidad < capacidad_minima:
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
                print(f"[DEBUG] Aula {aula.id_aula} seleccionada con capacidad {aula.capacidad} (necesaria: {capacidad_necesaria}) - capacidad ligeramente menor aceptada")
                return aula.id_aula
        
        # Tercera pasada: cualquier aula disponible sin verificar capacidad
        for aula in aulas_ordenadas:
            if aula.id_aula in aulas_excluidas:
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
                print(f"[DEBUG] ⚠️ Aula {aula.id_aula} seleccionada con capacidad {aula.capacidad} (necesaria: {capacidad_necesaria}) - sin verificar capacidad (último recurso)")
                return aula.id_aula
        
        return None
    
    def _elegir_sala_computo_carrera(
        self,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        aulas_en_horarios_carrera: set,
        salas_computo: List,
        asignaciones_existentes: Dict,
        numero_alumnos: int
    ) -> Optional[str]:
        """
        Elige una sala de cómputo para examen en plataforma.
        Prioriza salas usadas en la carrera (ej. CETI-SO). Evita conflictos si hay opción;
        si todas tienen conflicto, asigna de todas formas la primera preferida.
        """
        if not salas_computo:
            return None
        salas_carrera = [a for a in salas_computo if a.id_aula in aulas_en_horarios_carrera]
        salas_resto = [a for a in salas_computo if a.id_aula not in aulas_en_horarios_carrera]
        candidatas = salas_carrera + salas_resto
        primera_preferida = candidatas[0].id_aula if candidatas else None
        for aula in candidatas:
            key = (fecha, hora_inicio, aula.id_aula)
            if key in asignaciones_existentes:
                continue
            conflictos_aula = self.asignacion_aula_repo.get_by_aula_fecha_hora(
                aula.id_aula, fecha, hora_inicio, hora_fin
            )
            if not conflictos_aula and (aula.capacidad is None or aula.capacidad >= numero_alumnos):
                return aula.id_aula
        return primera_preferida
    
    def _crear_solicitud_examen_individual(
        self,
        id_horario: str,
        id_materia: str,
        grupo_info: Dict,
        horario_referencia: HorarioClase,
        id_periodo: str,
        id_evaluacion: str,
        fecha_examen: date,
        hora_inicio: time,
        hora_fin: time,
        id_aula: Optional[str],
        aulas_disponibles: List,
        asignaciones_existentes: Dict
    ) -> Dict:
        """
        Crea una solicitud de examen para un solo grupo con hora y opcionalmente aula.
        Si id_aula es None, no se crea AsignacionAula (aula en blanco).
        """
        try:
            # 1. Crear solicitud de examen
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
            
            # 2. Asociar grupo
            hash_input = f"{id_horario}-{grupo_info['id_grupo']}"
            hash_obj = hashlib.md5(hash_input.encode())
            id_examen_grupo = f"EG{hash_obj.hexdigest()[:18].upper()}"
            grupo_examen_data = GrupoExamenCreate(
                id_examen_grupo=id_examen_grupo,
                id_horario=id_horario,
                id_grupo=grupo_info['id_grupo']
            )
            grupo_examen = GrupoExamen(**grupo_examen_data.dict())
            self.db.add(grupo_examen)
            
            # 3. Asignar aula y aplicador solo si id_aula está definido (si no, aula en blanco)
            if id_aula:
                id_aplicador = None
                if horario_referencia and hasattr(horario_referencia, 'id_profesor'):
                    id_aplicador = horario_referencia.id_profesor
                if id_aplicador:
                    asignaciones_profesor = self.asignacion_aula_repo.get_by_profesor_aplicador(id_aplicador)
                    for asignacion in asignaciones_profesor:
                        solicitud_prof = self.solicitud_repo.get_by_id(asignacion.id_horario)
                        if solicitud_prof and solicitud_prof.fecha_examen == fecha_examen:
                            if solicitud_prof.hora_inicio < hora_fin and solicitud_prof.hora_fin > hora_inicio:
                                id_aplicador = self._buscar_aplicador_disponible(fecha_examen, hora_inicio, hora_fin)
                                break
                if not id_aplicador:
                    id_aplicador = self._buscar_aplicador_disponible(fecha_examen, hora_inicio, hora_fin)
                if not id_aplicador:
                    self.db.delete(solicitud)
                    return {
                        'exito': False,
                        'error': 'No se encontró profesor aplicador disponible'
                    }
                hash_input_aula = f"{id_horario}-{id_aula}"
                hash_obj_aula = hashlib.md5(hash_input_aula.encode())
                id_examen_aula = f"AA{hash_obj_aula.hexdigest()[:18].upper()}"
                asignacion_data = AsignacionAulaCreate(
                    id_examen_aula=id_examen_aula,
                    id_horario=id_horario,
                    id_aula=id_aula,
                    id_profesor_aplicador=id_aplicador
                )
                asignacion = AsignacionAula(**asignacion_data.dict())
                self.db.add(asignacion)
                asignaciones_existentes[(fecha_examen, hora_inicio, id_aula)] = id_horario
            
            # 4. Asignar sinodal
            self._asignar_sinodal(
                id_horario,
                id_materia,
                fecha_examen,
                hora_inicio,
                hora_fin
            )
            
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
        Excluye a los profesores titulares (que imparten la materia).
        """
        from app.models.HorarioClase import HorarioClase
        from sqlalchemy import distinct
        
        # Obtener profesores titulares de la materia (los que imparten clases)
        profesores_titulares = [
            row[0] for row in self.db.query(distinct(HorarioClase.id_profesor)).filter(
                HorarioClase.id_materia == id_materia
            ).all()
            if row[0]  # Filtrar None
        ]
        
        # Obtener profesores con permiso sinodal para esta materia
        permisos = self.permiso_repo.get_by_materia(id_materia)
        
        if not permisos:
            return None
        
        # Verificar disponibilidad de cada sinodal
        for permiso in permisos:
            id_profesor = permiso.id_profesor
            
            # Excluir profesores titulares (no pueden ser sinodales de su propia materia)
            if id_profesor in profesores_titulares:
                continue
            
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

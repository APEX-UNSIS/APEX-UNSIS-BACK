from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import httpx
from datetime import datetime
import logging
import re

from app.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.UsuarioSchema import UsuarioResponse
from app.models.Carrera import Carrera
from app.models.GrupoEscolar import GrupoEscolar
from app.models.Aula import Aula
from app.models.Profesor import Profesor
from app.models.Materia import Materia
from app.models.PeriodoAcademico import PeriodoAcademico
from app.models.HorarioClase import HorarioClase

router = APIRouter(prefix="/admin", tags=["admin"])

# URL base de la API externa
API_HORARIOS_BASE_URL = "http://serv-horarios.unsis.lan/api"

# Periodos permitidos para sincronización
PERIODOS_PERMITIDOS = ["2526A", "2425B"]

# Configurar logging
logger = logging.getLogger(__name__)

def log_progress(message: str, logs: List[str] = None):
    """Agrega un log con timestamp y lo imprime"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    if logs is not None:
        logs.append(log_message)


def filtrar_carreras_duplicadas(carreras: List[Dict]) -> tuple:
    """
    Filtra carreras duplicadas, quedándose solo con la más reciente de cada tipo.
    También crea un mapeo de carreras unificadas para actualizar referencias.
    
    Agrupa por nombre base (sin año) y selecciona:
    1. La que tiene vigente=True si existe
    2. La más reciente según el año en el nombre
    3. La clave más reciente como fallback
    
    Returns:
        Tuple[List[Dict], Dict[str, str]]: (carreras_filtradas, mapeo_carreras)
        mapeo_carreras: {clave_vieja: clave_principal} para actualizar referencias
    """
    if not isinstance(carreras, list) or len(carreras) == 0:
        return [], {}
    
    def obtener_nombre_base(nombre: str) -> str:
        """Extrae el nombre base sin el año"""
        if not nombre:
            return ""
        # Remover años al final (ej: "LICENCIATURA EN ADMINISTRACIÓN MUNICIPAL 2015" -> "LICENCIATURA EN ADMINISTRACIÓN MUNICIPAL")
        nombre_base = re.sub(r'\s+\d{4}$', '', nombre.strip())
        return nombre_base
    
    def extraer_año(nombre: str) -> int:
        """Extrae el año del nombre, retorna 0 si no encuentra"""
        if not nombre:
            return 0
        match = re.search(r'(\d{4})$', nombre)
        return int(match.group(1)) if match else 0
    
    # Agrupar por nombre base
    grupos = {}
    for carrera in carreras:
        nombre = carrera.get('nombre', '') or carrera.get('nombre_carrera', '')
        clave = carrera.get('clave', '') or carrera.get('id_carrera', '')
        
        if not nombre and not clave:
            continue
        
        nombre_base = obtener_nombre_base(nombre)
        if not nombre_base:
            nombre_base = clave  # Usar clave como fallback
        
        if nombre_base not in grupos:
            grupos[nombre_base] = []
        grupos[nombre_base].append(carrera)
    
    # Seleccionar la mejor de cada grupo y crear mapeo
    carreras_filtradas = []
    mapeo_carreras = {}  # {clave_vieja: clave_principal}
    
    for nombre_base, grupo_carreras in grupos.items():
        if len(grupo_carreras) == 1:
            carrera = grupo_carreras[0]
            clave = carrera.get('clave', '') or carrera.get('id_carrera', '')
            carreras_filtradas.append(carrera)
            mapeo_carreras[clave] = clave  # Mapear a sí misma
            continue
        
        # Priorizar: 1) vigente=True, 2) año más reciente, 3) clave más reciente
        vigentes = [c for c in grupo_carreras if c.get('vigente') is True]
        candidatas = vigentes if vigentes else grupo_carreras
        
        # Ordenar por año (más reciente primero)
        candidatas_ordenadas = sorted(
            candidatas,
            key=lambda c: (
                extraer_año(c.get('nombre', '') or c.get('nombre_carrera', '')),
                c.get('clave', '') or c.get('id_carrera', '')
            ),
            reverse=True
        )
        
        carrera_principal = candidatas_ordenadas[0]
        clave_principal = carrera_principal.get('clave', '') or carrera_principal.get('id_carrera', '')
        carreras_filtradas.append(carrera_principal)
        
        # Crear mapeo: todas las variantes apuntan a la carrera principal
        for carrera_variante in grupo_carreras:
            clave_variante = carrera_variante.get('clave', '') or carrera_variante.get('id_carrera', '')
            if clave_variante != clave_principal:
                mapeo_carreras[clave_variante] = clave_principal
            else:
                mapeo_carreras[clave_variante] = clave_principal
    
    return carreras_filtradas, mapeo_carreras


def filtrar_duplicados_por_id(datos: List[Dict], id_key: str = 'id') -> List[Dict]:
    """
    Filtra duplicados basándose en un campo ID, quedándose con el último encontrado.
    Útil para profesores, materias, aulas, etc.
    """
    if not isinstance(datos, list) or len(datos) == 0:
        return []
    
    vistos = {}
    for item in datos:
        item_id = item.get(id_key) or item.get('clave') or item.get('id_profesor') or item.get('id_materia') or item.get('id_aula')
        if item_id:
            vistos[str(item_id)] = item
    
    return list(vistos.values())


def filtrar_grupos_no_deseados(grupos: List[Dict]) -> tuple:
    """
    Filtra grupos que no son de interés:
    - Grupos que empiezan con P, p, V, v
    """
    grupos_filtrados = []
    grupos_excluidos = 0
    
    for grupo in grupos:
        id_grupo = grupo.get('id_grupo') or grupo.get('grupo') or grupo.get('clave') or grupo.get('idGrupo') or ''
        nombre_grupo = grupo.get('nombre_grupo') or grupo.get('nombre') or grupo.get('nombreGrupo') or ''
        
        # Convertir a string si es necesario
        if isinstance(id_grupo, (int, float)):
            id_grupo = str(int(id_grupo))
        if isinstance(nombre_grupo, (int, float)):
            nombre_grupo = str(int(nombre_grupo))
        
        # Verificar si el grupo empieza con P, p, V, v
        grupo_str = str(id_grupo).strip().upper()
        if grupo_str and grupo_str[0] in ['P', 'V']:
            grupos_excluidos += 1
            continue
        
        grupos_filtrados.append(grupo)
    
    return grupos_filtrados, grupos_excluidos


def filtrar_profesores_no_deseados(profesores: List[Dict]) -> tuple:
    """
    Filtra profesores que no son de interés:
    - Profesores técnicos de sala
    - Profesores de inglés genéricos
    - Técnicos de laboratorio
    - Otros roles técnicos
    """
    profesores_filtrados = []
    profesores_excluidos = 0
    
    # Palabras clave que indican profesores no deseados
    palabras_excluidas = [
        'TÉCNICO SALA',
        'TÉCNICO LAB',
        'PROFESOR INGLÉS',
        'SALA TESISTA',
        'COMITÉ TUTORIAL',
        'TÉCNICO',
        'S.O. TÉCNICO',
        'SOFTWARE TÉCNICO',
        'INFO TÉCNICO',
        'ODONT. TÉCNICO'
    ]
    
    for profesor in profesores:
        nombre_profesor = profesor.get('nombre_profesor') or profesor.get('nombre') or profesor.get('nombreCompleto') or ''
        
        # Convertir a string y normalizar
        if isinstance(nombre_profesor, (int, float)):
            nombre_profesor = str(int(nombre_profesor))
        
        nombre_upper = str(nombre_profesor).strip().upper()
        
        # Verificar si contiene alguna palabra excluida
        excluir = False
        for palabra in palabras_excluidas:
            if palabra in nombre_upper:
                excluir = True
                break
        
        if excluir:
            profesores_excluidos += 1
            continue
        
        profesores_filtrados.append(profesor)
    
    return profesores_filtrados, profesores_excluidos


def es_grupo_no_deseado(id_grupo: str) -> bool:
    """Verifica si un grupo debe ser excluido (empieza con P/p/V/v)"""
    if not id_grupo:
        return False
    grupo_str = str(id_grupo).strip().upper()
    return grupo_str and grupo_str[0] in ['P', 'V']


def es_profesor_no_deseado(nombre_profesor: str) -> bool:
    """Verifica si un profesor debe ser excluido"""
    if not nombre_profesor:
        return False
    
    nombre_upper = str(nombre_profesor).strip().upper()
    palabras_excluidas = [
        'TÉCNICO SALA', 'TÉCNICO LAB', 'PROFESOR INGLÉS', 'SALA TESISTA',
        'COMITÉ TUTORIAL', 'S.O. TÉCNICO', 'SOFTWARE TÉCNICO',
        'INFO TÉCNICO', 'ODONT. TÉCNICO'
    ]
    
    for palabra in palabras_excluidas:
        if palabra in nombre_upper:
            return True
    return False


@router.post("/sincronizar-base-datos", response_model=Dict)
async def sincronizar_base_datos(
    periodo: str = Query(..., description="Periodo académico (ej: 2526A)"),
    grupo: Optional[str] = Query(None, description="Grupo escolar específico (ej: 706). Si es None, sincroniza todos los grupos"),
    limpiar_datos: bool = Query(False, description="Si es True, borra los datos existentes antes de insertar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sincroniza la base de datos consultando la API externa de horarios.
    
    Si grupo es None, sincroniza TODAS las carreras y TODOS los grupos automáticamente.
    Si grupo se especifica, solo sincroniza ese grupo específico.
    
    Consulta http://serv-horarios.unsis.lan/api/ y actualiza:
    - Carreras
    - Grupos escolares
    - Aulas
    - Profesores
    - Materias
    - Periodos académicos
    - Horarios de clase
    
    Args:
        periodo: Periodo académico (ej: 2526A, 2025-1)
        grupo: Grupo escolar específico (ej: 706, 707). Si es None, sincroniza todos.
        limpiar_datos: Si es True, borra los datos existentes antes de insertar
    
    Returns:
        Dict con información del proceso de sincronización
    """
    if current_user.rol != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden sincronizar la base de datos"
        )
    
    # Validar que el periodo esté permitido
    if periodo not in PERIODOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Periodo no permitido. Solo se permiten los siguientes periodos: {', '.join(PERIODOS_PERMITIDOS)}"
        )
    
    try:
        # Lista de logs para retornar al frontend
        logs = []
        
        log_progress("🚀 Iniciando sincronización de base de datos...", logs)
        log_progress(f"📅 Periodo: {periodo}", logs)
        log_progress(f"👥 Grupo: {grupo if grupo else 'TODOS (sincronización automática)'}", logs)
        log_progress(f"🗑️ Limpiar datos: {'Sí' if limpiar_datos else 'No'}", logs)
        
        # 1. Consultar APIs externas base (aulas, carreras, grupos, periodos)
        url_aulas = f"{API_HORARIOS_BASE_URL}/aulas"
        url_carreras = f"{API_HORARIOS_BASE_URL}/carreras"
        url_grupos = f"{API_HORARIOS_BASE_URL}/grupos"
        url_periodos_lista = f"{API_HORARIOS_BASE_URL}/periodo/lista"
        url_periodo_actual = f"{API_HORARIOS_BASE_URL}/periodo/actual"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Obtener datos base primero
            log_progress("📡 Consultando APIs externas...", logs)
            
            # Obtener aulas
            try:
                log_progress("  📚 Consultando aulas...", logs)
                response_aulas = await client.get(url_aulas)
                response_aulas.raise_for_status()
                data_aulas_raw = response_aulas.json()
                count_aulas_raw = len(data_aulas_raw) if isinstance(data_aulas_raw, list) else 0
                
                # Filtrar duplicados por ID
                if isinstance(data_aulas_raw, list):
                    data_aulas = filtrar_duplicados_por_id(data_aulas_raw, 'id_aula')
                    count_aulas_filtradas = len(data_aulas)
                    log_progress(f"  ✅ Aulas obtenidas: {count_aulas_raw} → {count_aulas_filtradas} (filtradas: {count_aulas_raw - count_aulas_filtradas} duplicados)", logs)
                else:
                    data_aulas = []
                    log_progress(f"  ✅ Aulas obtenidas: 0 (formato no válido)", logs)
            except Exception as e:
                log_progress(f"  ⚠️ No se pudo obtener aulas: {str(e)[:100]}", logs)
                data_aulas = []
            
            # Obtener carreras
            try:
                log_progress("  🎓 Consultando carreras...", logs)
                response_carreras = await client.get(url_carreras)
                response_carreras.raise_for_status()
                data_carreras_raw = response_carreras.json()
                count_carreras_raw = len(data_carreras_raw) if isinstance(data_carreras_raw, list) else 0
                
                # Filtrar duplicados (carreras con mismo nombre base, quedarse con la más reciente)
                if isinstance(data_carreras_raw, list):
                    data_carreras, mapeo_carreras = filtrar_carreras_duplicadas(data_carreras_raw)
                    count_carreras_filtradas = len(data_carreras)
                    log_progress(f"  ✅ Carreras obtenidas: {count_carreras_raw} → {count_carreras_filtradas} (filtradas: {count_carreras_raw - count_carreras_filtradas} duplicados)", logs)
                    if mapeo_carreras:
                        carreras_mapeadas = sum(1 for k, v in mapeo_carreras.items() if k != v)
                        if carreras_mapeadas > 0:
                            log_progress(f"  🔗 {carreras_mapeadas} carreras serán unificadas (ej: 06B -> 06, 05B -> 05)", logs)
                else:
                    data_carreras = []
                    mapeo_carreras = {}
                    log_progress(f"  ✅ Carreras obtenidas: 0 (formato no válido)", logs)
            except Exception as e:
                log_progress(f"  ⚠️ No se pudo obtener carreras: {str(e)[:100]}", logs)
                data_carreras = []
                mapeo_carreras = {}
            
            # Obtener grupos (para saber qué grupos sincronizar)
            try:
                log_progress("  👥 Consultando grupos...", logs)
                response_grupos = await client.get(url_grupos)
                response_grupos.raise_for_status()
                data_grupos_raw = response_grupos.json()
                count_grupos_raw = len(data_grupos_raw) if isinstance(data_grupos_raw, list) else 0
                
                # Filtrar duplicados por ID
                if isinstance(data_grupos_raw, list):
                    data_grupos = filtrar_duplicados_por_id(data_grupos_raw, 'id_grupo')
                    count_grupos_filtrados = len(data_grupos)
                    log_progress(f"  ✅ Grupos obtenidos: {count_grupos_raw} → {count_grupos_filtrados} (filtrados: {count_grupos_raw - count_grupos_filtrados} duplicados)", logs)
                else:
                    data_grupos = []
                    log_progress(f"  ✅ Grupos obtenidos: 0 (formato no válido)", logs)
            except Exception as e:
                log_progress(f"  ⚠️ No se pudo obtener grupos: {str(e)[:100]}", logs)
                data_grupos = []
            
            # Profesores y materias se extraerán de los horarios (no hay API disponible)
            data_profesores = []
            data_materias = []
            log_progress("  ℹ️ Profesores y materias se extraerán de los horarios de grupos", logs)
            
            # Obtener periodos
            data_periodos = []
            periodo_actual_api = None
            try:
                log_progress("  📅 Consultando periodo actual...", logs)
                response_periodo_actual = await client.get(url_periodo_actual, timeout=10.0)
                if response_periodo_actual.status_code == 200:
                    periodo_actual_api = response_periodo_actual.json()
                    if isinstance(periodo_actual_api, dict):
                        periodo_actual_id = periodo_actual_api.get('periodo') or periodo_actual_api.get('id_periodo') or periodo_actual_api.get('periodog')
                        if periodo_actual_id:
                            log_progress(f"  ✅ Periodo actual de la API: {periodo_actual_id}", logs)
                            # Si el periodo proporcionado no coincide con el actual, usar el actual
                            if periodo_actual_id != periodo and not grupo:
                                log_progress(f"  ⚠️ El periodo proporcionado ({periodo}) no coincide con el actual ({periodo_actual_id}). Usando periodo actual.", logs)
                                periodo = periodo_actual_id
                    elif isinstance(periodo_actual_api, str):
                        log_progress(f"  ✅ Periodo actual de la API: {periodo_actual_api}", logs)
                        if periodo_actual_api != periodo and not grupo:
                            log_progress(f"  ⚠️ El periodo proporcionado ({periodo}) no coincide con el actual ({periodo_actual_api}). Usando periodo actual.", logs)
                            periodo = periodo_actual_api
            except Exception as e:
                log_progress(f"  ⚠️ No se pudo obtener periodo actual: {str(e)[:100]} (se usará el periodo proporcionado: {periodo})", logs)
            
            try:
                log_progress("  📅 Consultando lista de periodos...", logs)
                response_periodos = await client.get(url_periodos_lista, timeout=10.0)
                if response_periodos.status_code == 200:
                    data_periodos_raw = response_periodos.json()
                    if isinstance(data_periodos_raw, list):
                        data_periodos = data_periodos_raw
                        log_progress(f"  ✅ Periodos obtenidos: {len(data_periodos)}", logs)
                    elif isinstance(data_periodos_raw, dict):
                        # Intentar extraer lista de periodos del objeto
                        data_periodos = data_periodos_raw.get('periodos', data_periodos_raw.get('lista', []))
                        if isinstance(data_periodos, list):
                            log_progress(f"  ✅ Periodos obtenidos: {len(data_periodos)}", logs)
                        else:
                            data_periodos = []
            except Exception as e:
                log_progress(f"  ⚠️ No se pudo obtener lista de periodos: {str(e)[:100]} (se usará el periodo proporcionado: {periodo})", logs)
            
            # 2. Determinar qué grupos sincronizar
            log_progress("🔍 Determinando grupos a sincronizar...", logs)
            grupos_a_sincronizar = []
            if grupo:
                # Sincronizar solo el grupo especificado
                grupos_a_sincronizar = [grupo]
                log_progress(f"  ✅ Sincronizando grupo específico: {grupo}", logs)
            else:
                # Sincronizar todos los grupos
                if isinstance(data_grupos, list) and len(data_grupos) > 0:
                    # Extraer IDs de grupos de la API
                    grupos_unicos = set()
                    for grupo_item in data_grupos:
                        grupo_id = grupo_item.get('id_grupo') or grupo_item.get('grupo') or grupo_item.get('clave') or grupo_item.get('idGrupo')
                        if grupo_id:
                            grupo_id_str = str(grupo_id)
                            # Filtrar grupos P/V desde el inicio
                            if not es_grupo_no_deseado(grupo_id_str):
                                grupos_unicos.add(grupo_id_str)
                    grupos_a_sincronizar = sorted(list(grupos_unicos))
                    log_progress(f"  ✅ {len(grupos_a_sincronizar)} grupos obtenidos de la API de grupos (grupos P/V excluidos)", logs)
                else:
                    # Si no hay API de grupos, intentar obtener grupos únicos consultando horarios de muestra
                    log_progress("  ⚠️ No se pudo obtener lista de grupos de la API, extrayendo grupos únicos de horarios...", logs)
                    # Consultar algunos grupos de muestra para extraer todos los grupos únicos
                    grupos_unicos = set()
                    # Intentar con un rango amplio de grupos para encontrar los que existen
                    grupos_muestra = [str(i) for i in range(600, 900)]  # Grupos 600-899
                    log_progress(f"  🔍 Consultando {len(grupos_muestra)} grupos para encontrar los que tienen horarios...", logs)
                    
                    for grupo_muestra in grupos_muestra:
                        # Filtrar grupos P/V antes de consultar
                        if es_grupo_no_deseado(grupo_muestra):
                            continue
                        
                        try:
                            url_horarios_muestra = f"{API_HORARIOS_BASE_URL}/horarios/{periodo}/grupo/{grupo_muestra}"
                            response_muestra = await client.get(url_horarios_muestra, timeout=10.0)
                            if response_muestra.status_code == 200:
                                horarios_muestra = response_muestra.json()
                                if isinstance(horarios_muestra, list) and len(horarios_muestra) > 0:
                                    grupos_unicos.add(grupo_muestra)
                                    # También extraer grupos de los horarios (filtrar P/V)
                                    for h in horarios_muestra:
                                        grupo_h = h.get('idGrupo') or h.get('id_grupo')
                                        if grupo_h:
                                            grupo_h_str = str(grupo_h)
                                            if not es_grupo_no_deseado(grupo_h_str):
                                                grupos_unicos.add(grupo_h_str)
                                elif isinstance(horarios_muestra, dict):
                                    horarios_list = horarios_muestra.get('horarios', [])
                                    if len(horarios_list) > 0:
                                        grupos_unicos.add(grupo_muestra)
                                        for h in horarios_list:
                                            grupo_h = h.get('idGrupo') or h.get('id_grupo')
                                            if grupo_h:
                                                grupo_h_str = str(grupo_h)
                                                if not es_grupo_no_deseado(grupo_h_str):
                                                    grupos_unicos.add(grupo_h_str)
                        except:
                            # Grupo no existe o no tiene horarios, continuar
                            pass
                    
                    grupos_a_sincronizar = sorted(list(grupos_unicos))
                    log_progress(f"  ✅ {len(grupos_a_sincronizar)} grupos únicos encontrados: {grupos_a_sincronizar[:20]}{'...' if len(grupos_a_sincronizar) > 20 else ''}", logs)
            
            if not grupos_a_sincronizar:
                log_progress("❌ ERROR: No se pudo determinar qué grupos sincronizar", logs)
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo determinar qué grupos sincronizar. Por favor, especifica un grupo o asegúrate de que la API de grupos esté disponible."
                )
            
            # Filtrar grupos según el periodo con rangos de centenas:
            # Periodo A: 100-199, 300-399, 500-599, 700-799, 900-999, 1100-1199
            # Periodo B: 200-299, 400-499, 600-699, 800-899, 1000-1099, 1200-1299
            def obtener_numero_grupo(grupo_id: str) -> Optional[int]:
                """Extrae el número completo del grupo (primer número encontrado)"""
                import re
                numeros = re.findall(r'\d+', str(grupo_id))
                if numeros:
                    # Usar el primer número encontrado (puede ser 100, 701, 1001, 1100, etc.)
                    return int(numeros[0])
                return None
            
            def pertenece_periodo_a(numero: int) -> bool:
                """Determina si un número pertenece al periodo A (rangos de centenas impares)"""
                return (100 <= numero <= 199 or   # 100-199
                        300 <= numero <= 399 or   # 300-399
                        500 <= numero <= 599 or   # 500-599
                        700 <= numero <= 799 or   # 700-799
                        900 <= numero <= 999 or   # 900-999
                        1100 <= numero <= 1199)   # 1100-1199
            
            def pertenece_periodo_b(numero: int) -> bool:
                """Determina si un número pertenece al periodo B (rangos de centenas pares)"""
                return (200 <= numero <= 299 or   # 200-299
                        400 <= numero <= 499 or   # 400-499
                        600 <= numero <= 699 or   # 600-699
                        800 <= numero <= 899 or   # 800-899
                        1000 <= numero <= 1099 or # 1000-1099
                        1200 <= numero <= 1299)   # 1200-1299
            
            if periodo.upper().endswith('A'):
                log_progress("🔍 Filtrando grupos: Periodo A - 100-199, 300-399, 500-599, 700-799, 900-999, 1100-1199", logs)
                grupos_filtrados = []
                for grupo_id in grupos_a_sincronizar:
                    numero_grupo = obtener_numero_grupo(grupo_id)
                    if numero_grupo is not None and pertenece_periodo_a(numero_grupo):
                        grupos_filtrados.append(grupo_id)
                grupos_a_sincronizar = grupos_filtrados
                log_progress(f"  ✅ Grupos filtrados: {len(grupos_a_sincronizar)} grupos para periodo A", logs)
            elif periodo.upper().endswith('B'):
                log_progress("🔍 Filtrando grupos: Periodo B - 200-299, 400-499, 600-699, 800-899, 1000-1099, 1200-1299", logs)
                grupos_filtrados = []
                for grupo_id in grupos_a_sincronizar:
                    numero_grupo = obtener_numero_grupo(grupo_id)
                    if numero_grupo is not None and pertenece_periodo_b(numero_grupo):
                        grupos_filtrados.append(grupo_id)
                grupos_a_sincronizar = grupos_filtrados
                log_progress(f"  ✅ Grupos filtrados: {len(grupos_a_sincronizar)} grupos para periodo B", logs)
            else:
                log_progress(f"⚠️ Periodo '{periodo}' no termina en A o B, no se filtrarán grupos por paridad", logs)
            
            # Filtrar grupos que empiezan con P/p/V/v (ANTES de consultar horarios)
            grupos_antes_filtro_pv = len(grupos_a_sincronizar)
            grupos_a_sincronizar = [g for g in grupos_a_sincronizar if not es_grupo_no_deseado(str(g))]
            grupos_excluidos_pv = grupos_antes_filtro_pv - len(grupos_a_sincronizar)
            if grupos_excluidos_pv > 0:
                log_progress(f"  🚫 {grupos_excluidos_pv} grupos excluidos (empiezan con P/V) - no se consultarán sus horarios", logs)
            
            if not grupos_a_sincronizar:
                log_progress("❌ ERROR: No quedaron grupos después del filtrado", logs)
                raise HTTPException(
                    status_code=400,
                    detail=f"No quedaron grupos después de filtrar por periodo {periodo} y excluir grupos P/V. Verifica que el periodo sea correcto (A=impares, B=pares)."
                )
            
            log_progress(f"📋 Sincronizando {len(grupos_a_sincronizar)} grupos: {grupos_a_sincronizar[:10]}{'...' if len(grupos_a_sincronizar) > 10 else ''}", logs)
            
            # 3. Consultar horarios para cada grupo
            log_progress("📥 Descargando horarios de grupos...", logs)
            todos_horarios = []
            grupos_exitosos = 0
            grupos_fallidos = []
            
            for idx, grupo_actual in enumerate(grupos_a_sincronizar, 1):
                try:
                    url_horarios = f"{API_HORARIOS_BASE_URL}/horarios/{periodo}/grupo/{grupo_actual}"
                    if idx % 10 == 0 or idx == 1 or idx == len(grupos_a_sincronizar):
                        log_progress(f"  [{idx}/{len(grupos_a_sincronizar)}] Consultando horarios para grupo {grupo_actual}...", logs)
                    response_horarios = await client.get(url_horarios, timeout=30.0)
                    response_horarios.raise_for_status()
                    horarios_grupo = response_horarios.json()
                    
                    if isinstance(horarios_grupo, list):
                        todos_horarios.extend(horarios_grupo)
                        grupos_exitosos += 1
                    elif isinstance(horarios_grupo, dict):
                        horarios_list = horarios_grupo.get('horarios', [])
                        todos_horarios.extend(horarios_list)
                        grupos_exitosos += 1
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        # Grupo no existe, no es un error crítico
                        pass
                    else:
                        grupos_fallidos.append({'grupo': grupo_actual, 'error': f"HTTP {e.response.status_code}"})
                except Exception as e:
                    grupos_fallidos.append({'grupo': grupo_actual, 'error': str(e)[:100]})
            
            log_progress(f"✅ Total de horarios obtenidos: {len(todos_horarios)} de {grupos_exitosos} grupos exitosos", logs)
            if grupos_fallidos:
                log_progress(f"⚠️ Grupos con errores: {len(grupos_fallidos)}", logs)
            data_horarios = todos_horarios
            
            # Extraer profesores y materias únicos de los horarios (sin duplicados)
            log_progress("📥 Extrayendo profesores y materias de los horarios...", logs)
            profesores_unicos = {}
            materias_unicas = {}
            
            for horario in todos_horarios:
                # Extraer profesor
                id_profesor = horario.get('id_profesor') or horario.get('idprofesor')
                nombre_profesor = horario.get('nombre_profesor') or horario.get('nombreCompleto')
                if id_profesor and nombre_profesor:
                    id_profesor_str = str(id_profesor)
                    # Solo agregar si no existe o si el nombre es más completo
                    if id_profesor_str not in profesores_unicos or len(nombre_profesor) > len(profesores_unicos[id_profesor_str].get('nombre_profesor', '')):
                        profesores_unicos[id_profesor_str] = {
                            'id_profesor': id_profesor_str,
                            'nombre_profesor': nombre_profesor
                        }
                
                # Extraer materia
                id_materia = horario.get('id_materia') or horario.get('asignatura')
                nombre_materia = horario.get('nombre_materia') or horario.get('materia')
                if id_materia and nombre_materia:
                    id_materia_str = str(id_materia)
                    # Truncar nombre si es muy largo
                    nombre_truncado = nombre_materia
                    if len(nombre_materia.encode('utf-8')) > 50:
                        nombre_truncado = nombre_materia[:47] + "..."
                    # Solo agregar si no existe o si el nombre es más completo
                    if id_materia_str not in materias_unicas or len(nombre_truncado) > len(materias_unicas[id_materia_str].get('nombre_materia', '')):
                        materias_unicas[id_materia_str] = {
                            'id_materia': id_materia_str,
                            'nombre_materia': nombre_truncado
                        }
            
            data_profesores = list(profesores_unicos.values())
            data_materias = list(materias_unicas.values())
            log_progress(f"  ✅ {len(data_profesores)} profesores únicos extraídos de horarios", logs)
            log_progress(f"  ✅ {len(data_materias)} materias únicas extraídas de horarios", logs)
            
            # Consolidar datos - normalizar formatos (array directo o objeto con propiedad)
            def normalize_data(data, key):
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # Intentar diferentes nombres de propiedades comunes
                    return data.get(key, data.get(key.rstrip('s'), data.get(key + 's', [])))
                return []
            
            data = {
                'horarios': normalize_data(data_horarios, 'horarios'),
                'aulas': normalize_data(data_aulas, 'aulas'),
                'carreras': normalize_data(data_carreras, 'carreras'),
                'profesores': normalize_data(data_profesores, 'profesores'),
                'materias': normalize_data(data_materias, 'materias'),
                'grupos': normalize_data(data_grupos, 'grupos'),
                'periodos': normalize_data(data_periodos, 'periodos'),
                'periodo': {'id_periodo': periodo, 'nombre_periodo': periodo, 'periodog': periodo},
                '_mapeo_carreras': mapeo_carreras  # Guardar mapeo para uso posterior
            }
            
            log_progress("📊 Datos consolidados:", logs)
            log_progress(f"  - Horarios: {len(data['horarios'])}", logs)
            log_progress(f"  - Aulas: {len(data['aulas'])}", logs)
            log_progress(f"  - Carreras: {len(data['carreras'])}", logs)
            log_progress(f"  - Profesores: {len(data['profesores'])}", logs)
            log_progress(f"  - Materias: {len(data['materias'])}", logs)
            log_progress(f"  - Grupos: {len(data['grupos'])}", logs)
            
            # 2. Verificar si la BD está vacía
            log_progress("🔍 Verificando estado de la base de datos...", logs)
            total_carreras = db.query(Carrera).count()
            total_grupos = db.query(GrupoEscolar).count()
            total_aulas = db.query(Aula).count()
            total_profesores = db.query(Profesor).count()
            total_materias = db.query(Materia).count()
            total_periodos = db.query(PeriodoAcademico).count()
            total_horarios = db.query(HorarioClase).count()
            
            bd_vacia = (total_carreras == 0 and total_grupos == 0 and total_aulas == 0 and 
                       total_profesores == 0 and total_materias == 0 and total_periodos == 0 and 
                       total_horarios == 0)
            
            if bd_vacia:
                log_progress("✅ Base de datos vacía detectada. Se insertarán todos los datos automáticamente.", logs)
            elif limpiar_datos:
                log_progress("🗑️ Limpiando datos existentes (excepto usuarios)...", logs)
                # Limpiar horarios primero (por las foreign keys)
                db.query(HorarioClase).delete()
                # Limpiar grupos, aulas, profesores, materias, carreras, periodos
                # IMPORTANTE: NO se borran usuarios
                db.query(GrupoEscolar).delete()
                db.query(Aula).delete()
                db.query(Profesor).delete()
                db.query(Materia).delete()
                db.query(Carrera).delete()
                db.query(PeriodoAcademico).delete()
                db.commit()
                log_progress("✅ Datos limpiados exitosamente (usuarios preservados)", logs)
            else:
                log_progress("ℹ️ Base de datos tiene datos existentes. Se actualizarán/insertarán según corresponda.", logs)
            
            # 3. Obtener mapeo de carreras para unificar referencias
            mapeo_carreras = data.get('_mapeo_carreras', {})
            
            # 4. Procesar y insertar datos
            log_progress("💾 Procesando e insertando datos en la base de datos...", logs)
            estadisticas = {
                'carreras_insertadas': 0,
                'grupos_insertados': 0,
                'aulas_insertadas': 0,
                'profesores_insertados': 0,
                'materias_insertadas': 0,
                'periodos_insertados': 0,
                'horarios_insertados': 0,
                'carreras_actualizadas': 0,
                'grupos_actualizados': 0,
                'aulas_actualizadas': 0,
                'profesores_actualizados': 0,
                'materias_actualizadas': 0,
                'periodos_actualizados': 0,
                'horarios_actualizados': 0,
                'errores': [],
                'bd_vacia': bd_vacia
            }
            
            # Procesar periodos
            log_progress("  📅 Procesando periodos...", logs)
            if 'periodo' in data or 'periodos' in data:
                periodo_data = data.get('periodo') or (data.get('periodos', [])[0] if data.get('periodos') else None)
                if periodo_data:
                    id_periodo = periodo_data.get('id_periodo') or periodo
                    nombre_periodo = periodo_data.get('nombre_periodo') or periodo
                    
                    periodo_existente = db.query(PeriodoAcademico).filter(
                        PeriodoAcademico.id_periodo == id_periodo
                    ).first()
                    
                    if not periodo_existente:
                        nuevo_periodo = PeriodoAcademico(
                            id_periodo=id_periodo,
                            nombre_periodo=nombre_periodo
                        )
                        db.add(nuevo_periodo)
                        estadisticas['periodos_insertados'] += 1
                    else:
                        # Actualizar si existe
                        periodo_existente.nombre_periodo = nombre_periodo
                        estadisticas['periodos_actualizados'] += 1
            log_progress(f"    ✅ Periodos: {estadisticas['periodos_insertados']} insertados, {estadisticas['periodos_actualizados']} actualizados", logs)
            
            # Procesar carreras
            log_progress("  🎓 Procesando carreras...", logs)
            if 'carreras' in data:
                for carrera_data in data['carreras']:
                    try:
                        # Mapear campos: la API usa 'clave' como ID y 'nombre' como nombre
                        id_carrera = carrera_data.get('id_carrera') or carrera_data.get('clave')
                        nombre_carrera = carrera_data.get('nombre_carrera') or carrera_data.get('nombre')
                        
                        if not id_carrera or not nombre_carrera:
                            continue
                        
                        # Convertir id_carrera a string si es necesario
                        if isinstance(id_carrera, (int, float)):
                            id_carrera = str(id_carrera)
                        
                        carrera_existente = db.query(Carrera).filter(
                            Carrera.id_carrera == id_carrera
                        ).first()
                        
                        if not carrera_existente:
                            nueva_carrera = Carrera(
                                id_carrera=id_carrera,
                                nombre_carrera=nombre_carrera
                            )
                            db.add(nueva_carrera)
                            estadisticas['carreras_insertadas'] += 1
                        else:
                            # Actualizar si existe
                            carrera_existente.nombre_carrera = nombre_carrera
                            estadisticas['carreras_actualizadas'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando carrera: {str(e)}")
            log_progress(f"    ✅ Carreras: {estadisticas['carreras_insertadas']} insertadas, {estadisticas['carreras_actualizadas']} actualizadas", logs)
            
            # Procesar grupos
            log_progress("  👥 Procesando grupos...", logs)
            if 'grupos' in data:
                # Filtrar grupos no deseados (que empiezan con P/p/V/v)
                grupos_filtrados, grupos_excluidos = filtrar_grupos_no_deseados(data['grupos'])
                if grupos_excluidos > 0:
                    log_progress(f"    🚫 {grupos_excluidos} grupos excluidos (empiezan con P/V)", logs)
                data['grupos'] = grupos_filtrados
                log_progress(f"    📊 Grupos después de filtrar: {len(data['grupos'])} grupos válidos", logs)
                # Obtener mapeo de carreras (si existe) para unificar referencias
                mapeo_carreras = data.get('_mapeo_carreras', {})
                
                # Primero, extraer todas las carreras referenciadas por los grupos y aplicar mapeo
                carreras_referenciadas = set()
                grupos_actualizados_carrera = 0
                
                for grupo_data in data['grupos']:
                    id_carrera = grupo_data.get('id_carrera') or grupo_data.get('carrera') or grupo_data.get('claveCarrera')
                    if id_carrera:
                        if isinstance(id_carrera, (int, float)):
                            id_carrera = str(int(id_carrera))
                        
                        # Aplicar mapeo de carreras unificadas (ej: 06B -> 06)
                        if mapeo_carreras and id_carrera in mapeo_carreras:
                            id_carrera_unificada = mapeo_carreras[id_carrera]
                            if id_carrera_unificada != id_carrera:
                                grupo_data['id_carrera'] = id_carrera_unificada
                                grupo_data['carrera'] = id_carrera_unificada
                                grupos_actualizados_carrera += 1
                                id_carrera = id_carrera_unificada
                        
                        carreras_referenciadas.add(id_carrera)
                
                if grupos_actualizados_carrera > 0:
                    log_progress(f"    🔗 {grupos_actualizados_carrera} grupos actualizados con carrera unificada", logs)
                
                # Asegurar que todas las carreras referenciadas existan en la BD
                carreras_existentes_ids = {c.get('id_carrera') or c.get('clave') for c in data['carreras'] if c.get('id_carrera') or c.get('clave')}
                carreras_faltantes = carreras_referenciadas - carreras_existentes_ids
                
                if carreras_faltantes:
                    log_progress(f"    ⚠️ {len(carreras_faltantes)} carreras referenciadas por grupos no están en la lista filtrada. Verificando en BD...", logs)
                    for id_carrera_faltante in carreras_faltantes:
                        # Verificar si ya existe en la BD
                        carrera_bd = db.query(Carrera).filter(Carrera.id_carrera == id_carrera_faltante).first()
                        if not carrera_bd:
                            # Crear carrera con nombre genérico
                            nueva_carrera = Carrera(
                                id_carrera=id_carrera_faltante,
                                nombre_carrera=f'Carrera {id_carrera_faltante}'
                            )
                            db.add(nueva_carrera)
                            estadisticas['carreras_insertadas'] += 1
                            log_progress(f"      ✅ Carrera creada: {id_carrera_faltante}", logs)
                    # Hacer commit de las carreras creadas antes de procesar grupos
                    if estadisticas['carreras_insertadas'] > 0:
                        db.commit()
                        log_progress(f"    ✅ {estadisticas['carreras_insertadas']} carreras faltantes creadas y guardadas", logs)
                
                for grupo_data in data['grupos']:
                    try:
                        # Mapear campos: la API puede usar diferentes nombres
                        id_grupo = grupo_data.get('id_grupo') or grupo_data.get('grupo') or grupo_data.get('clave') or grupo_data.get('idGrupo')
                        nombre_grupo = grupo_data.get('nombre_grupo') or grupo_data.get('nombre') or grupo_data.get('nombreGrupo')
                        id_carrera = grupo_data.get('id_carrera') or grupo_data.get('carrera') or grupo_data.get('claveCarrera')
                        numero_alumnos = grupo_data.get('numero_alumnos') or grupo_data.get('numeroAlumnos') or grupo_data.get('alumnos', 0)
                        
                        if not id_grupo:
                            continue
                        
                        # Convertir a string si es necesario
                        if isinstance(id_grupo, (int, float)):
                            id_grupo = str(int(id_grupo))
                        if id_carrera and isinstance(id_carrera, (int, float)):
                            id_carrera = str(id_carrera)
                        
                        # Verificar que la carrera exista antes de insertar el grupo
                        if id_carrera:
                            carrera_existente = db.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
                            if not carrera_existente:
                                # Crear carrera si no existe (fallback adicional)
                                nueva_carrera = Carrera(
                                    id_carrera=id_carrera,
                                    nombre_carrera=f'Carrera {id_carrera}'
                                )
                                db.add(nueva_carrera)
                                estadisticas['carreras_insertadas'] += 1
                        
                        grupo_existente = db.query(GrupoEscolar).filter(
                            GrupoEscolar.id_grupo == id_grupo
                        ).first()
                        
                        if not grupo_existente:
                            nuevo_grupo = GrupoEscolar(
                                id_grupo=id_grupo,
                                nombre_grupo=nombre_grupo or id_grupo,
                                id_carrera=id_carrera,
                                numero_alumnos=numero_alumnos
                            )
                            db.add(nuevo_grupo)
                            estadisticas['grupos_insertados'] += 1
                        else:
                            # Actualizar si existe
                            grupo_existente.nombre_grupo = nombre_grupo or id_grupo
                            grupo_existente.id_carrera = id_carrera
                            grupo_existente.numero_alumnos = numero_alumnos
                            estadisticas['grupos_actualizados'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando grupo: {str(e)}")
            log_progress(f"    ✅ Grupos: {estadisticas['grupos_insertados']} insertados, {estadisticas['grupos_actualizados']} actualizados", logs)
            
            # Procesar aulas
            log_progress("  📚 Procesando aulas...", logs)
            if 'aulas' in data:
                for aula_data in data['aulas']:
                    try:
                        # Mapear campos: la API usa 'clave' como ID y 'nombre' como nombre
                        id_aula = aula_data.get('id_aula') or aula_data.get('clave')
                        nombre_aula = aula_data.get('nombre_aula') or aula_data.get('nombre')
                        capacidad = aula_data.get('capacidad', 0)
                        
                        if not id_aula or not nombre_aula:
                            continue
                        
                        # Convertir id_aula a string si es numérico
                        if isinstance(id_aula, (int, float)):
                            id_aula = str(int(id_aula))
                        
                        aula_existente = db.query(Aula).filter(
                            Aula.id_aula == id_aula
                        ).first()
                        
                        if not aula_existente:
                            nueva_aula = Aula(
                                id_aula=id_aula,
                                nombre_aula=nombre_aula,
                                capacidad=capacidad,
                                is_disable=False
                            )
                            db.add(nueva_aula)
                            estadisticas['aulas_insertadas'] += 1
                        else:
                            # Actualizar si existe
                            aula_existente.nombre_aula = nombre_aula
                            aula_existente.capacidad = capacidad
                            estadisticas['aulas_actualizadas'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando aula: {str(e)}")
            
            # Procesar profesores
            log_progress("  👨‍🏫 Procesando profesores...", logs)
            if 'profesores' in data:
                # Filtrar profesores no deseados (técnicos, profesores genéricos, etc.)
                profesores_filtrados, profesores_excluidos = filtrar_profesores_no_deseados(data['profesores'])
                if profesores_excluidos > 0:
                    log_progress(f"    🚫 {profesores_excluidos} profesores excluidos (técnicos/genéricos)", logs)
                data['profesores'] = profesores_filtrados
                log_progress(f"    📊 Profesores después de filtrar: {len(data['profesores'])} profesores válidos", logs)
            
            if 'profesores' not in data:
                log_progress("  👨‍🏫 No hay profesores en datos separados, se extraerán de horarios", logs)
                for profesor_data in data['profesores']:
                    try:
                        # Mapear campos: la API puede usar diferentes nombres
                        id_profesor = profesor_data.get('id_profesor') or profesor_data.get('idprofesor') or profesor_data.get('clave')
                        nombre_profesor = profesor_data.get('nombre_profesor') or profesor_data.get('nombre') or profesor_data.get('nombreCompleto')
                        
                        if not id_profesor or not nombre_profesor:
                            continue
                        
                        # Convertir a string si es numérico
                        if isinstance(id_profesor, (int, float)):
                            id_profesor = str(int(id_profesor))
                        
                        profesor_existente = db.query(Profesor).filter(
                            Profesor.id_profesor == id_profesor
                        ).first()
                        
                        if not profesor_existente:
                            nuevo_profesor = Profesor(
                                id_profesor=id_profesor,
                                nombre_profesor=nombre_profesor,
                                is_disable=False
                            )
                            db.add(nuevo_profesor)
                            estadisticas['profesores_insertados'] += 1
                        else:
                            # Actualizar si existe
                            profesor_existente.nombre_profesor = nombre_profesor
                            profesor_existente.is_disable = False
                            estadisticas['profesores_actualizados'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando profesor: {str(e)}")
            log_progress(f"    ✅ Profesores: {estadisticas['profesores_insertados']} insertados, {estadisticas['profesores_actualizados']} actualizados", logs)
            
            # Procesar materias
            log_progress("  📖 Procesando materias...", logs)
            if 'materias' in data:
                for materia_data in data['materias']:
                    try:
                        # Mapear campos: la API puede usar diferentes nombres
                        id_materia = materia_data.get('id_materia') or materia_data.get('asignatura') or materia_data.get('clave')
                        nombre_materia = materia_data.get('nombre_materia') or materia_data.get('nombre') or materia_data.get('materia')
                        
                        if not id_materia or not nombre_materia:
                            continue
                        
                        # Truncar nombre si es muy largo (máximo 50 caracteres)
                        if len(nombre_materia.encode('utf-8')) > 50:
                            nombre_materia = nombre_materia[:47] + "..."
                        
                        materia_existente = db.query(Materia).filter(
                            Materia.id_materia == id_materia
                        ).first()
                        
                        if not materia_existente:
                            nueva_materia = Materia(
                                id_materia=id_materia,
                                nombre_materia=nombre_materia
                            )
                            db.add(nueva_materia)
                            estadisticas['materias_insertadas'] += 1
                        else:
                            # Actualizar si existe
                            materia_existente.nombre_materia = nombre_materia
                            estadisticas['materias_actualizadas'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando materia: {str(e)}")
            
            # Procesar horarios
            horarios_excluidos_grupo = 0
            horarios_excluidos_profesor = 0
            
            if 'horarios' in data:
                id_periodo_actual = data.get('periodo', {}).get('id_periodo') or data.get('periodo', {}).get('periodog') or periodo
                
                for horario_data in data['horarios']:
                    try:
                        # Mapear campos de la API real: rowId, idprofesor, idGrupo, idAula, dia, hora, carrera, periodog, materia
                        id_horario_clase = horario_data.get('id_horario_clase') or horario_data.get('id_horario') or f"HOR{horario_data.get('rowId', '')}"
                        id_materia = horario_data.get('id_materia') or horario_data.get('asignatura')
                        id_grupo_horario = horario_data.get('id_grupo') or horario_data.get('idGrupo') or grupo
                        id_profesor_horario = horario_data.get('id_profesor') or horario_data.get('idprofesor')
                        id_aula_horario = horario_data.get('id_aula') or horario_data.get('idAula')
                        dia_semana = horario_data.get('dia_semana') or horario_data.get('dia', 0)
                        nombre_profesor = horario_data.get('nombreCompleto') or horario_data.get('nombre_profesor') or horario_data.get('profesor')
                        
                        # FILTRAR PRIMERO: Grupos y profesores no deseados (antes de procesar cualquier cosa)
                        if id_grupo_horario and es_grupo_no_deseado(str(id_grupo_horario)):
                            horarios_excluidos_grupo += 1
                            continue  # Saltar este horario completo
                        
                        if nombre_profesor and es_profesor_no_deseado(str(nombre_profesor)):
                            horarios_excluidos_profesor += 1
                            continue  # Saltar este horario completo
                        
                        # Extraer carrera del horario si no está en datos separados
                        carrera_horario = horario_data.get('carrera')
                        
                        # Aplicar mapeo de carreras unificadas (si existe)
                        mapeo_carreras_horarios = data.get('_mapeo_carreras', {})
                        if carrera_horario and mapeo_carreras_horarios and carrera_horario in mapeo_carreras_horarios:
                            carrera_horario = mapeo_carreras_horarios[carrera_horario]
                        
                        if carrera_horario and 'carreras' not in data:
                            # Agregar carrera si no existe en la lista
                            carrera_existente = db.query(Carrera).filter(Carrera.id_carrera == carrera_horario).first()
                            if not carrera_existente:
                                nueva_carrera = Carrera(
                                    id_carrera=carrera_horario,
                                    nombre_carrera=horario_data.get('nombreCarrera', f'Carrera {carrera_horario}')
                                )
                                db.add(nueva_carrera)
                                estadisticas['carreras_insertadas'] += 1
                        
                        # Extraer materia del horario si no está en datos separados
                        nombre_materia = horario_data.get('materia')
                        if nombre_materia and id_materia and 'materias' not in data:
                            materia_existente = db.query(Materia).filter(Materia.id_materia == id_materia).first()
                            if not materia_existente:
                                # Truncar nombre si es muy largo
                                nombre_materia_truncado = nombre_materia
                                if len(nombre_materia.encode('utf-8')) > 50:
                                    nombre_materia_truncado = nombre_materia[:47] + "..."
                                nueva_materia = Materia(
                                    id_materia=id_materia,
                                    nombre_materia=nombre_materia_truncado
                                )
                                db.add(nueva_materia)
                                estadisticas['materias_insertadas'] += 1
                        
                        # Extraer profesor del horario si no está en datos separados
                        # (nombre_profesor ya se obtuvo arriba para el filtrado)
                        if nombre_profesor and id_profesor_horario and 'profesores' not in data:
                            profesor_existente = db.query(Profesor).filter(Profesor.id_profesor == str(id_profesor_horario)).first()
                            if not profesor_existente:
                                nuevo_profesor = Profesor(
                                    id_profesor=str(id_profesor_horario),
                                    nombre_profesor=nombre_profesor,
                                    is_disable=False
                                )
                                db.add(nuevo_profesor)
                                estadisticas['profesores_insertados'] += 1
                        
                        # Extraer aula del horario si no está en datos separados
                        nombre_aula = horario_data.get('nombreAula')
                        if nombre_aula and id_aula_horario and 'aulas' not in data:
                            aula_existente = db.query(Aula).filter(Aula.id_aula == str(id_aula_horario)).first()
                            if not aula_existente:
                                nueva_aula = Aula(
                                    id_aula=str(id_aula_horario),
                                    nombre_aula=nombre_aula,
                                    capacidad=0,  # No disponible en horarios
                                    is_disable=False
                                )
                                db.add(nueva_aula)
                                estadisticas['aulas_insertadas'] += 1
                        
                        # Extraer grupo del horario si no está en datos separados
                        nombre_grupo = horario_data.get('nombreGrupo')
                        if nombre_grupo and id_grupo_horario and carrera_horario and 'grupos' not in data:
                            # (Ya se filtró arriba, no es necesario filtrar de nuevo)
                            grupo_existente = db.query(GrupoEscolar).filter(GrupoEscolar.id_grupo == str(id_grupo_horario)).first()
                            if not grupo_existente:
                                nuevo_grupo = GrupoEscolar(
                                    id_grupo=str(id_grupo_horario),
                                    nombre_grupo=nombre_grupo,
                                    id_carrera=carrera_horario,
                                    numero_alumnos=0
                                )
                                db.add(nuevo_grupo)
                                estadisticas['grupos_insertados'] += 1
                        
                        # Procesar hora_inicio y hora_fin
                        # La API usa 'hora' como número (ej: 17 = 17:00)
                        hora_num = horario_data.get('hora')
                        hora_inicio_str = horario_data.get('hora_inicio')
                        hora_fin_str = horario_data.get('hora_fin')
                        
                        # Si viene como número, convertir a formato HH:MM
                        if hora_num is not None and not hora_inicio_str:
                            hora_inicio_str = f"{int(hora_num):02d}:00"
                            # Asumir 1 hora de duración por defecto
                            hora_fin_str = f"{int(hora_num) + 1:02d}:00"
                        
                        from datetime import time as dt_time
                        hora_inicio = None
                        hora_fin = None
                        
                        if hora_inicio_str:
                            if isinstance(hora_inicio_str, str):
                                try:
                                    h, m = hora_inicio_str.split(':')
                                    hora_inicio = dt_time(int(h), int(m))
                                except:
                                    pass
                        
                        if hora_fin_str:
                            if isinstance(hora_fin_str, str):
                                try:
                                    h, m = hora_fin_str.split(':')
                                    hora_fin = dt_time(int(h), int(m))
                                except:
                                    pass
                        
                        if not id_horario_clase or not id_materia or not id_grupo_horario:
                            continue
                        
                        # Convertir IDs a string
                        if isinstance(id_horario_clase, (int, float)):
                            id_horario_clase = f"HOR{int(id_horario_clase)}"
                        if isinstance(id_grupo_horario, (int, float)):
                            id_grupo_horario = str(int(id_grupo_horario))
                        if id_profesor_horario and isinstance(id_profesor_horario, (int, float)):
                            id_profesor_horario = str(int(id_profesor_horario))
                        if id_aula_horario and isinstance(id_aula_horario, (int, float)):
                            id_aula_horario = str(int(id_aula_horario))
                        
                        # Asegurar que el profesor exista antes de crear el horario
                        if id_profesor_horario:
                            profesor_existente_horario = db.query(Profesor).filter(
                                Profesor.id_profesor == str(id_profesor_horario)
                            ).first()
                            
                            if not profesor_existente_horario:
                                # Crear profesor si no existe (solo si tiene nombre)
                                if nombre_profesor:
                                    nuevo_profesor_horario = Profesor(
                                        id_profesor=str(id_profesor_horario),
                                        nombre_profesor=nombre_profesor,
                                        is_disable=False
                                    )
                                    db.add(nuevo_profesor_horario)
                                    estadisticas['profesores_insertados'] += 1
                                    db.flush()  # Hacer flush para que esté disponible para el horario
                                else:
                                    # Si no hay nombre de profesor, saltar este horario
                                    continue
                        
                        horario_existente = db.query(HorarioClase).filter(
                            HorarioClase.id_horario_clase == id_horario_clase
                        ).first()
                        
                        if not horario_existente:
                            nuevo_horario = HorarioClase(
                                id_horario_clase=id_horario_clase,
                                id_periodo=id_periodo_actual,
                                id_materia=id_materia,
                                id_grupo=id_grupo_horario,
                                id_profesor=id_profesor_horario,
                                id_aula=id_aula_horario,
                                dia_semana=dia_semana,
                                hora_inicio=hora_inicio,
                                hora_fin=hora_fin
                            )
                            db.add(nuevo_horario)
                            estadisticas['horarios_insertados'] += 1
                        else:
                            # Actualizar si existe
                            horario_existente.id_periodo = id_periodo_actual
                            horario_existente.id_materia = id_materia
                            horario_existente.id_grupo = id_grupo_horario
                            horario_existente.id_profesor = id_profesor_horario
                            horario_existente.id_aula = id_aula_horario
                            horario_existente.dia_semana = dia_semana
                            horario_existente.hora_inicio = hora_inicio
                            horario_existente.hora_fin = hora_fin
                            estadisticas['horarios_actualizados'] += 1
                    except Exception as e:
                        estadisticas['errores'].append(f"Error procesando horario: {str(e)}")
            if horarios_excluidos_grupo > 0 or horarios_excluidos_profesor > 0:
                log_progress(f"    🚫 Horarios excluidos: {horarios_excluidos_grupo} por grupo (P/V), {horarios_excluidos_profesor} por profesor (técnico/genérico)", logs)
            log_progress(f"    ✅ Horarios: {estadisticas['horarios_insertados']} insertados, {estadisticas['horarios_actualizados']} actualizados", logs)
            
            # Commit de todos los cambios
            log_progress("💾 Guardando cambios en la base de datos...", logs)
            db.commit()
            log_progress("✅ Cambios guardados exitosamente", logs)
            
            total_operaciones = sum([
                estadisticas['carreras_insertadas'],
                estadisticas['grupos_insertados'],
                estadisticas['aulas_insertadas'],
                estadisticas['profesores_insertados'],
                estadisticas['materias_insertadas'],
                estadisticas['periodos_insertados'],
                estadisticas['horarios_insertados'],
                estadisticas['carreras_actualizadas'],
                estadisticas['grupos_actualizados'],
                estadisticas['aulas_actualizadas'],
                estadisticas['profesores_actualizados'],
                estadisticas['materias_actualizadas'],
                estadisticas['periodos_actualizados'],
                estadisticas['horarios_actualizados']
            ])
            
            mensaje = 'Sincronización completada exitosamente'
            if bd_vacia:
                mensaje = 'Base de datos llenada exitosamente (estaba vacía)'
            
            return {
                'mensaje': mensaje,
                'periodo': periodo,
                'grupo': grupo if grupo else 'TODOS',
                'grupos_sincronizados': grupos_exitosos,
                'grupos_fallidos': len(grupos_fallidos),
                'grupos_fallidos_detalle': grupos_fallidos[:10],  # Solo primeros 10 para no saturar
                'fecha_sincronizacion': datetime.now().isoformat(),
                'estadisticas': estadisticas,
                'total_insertado': sum([
                    estadisticas['carreras_insertadas'],
                    estadisticas['grupos_insertados'],
                    estadisticas['aulas_insertadas'],
                    estadisticas['profesores_insertados'],
                    estadisticas['materias_insertadas'],
                    estadisticas['periodos_insertados'],
                    estadisticas['horarios_insertados']
                ]),
                'total_actualizado': sum([
                    estadisticas['carreras_actualizadas'],
                    estadisticas['grupos_actualizados'],
                    estadisticas['aulas_actualizadas'],
                    estadisticas['profesores_actualizados'],
                    estadisticas['materias_actualizadas'],
                    estadisticas['periodos_actualizados'],
                    estadisticas['horarios_actualizados']
                ]),
                'total_operaciones': total_operaciones,
                'bd_estaba_vacia': bd_vacia,
                'logs': logs
            }
        
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error al consultar la API externa: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        print(f"[Sincronización] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante la sincronización: {str(e)}"
        )

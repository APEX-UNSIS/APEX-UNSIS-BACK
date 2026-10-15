# APIs Necesarias para Sincronización de Base de Datos

Este documento lista todas las APIs que deben estar disponibles en `http://serv-horarios.unsis.lan/api/` para poder llenar la base de datos correctamente.

## ✅ APIs Confirmadas que Funcionan

- ✅ `GET http://serv-horarios.unsis.lan/api/horarios/{periodo}/grupo/{grupo}`
- ✅ `GET http://serv-horarios.unsis.lan/api/grupos`
- ✅ `GET http://serv-horarios.unsis.lan/api/aulas`
- ✅ `GET http://serv-horarios.unsis.lan/api/carreras`

## 📋 Lista de APIs Requeridas

### 1. **API de Horarios** (OBLIGATORIA) ✅
```
GET http://serv-horarios.unsis.lan/api/horarios/{periodo}/grupo/{grupo}
```
**Ejemplo:**
```
GET http://serv-horarios.unsis.lan/api/horarios/2526A/grupo/706
```

**Respuesta:** Array de objetos horario

**Estructura real de cada horario:**
```json
{
  "rowId": 50195,
  "idprofesor": "1476",
  "nombreCompleto": "DR. GERARDO ROBERTO ARAGÓN GONZÁLEZ",
  "asignatura": "P6075_2022",
  "idGrupo": "706",
  "idAula": "73",
  "dia": 1,
  "hora": 17,
  "carrera": "03C",
  "periodog": "2526A",
  "materia": "DERECHO Y LEGISLACIÓN EN INFORMÁTICA",
  "nombreGrupo": "706",
  "nombreAula": "CETI - REDES"
}
```

**Mapeo de campos:**
- `rowId` → se usa para generar `id_horario_clase` (ej: "HOR50195")
- `idprofesor` → `id_profesor`
- `nombreCompleto` → nombre del profesor
- `asignatura` → `id_materia`
- `materia` → nombre de la materia
- `idGrupo` → `id_grupo`
- `nombreGrupo` → nombre del grupo
- `idAula` → `id_aula`
- `nombreAula` → nombre del aula
- `carrera` → `id_carrera`
- `periodog` → `id_periodo`
- `dia` → `dia_semana`
- `hora` → se convierte a `hora_inicio` (ej: 17 → "17:00")

---

### 2. **API de Aulas** (RECOMENDADA) ✅
```
GET http://serv-horarios.unsis.lan/api/aulas
```

**Ejemplo:**
```
GET http://serv-horarios.unsis.lan/api/aulas
```

**Respuesta:** Array de objetos aula

**Estructura real de cada aula:**
```json
{
  "clave": "1",
  "nombre": "A1",
  "capacidad": 18,
  "tipo": "AULA",
  "statusProyector": "NO_FUNCIONA"
}
```

**Mapeo de campos:**
- `clave` → `id_aula`
- `nombre` → `nombre_aula`
- `capacidad` → `capacidad`

---

### 3. **API de Carreras** (RECOMENDADA) ✅
```
GET http://serv-horarios.unsis.lan/api/carreras
```

**Ejemplo:**
```
GET http://serv-horarios.unsis.lan/api/carreras
```

**Respuesta:** Array de objetos carrera

**Estructura real de cada carrera:**
```json
{
  "clave": "01B",
  "nombre": "LICENCIATURA EN ADMINISTRACIÓN MUNICIPAL 2015",
  "vigente": true
}
```

**Mapeo de campos:**
- `clave` → `id_carrera`
- `nombre` → `nombre_carrera`
- `vigente` → se ignora (solo se usa para referencia)

---

### 4. **API de Profesores** (RECOMENDADA)
```
GET http://serv-horarios/api/profesores
```

**Ejemplo:**
```
GET http://serv-horarios/api/profesores
```

**Respuesta esperada:**
- Array de objetos profesor
- O objeto con propiedad `profesores` que contiene el array

**Estructura esperada de cada profesor:**
```json
{
  "id_profesor": "PROF001",
  "nombre_profesor": "Dr. Juan Pérez López"
}
```

---

### 5. **API de Materias** (RECOMENDADA)
```
GET http://serv-horarios/api/materias
```

**Ejemplo:**
```
GET http://serv-horarios/api/materias
```

**Respuesta esperada:**
- Array de objetos materia
- O objeto con propiedad `materias` que contiene el array

**Estructura esperada de cada materia:**
```json
{
  "id_materia": "MAT001",
  "nombre_materia": "Programación I"
}
```

**⚠️ IMPORTANTE:** El nombre de la materia no debe exceder 50 bytes cuando se codifica en UTF-8 (caracteres con acentos ocupan más bytes).

---

### 6. **API de Grupos** (RECOMENDADA) ✅
```
GET http://serv-horarios.unsis.lan/api/grupos
```

**Ejemplo:**
```
GET http://serv-horarios.unsis.lan/api/grupos
```

**Respuesta:** Array de objetos grupo (estructura a confirmar)

**Estructura esperada de cada grupo:**
```json
{
  "id_grupo": "706",
  "nombre_grupo": "706",
  "id_carrera": "CARR001",
  "numero_alumnos": 25
}
```

**Nota:** Si la estructura es diferente, el código intentará mapear campos comunes como `clave`, `nombre`, `carrera`, etc.

---

### 7. **API de Periodos** (OPCIONAL)
```
GET http://serv-horarios/api/periodos
```

**Ejemplo:**
```
GET http://serv-horarios/api/periodos
```

**Respuesta esperada:**
- Array de objetos periodo
- O objeto con propiedad `periodos` que contiene el array

**Estructura esperada de cada periodo:**
```json
{
  "id_periodo": "2526A",
  "nombre_periodo": "2025-2026 Semestre A"
}
```

**Nota:** Si esta API no está disponible, se usará el periodo proporcionado en el parámetro.

---

## 🔄 Comportamiento del Sistema

### Si todas las APIs están disponibles:
- Se obtendrán todos los datos de las APIs individuales
- Se procesarán y sincronizarán en la base de datos

### Si alguna API falla:
- El sistema continuará con las APIs disponibles
- Se mostrará un mensaje de advertencia en los logs
- Se intentará extraer datos relacionados de la API de horarios

### Si solo la API de horarios está disponible:
- El sistema intentará extraer información relacionada (aulas, profesores, materias, grupos, carreras) de los horarios
- Esto requiere que los horarios incluyan toda la información necesaria

---

## ✅ Checklist de Verificación

Usa este checklist para verificar que todas las APIs funcionan:

- [x] `GET http://serv-horarios.unsis.lan/api/horarios/2526A/grupo/706` - **OBLIGATORIA** ✅
- [x] `GET http://serv-horarios.unsis.lan/api/aulas` ✅
- [x] `GET http://serv-horarios.unsis.lan/api/carreras` ✅
- [x] `GET http://serv-horarios.unsis.lan/api/grupos` ✅
- [ ] `GET http://serv-horarios.unsis.lan/api/profesores` (opcional - se extraen de horarios)
- [ ] `GET http://serv-horarios.unsis.lan/api/materias` (opcional - se extraen de horarios)
- [ ] `GET http://serv-horarios.unsis.lan/api/periodos` (opcional - se usa el periodo proporcionado)

---

## 📝 Notas Importantes

1. **Formato de respuesta:** Las APIs pueden devolver:
   - Un array directamente: `[{...}, {...}]`
   - Un objeto con una propiedad: `{"aulas": [{...}, {...}]}`

2. **Códigos de estado HTTP:**
   - `200 OK`: API funciona correctamente
   - `404 Not Found`: Endpoint no existe
   - `500 Internal Server Error`: Error en el servidor

3. **Timeout:** El sistema espera máximo 30 segundos por cada API

4. **Datos mínimos:** Al menos la API de horarios debe estar disponible para que el sistema funcione

---

## 🧪 Ejemplo de Prueba en Navegador

Abre cada URL en tu navegador y verifica que:
1. La respuesta es JSON válido
2. La estructura coincide con lo esperado
3. Los datos están completos

**URLs confirmadas que funcionan:**
```
✅ http://serv-horarios.unsis.lan/api/horarios/2526A/grupo/706
✅ http://serv-horarios.unsis.lan/api/aulas
✅ http://serv-horarios.unsis.lan/api/carreras
✅ http://serv-horarios.unsis.lan/api/grupos
```

**URLs opcionales (si no están disponibles, se extraerán datos de horarios):**
```
http://serv-horarios.unsis.lan/api/profesores
http://serv-horarios.unsis.lan/api/materias
http://serv-horarios.unsis.lan/api/periodos
```

## 📌 Notas Importantes sobre el Mapeo

El código ahora está configurado para:
1. **Mapear campos reales** de las APIs (ej: `clave` → `id_aula`, `idprofesor` → `id_profesor`)
2. **Extraer datos de horarios** si las APIs individuales no están disponibles
3. **Convertir tipos** automáticamente (números a strings cuando sea necesario)
4. **Manejar diferentes formatos** de respuesta (arrays directos o objetos con propiedades)

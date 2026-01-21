-- =====================================================
-- Script para insertar datos de TERCERA EVALUACIÓN PARCIAL
-- Periodo: 19 al 26 de enero de 2026
-- Evaluación: EVAL003 (Parcial 3)
-- =====================================================
-- Datos extraídos del PDF: TERCERA EVALUACIÓN PARCIAL DEL 19 AL 26 DE ENERO DE 2026
-- =====================================================

-- =====================================================
-- 1. CARRERAS
-- =====================================================
INSERT INTO carreras (id_carrera, nombre_carrera) VALUES
('LIC-CE', 'Licenciatura en Ciencias Empresariales'),
('LIC-CB', 'Licenciatura en Ciencias Biomédicas'),
('LIC-SC', 'Licenciatura en Sistemas Computacionales'),
('LIC-AP', 'Licenciatura en Administración Pública'),
('LIC-AM', 'Licenciatura en Administración Municipal'),
('LIC-NUT', 'Licenciatura en Nutrición'),
('LIC-ODO', 'Licenciatura en Odontología'),
('LIC-ENF', 'Licenciatura en Enfermería'),
('LIC-MED', 'Licenciatura en Medicina')
ON CONFLICT (id_carrera) DO NOTHING;

-- =====================================================
-- 2. USUARIOS
-- =====================================================
-- NOTA: Este script NO inserta usuarios. Solo debe existir el usuario 'admin'
-- que se crea automáticamente en crear_tablas.sql
-- Si necesitas crear usuarios adicionales, hazlo manualmente o con otro script

-- =====================================================
-- 3. PROFESORES
-- =====================================================
INSERT INTO profesores (id_profesor, nombre_profesor, is_disable) VALUES
-- Ciencias Empresariales
('PROF001', 'Mtra. Monica Lerícia Mejía Ramírez', FALSE),
('PROF002', 'Mtra. Mariano Olvera Ramírez', FALSE),
('PROF003', 'Mtra. Silviana Juarez Chalini', FALSE),
('PROF004', 'Mtra. Araceli Luz Alva Rodríguez Martínez', FALSE),
('PROF005', 'Mtra. Jorge Lamas Carlos', FALSE),
('PROF006', 'Dr. Arturo Benítez Hernández', FALSE),
('PROF007', 'Dr. Amando Alejandro Ruiz Figueroa', FALSE),
('PROF008', 'Mtra. Rafael Renteria Gaeta', FALSE),
('PROF009', 'Mtra. Enrique García Reyes', FALSE),
('PROF010', 'Mtra. Fabiola Crespo Barrios', FALSE),
('PROF011', 'Mtra. Hadya Concepción Díaz Ortiz', FALSE),
('PROF012', 'Mtra. Maximo Jorge Saavedra García', FALSE),
('PROF013', 'Dr. Pedro Durán Féman', FALSE),
('PROF014', 'Dr. Oscar David Valencia López', FALSE),
('PROF015', 'Mtro. Marco Antonio Santos Martínez', FALSE),
-- Ciencias Biomédicas
('PROF016', 'Mtra. Victoria Vera Pineda', FALSE),
('PROF017', 'Dr. Roberto García Zúñiga', FALSE),
('PROF018', 'Mtro. Irving Ulises Hernández Miguel', FALSE),
('PROF019', 'Mtra. Iliana Vasquez Lara', FALSE),
('PROF020', 'Dr. Edgar Rodrigo Guzmán Bautista', FALSE),
('PROF021', 'M.C. Andrea Itayetzzi Ortiz García', FALSE),
('PROF022', 'Mtro. Raúl Misael Cortés Olivera', FALSE),
('PROF023', 'Dra. Claudia Chávez López', FALSE),
('PROF024', 'M.C.I.B. Ericy Berenice Martínez Ramos', FALSE),
('PROF025', 'E.A.P. Jorge Carlos Moguel Gamboa', FALSE),
('PROF026', 'L.E. Said Daniel Carseco González', FALSE),
-- Sistemas Computacionales
('PROF027', 'M.T.E. Everardo de Jesús Pacheco Antonio', FALSE),
('PROF028', 'M.I.S. Fabiola Crespo Barrios', FALSE),
('PROF029', 'M.I.T.I. Oswaldo Rey Ávila Barrón', FALSE),
('PROF030', 'M.C.M. Jesús Pacheco Mendoza', FALSE),
('PROF031', 'M.C. Enrique García Reyes', FALSE),
('PROF032', 'M.C.C. Eliezer Alcazar Silva', FALSE),
('PROF033', 'M.C. Mónica Pérez Meza', FALSE),
('PROF034', 'Dr. Ariasí Dario Barragán López', FALSE),
('PROF035', 'M.C.C. Silviana Juárez Chalini', FALSE),
('PROF036', 'Dr. Eric Melecio Castro Leal', FALSE),
('PROF037', 'Dr. Alejandro Jarillo Silva', FALSE),
('PROF038', 'M.J.O.S.A. Gerardo Roberto Aragón González', FALSE),
-- Administración Pública
('PROF039', 'Dra. Nina Martínez Cruz', FALSE),
('PROF040', 'Dra. Alicia Martínez Cruz', FALSE),
('PROF041', 'Mtro. Joann E. Olivier Picard', FALSE),
('PROF042', 'Mtro. Rocío G. Bravo Salazar', FALSE),
('PROF043', 'Mtro. Daniel Robles Torres', FALSE),
('PROF044', 'Mtro. Juan Carlos Mata Espinoza', FALSE),
('PROF045', 'Dr. Mauricio Sosa Montes', FALSE),
('PROF046', 'Mtro. Abisai Aragón Cruz', FALSE),
('PROF047', 'Mtra. Lizeth Daniza Gómez Hernández', FALSE),
('PROF048', 'Dr. Diego Soto Hernández', FALSE),
('PROF049', 'Mtra. Abisal Aragón Cruz', FALSE),
('PROF050', 'Mtra. Rosario Maya Lucas', FALSE),
('PROF051', 'Mtra. Enrique Martínez Sánchez', FALSE),
-- Administración Municipal
('PROF052', 'Dr. Joaquín H. Camacho Vera', FALSE),
('PROF053', 'Dr. Omar Ávila Flores', FALSE),
('PROF054', 'Dra. Felicitas Ortiz García', FALSE),
('PROF055', 'Mtra. Emanuel L. Ramírez Arellanes', FALSE),
('PROF056', 'Mtra. Eleazar Brena García', FALSE),
('PROF057', 'Mtro. Eleazar Brena García', FALSE),
-- Nutrición
('PROF058', 'M.C.B. Araceli Meneses Corona', FALSE),
('PROF059', 'L.N. Yannick José Ruiz Ramos', FALSE),
('PROF060', 'L.N. César Juárez Durán', FALSE),
('PROF061', 'Dra. Claudia Villanueva Cañongo', FALSE),
('PROF062', 'M.D.G.P.L. Eleazar Brena García', FALSE),
('PROF063', 'Dr. Juan Carlos Barragán Gálvez', FALSE),
('PROF064', 'Méd. Marcos Uriel Cuevas Olivera', FALSE),
('PROF065', 'Psic. Odalis Daniela Flores Bustamante', FALSE),
('PROF066', 'Méd. Alain Ayrton Chávez Gómez', FALSE),
('PROF067', 'M.S.P. Teófila Enriquez Almaraz', FALSE),
('PROF068', 'Dra. Fabiola López Bautista', FALSE),
('PROF069', 'M.F. Máximo Jorge Zaavedra García', FALSE),
('PROF070', 'M.S.P. Eric Ramirez Bohórquez', FALSE),
('PROF071', 'M.C.A. Laura Jocelyn Valdéz Gutiérrez', FALSE),
('PROF072', 'M.N.C. Griselda Belen Avendaño Rodríguez', FALSE),
('PROF073', 'M.C.A.C. Jorge Alberto Cruz Tolentino', FALSE),
-- Odontología
('PROF074', 'C.D. Mauricio González Osorio', FALSE),
('PROF075', 'C.D. Katia Cecilia González Vásquez', FALSE),
('PROF076', 'C.D.E.O. Carlos Ogarrio Ramírez', FALSE),
('PROF077', 'Mtro. Diego Ortega Pacheco', FALSE),
('PROF078', 'Amalinalli Barón Zaragoza', FALSE),
('PROF079', 'C.D. Jawer López Reyes', FALSE),
-- Enfermería
('PROF080', 'M.C.E. Ignacio Grajales Alonso', FALSE),
('PROF081', 'Dra. Roxana Nayeli Guerrero Sotelo', FALSE),
('PROF082', 'M.T.H.E.Q. Margarita Selene Aragón Sierra', FALSE),
('PROF083', 'Dra. Deisy Coromoto Rebolledo López', FALSE),
('PROF084', 'M.E.D. Verónica García Brena', FALSE),
-- Medicina
('PROF085', 'Méd. Xochiquetzalli García Mendoza', FALSE),
('PROF086', 'E.E. Edgar García Casas', FALSE),
('PROF087', 'Méd. Jasiibe Ivette Cruz Vásquez', FALSE)
ON CONFLICT (id_profesor) DO NOTHING;

-- =====================================================
-- 4. PERIODOS ACADÉMICOS
-- =====================================================
INSERT INTO periodos_academicos (id_periodo, nombre_periodo) VALUES
('2025-1', 'Enero-Junio 2025'),
('2025-2', 'Agosto-Diciembre 2025'),
('2026-1', 'Enero-Junio 2026')
ON CONFLICT (id_periodo) DO NOTHING;

-- =====================================================
-- 5. MATERIAS
-- =====================================================
INSERT INTO materias (id_materia, nombre_materia) VALUES
-- Ciencias Empresariales
('MAT001', 'Introducción a la Contabilidad'),
('MAT002', 'Introducción a las Ciencias Administrativas'),
('MAT003', 'Informática Empresarial'),
('MAT004', 'Historia del Pensamiento Filosófico'),
('MAT005', 'Matemáticas para Ciencias Empresariales'),
('MAT006', 'Administración de Recursos Humanos II'),
('MAT007', 'Derecho Mercantil'),
('MAT008', 'Estadística Inferencial'),
('MAT009', 'Administración de Compras e Inventarios'),
('MAT010', 'Contabilidad de Costos'),
('MAT011', 'Finanzas Empresariales I'),
('MAT012', 'Derecho Fiscal'),
('MAT013', 'Taller de Metodología de la Investigación'),
('MAT014', 'Administración de Sueldos y Salarios'),
('MAT015', 'Macroeconomía'),
('MAT016', 'Administración Estratégica de Ventas'),
('MAT017', 'Sistema Financiero'),
('MAT018', 'Comercio Exterior'),
('MAT019', 'Gestión de la Calidad'),
('MAT020', 'Finanzas Corporativas'),
('MAT021', 'Emprendimiento de Negocios'),
('MAT022', 'Cultura Empresarial'),
-- Ciencias Biomédicas
('MAT023', 'Biología celular'),
('MAT024', 'Matemáticas'),
('MAT025', 'Introducción a Metodología de Investigación'),
('MAT026', 'Química'),
('MAT027', 'Bioquímica Metabólica'),
('MAT028', 'Bioseguridad'),
('MAT029', 'Histología'),
('MAT030', 'TIC Aplicadas a las Ciencias Biomédicas'),
('MAT031', 'Anatomía'),
-- Sistemas Computacionales
('MAT032', 'Diseño Estructurado de Algoritmos'),
('MAT033', 'Administración'),
('MAT034', 'Lógica Matemática'),
('MAT035', 'Cálculo I'),
('MAT036', 'Estructuras de Datos'),
('MAT037', 'Electrónica Digital'),
('MAT038', 'Contabilidad y Finanzas'),
('MAT039', 'Teoría de Autómatas'),
('MAT040', 'Álgebra Lineal'),
('MAT041', 'Paradigmas de Programación II'),
('MAT042', 'Redes I'),
('MAT043', 'Bases de Datos II'),
('MAT044', 'Fundamentos de Sistemas Operativos'),
('MAT045', 'Diseño Web'),
('MAT046', 'Tecnologías Web II'),
('MAT047', 'Bases de Datos Avanzadas'),
('MAT048', 'Ingeniería de Software II'),
('MAT049', 'Probabilidad y Estadística'),
('MAT050', 'Derecho y Legislación en Informática'),
('MAT051', 'Inteligencia Artificial I'),
-- Administración Pública
('MAT052', 'Introducción al Sistema Jurídico Mexicano'),
('MAT053', 'Fundamentos de la Administración Pública'),
('MAT054', 'Historia Mundial'),
('MAT055', 'Matemáticas Aplicadas a las Ciencias Sociales'),
('MAT056', 'Derecho Administrativo'),
('MAT057', 'Microeconomía'),
('MAT058', 'Teoría General del Estado'),
('MAT059', 'Sociedad y Estado en México'),
('MAT060', 'Gobierno y Asuntos Públicos'),
('MAT061', 'Gerencia Pública'),
('MAT062', 'Sistema Político Mexicano'),
('MAT063', 'Finanzas Públicas I'),
('MAT064', 'Sistemas de Auditoría Gubernamental'),
('MAT065', 'Gerencia Social'),
('MAT066', 'Procesos de Gobierno en México (Fed.)'),
('MAT067', 'Ética y Rendición de Cuentas Públicas'),
('MAT068', 'Planeación Estratégica'),
('MAT069', 'Gestión y Administración Urbanas'),
('MAT070', 'Procesos de Gobierno en México (Mun.)'),
('MAT071', 'Seminario de Tesis I'),
-- Administración Municipal
('MAT072', 'Sistemas Políticos de Gobierno Municipal'),
('MAT073', 'Derecho Agrario y Análisis de Conflictos'),
('MAT074', 'Gestión de la Información Territorial II'),
('MAT075', 'Contabilidad Gubernamental'),
('MAT076', 'Planeación, Programación y Presupuesto'),
('MAT077', 'Sustentabilidad y Gestión Local'),
('MAT078', 'Desarrollo Urbano'),
('MAT079', 'Metodología de la Investigación Cuantitativa'),
('MAT080', 'Auditoría Gubernamental'),
('MAT081', 'Administración de Servicios Públicos Municipales'),
('MAT082', 'Sistemas de Evaluación y Seguimiento'),
('MAT083', 'Administración de Obras Públicas'),
('MAT084', 'Formulación y Evaluación de Proyectos'),
-- Nutrición
('MAT085', 'Fundamentos de Nutrición Humana'),
('MAT086', 'Anatomía y Fisiología Humana I'),
('MAT087', 'Antropología de la Alimentación'),
('MAT088', 'Química Nutricional'),
('MAT089', 'Bioquímica Nutricional II'),
('MAT090', 'Patología I'),
('MAT091', 'Psicología Alimentaria y Nutricional'),
('MAT092', 'Microbiología y Parasitología de los Alimentos'),
('MAT093', 'Educación y Nutrición'),
('MAT094', 'Gastroenterología Nutricional'),
('MAT095', 'Cálculo y Lab. Nutrición en Ciclo de Vida'),
('MAT096', 'Lab. Evaluación del Estado de Nutrición'),
('MAT097', 'Administración General'),
('MAT098', 'Nutrición Poblacional II'),
('MAT099', 'Nutrición y Farmacología'),
('MAT100', 'Análisis de Alimentos'),
('MAT101', 'Química de los Alimentos'),
('MAT102', 'Administración de Servicios de Alimentos II'),
('MAT103', 'Atención Clínica Nutricional'),
('MAT104', 'Bioestadística'),
('MAT105', 'Nutrición en Salud Pública'),
('MAT106', 'Métodos y Técnicas de Investigación'),
('MAT107', 'Tecnología de Alimentos de Origen Animal'),
-- Odontología
('MAT108', 'Cirugía Bucal'),
('MAT109', 'Odontopediatría'),
('MAT110', 'Ortodoncia'),
('MAT111', 'Investigación en Salud'),
('MAT112', 'Periodoncia'),
-- Enfermería
('MAT113', 'Bases Epistemológicas de la Enfermería'),
('MAT114', 'Bioquímica para Enfermería'),
('MAT115', 'Anatomía Humana I'),
('MAT116', 'Sociología y Salud'),
-- Medicina
('MAT117', 'Histología I'),
('MAT118', 'Bioquímica'),
('MAT119', 'Embriología')
ON CONFLICT (id_materia) DO NOTHING;

-- =====================================================
-- 6. TIPOS DE EVALUACIÓN
-- =====================================================
INSERT INTO tipos_de_evaluacion (id_evaluacion, nombre_evaluacion) VALUES
('EVAL001', 'Parcial 1'),
('EVAL002', 'Parcial 2'),
('EVAL003', 'Parcial 3'),
('EVAL004', 'Ordinario')
ON CONFLICT (id_evaluacion) DO NOTHING;

-- =====================================================
-- 7. AULAS
-- =====================================================
INSERT INTO aulas (id_aula, nombre_aula, capacidad, is_disable) VALUES
('AULA001', 'Aula E4', 30, FALSE),
('AULA002', 'Aula D7', 30, FALSE),
('AULA003', 'Aula SC-CEDGE', 25, FALSE),
('AULA004', 'Aula C2', 30, FALSE),
('AULA005', 'Aula D9', 30, FALSE),
('AULA006', 'Aula C4', 30, FALSE),
('AULA007', 'Aula F1', 40, FALSE),
('AULA008', 'Aula CEDGE-DO', 25, FALSE),
('AULA009', 'Aula F2', 40, FALSE),
('AULA010', 'Aula CEDGE-SIG', 25, FALSE),
('AULA011', 'Aula F3', 40, FALSE),
('AULA012', 'Aula H2', 30, FALSE),
('AULA013', 'Aula D2', 30, FALSE),
('AULA014', 'Aula J6', 30, FALSE),
('AULA015', 'Aula J7', 30, FALSE),
('AULA016', 'Aula G6', 30, FALSE),
('AULA017', 'Aula E5', 30, FALSE),
('AULA018', 'Aula G1', 30, FALSE),
('AULA019', 'Aula SC 11', 30, FALSE),
('AULA020', 'Aula D1', 30, FALSE),
('AULA021', 'Aula CETI-S.O', 25, FALSE),
('AULA022', 'Aula SC 8', 30, FALSE),
('AULA023', 'Aula D4', 30, FALSE),
('AULA024', 'Aula D3', 30, FALSE),
('AULA025', 'Aula CETI-DES SW', 25, FALSE),
('AULA026', 'Aula CETI-ING SW', 25, FALSE),
('AULA027', 'Aula SC 9', 30, FALSE),
('AULA028', 'Aula CETI-TEC WEB', 25, FALSE),
('AULA029', 'Aula CETI-REDES', 25, FALSE),
('AULA030', 'Aula B1', 30, FALSE),
('AULA031', 'Aula CEDGE-DO', 25, FALSE),
('AULA032', 'Aula B2', 30, FALSE),
('AULA033', 'Aula C1', 30, FALSE),
('AULA034', 'Aula B3', 30, FALSE),
('AULA035', 'Aula CEDGE-SALA', 30, FALSE),
('AULA036', 'Aula B4', 30, FALSE),
('AULA037', 'Aula LGE', 30, FALSE),
('AULA038', 'Aula DEP 4', 30, FALSE),
('AULA039', 'Aula SC CAD', 30, FALSE),
('AULA040', 'Aula K3', 30, FALSE),
('AULA041', 'Aula SC 6', 30, FALSE),
('AULA042', 'Aula SC BIBLIOTECA', 50, FALSE),
('AULA043', 'Aula SC 4', 30, FALSE),
('AULA044', 'Aula SC 10', 30, FALSE),
('AULA045', 'Aula SC 5', 30, FALSE),
('AULA046', 'Aula SC 2', 30, FALSE),
('AULA047', 'Aula SC 3', 30, FALSE),
('AULA048', 'Aula J1', 30, FALSE),
('AULA049', 'Aula K6', 30, FALSE),
('AULA050', 'Aula K4', 30, FALSE),
('AULA051', 'Aula K7', 30, FALSE),
('AULA052', 'Aula J2', 30, FALSE)
ON CONFLICT (id_aula) DO NOTHING;

-- =====================================================
-- 8. GRUPOS ESCOLARES
-- =====================================================
INSERT INTO grupos_escolares (id_grupo, nombre_grupo, numero_alumnos, id_carrera) VALUES
-- Ciencias Empresariales
('GRUPO001', '104A', 30, 'LIC-CE'),
('GRUPO002', '104B', 30, 'LIC-CE'),
('GRUPO003', '304', 30, 'LIC-CE'),
('GRUPO004', '504', 30, 'LIC-CE'),
('GRUPO005', '704', 25, 'LIC-CE'),
('GRUPO006', '904', 25, 'LIC-CE'),
-- Ciencias Biomédicas
('GRUPO007', '116A', 30, 'LIC-CB'),
('GRUPO008', '116B', 30, 'LIC-CB'),
('GRUPO009', '316', 30, 'LIC-CB'),
-- Sistemas Computacionales
('GRUPO010', '106B', 30, 'LIC-SC'),
('GRUPO011', '306A', 30, 'LIC-SC'),
('GRUPO012', '306B', 30, 'LIC-SC'),
('GRUPO013', '506', 30, 'LIC-SC'),
('GRUPO014', '706', 30, 'LIC-SC'),
('GRUPO015', '906', 25, 'LIC-SC'),
-- Administración Pública
('GRUPO016', '105', 30, 'LIC-AP'),
('GRUPO017', '305', 30, 'LIC-AP'),
('GRUPO018', '505', 30, 'LIC-AP'),
('GRUPO019', '705', 25, 'LIC-AP'),
('GRUPO020', '905', 25, 'LIC-AP'),
-- Administración Municipal
('GRUPO021', '501', 30, 'LIC-AM'),
('GRUPO022', '701', 30, 'LIC-AM'),
('GRUPO023', '901', 25, 'LIC-AM'),
-- Nutrición
('GRUPO024', '107A', 30, 'LIC-NUT'),
('GRUPO025', '107B', 30, 'LIC-NUT'),
('GRUPO026', '307', 30, 'LIC-NUT'),
('GRUPO027', '507', 30, 'LIC-NUT'),
('GRUPO028', '707', 25, 'LIC-NUT'),
('GRUPO029', '907', 25, 'LIC-NUT'),
-- Odontología
('GRUPO030', '913A', 25, 'LIC-ODO'),
('GRUPO031', '913B', 25, 'LIC-ODO'),
('GRUPO032', '913C', 25, 'LIC-ODO'),
-- Enfermería
('GRUPO033', '103-A', 30, 'LIC-ENF'),
('GRUPO034', '103-B', 30, 'LIC-ENF'),
-- Medicina
('GRUPO035', '114A', 30, 'LIC-MED')
ON CONFLICT (id_grupo) DO NOTHING;

-- =====================================================
-- 9. VENTANAS DE APLICACIÓN
-- =====================================================
-- Tercera Evaluación Parcial: 19 al 26 de enero de 2026
INSERT INTO ventanas_de_aplicacion_por_periodo (id_ventana, id_periodo, id_evaluacion, fecha_inicio_examenes, fecha_fin_examenes) VALUES
('VENT005', '2025-1', 'EVAL003', '2026-01-19', '2026-01-26'),
('VENT006', '2025-2', 'EVAL003', '2026-01-19', '2026-01-26'),
('VENT007', '2026-1', 'EVAL003', '2026-01-19', '2026-01-26')
ON CONFLICT (id_ventana) DO NOTHING;

-- =====================================================
-- 10. HORARIOS REGULARES DE CLASE
-- =====================================================
-- Nota: Los horarios se infieren del día de la semana del examen
-- 20/01/2026 = Martes (dia_semana = 1)
-- 21/01/2026 = Miércoles (dia_semana = 2)
-- 22/01/2026 = Jueves (dia_semana = 3)
-- 23/01/2026 = Viernes (dia_semana = 4)
-- 26/01/2026 = Lunes (dia_semana = 0)

-- Ciencias Empresariales - Grupo 104A
INSERT INTO horarios_regulares_de_clase (id_horario_clase, id_periodo, id_materia, id_grupo, id_profesor, id_aula, dia_semana, hora_inicio, hora_fin) VALUES
('HOR001', '2025-1', 'MAT001', 'GRUPO001', 'PROF001', 'AULA001', 1, '08:00:00', '09:00:00'),
('HOR002', '2025-1', 'MAT002', 'GRUPO001', 'PROF002', 'AULA002', 2, '17:00:00', '18:00:00'),
('HOR003', '2025-1', 'MAT003', 'GRUPO001', 'PROF003', 'AULA003', 3, '11:00:00', '12:00:00'),
('HOR004', '2025-1', 'MAT004', 'GRUPO001', 'PROF004', 'AULA001', 4, '12:00:00', '13:00:00'),
('HOR005', '2025-1', 'MAT005', 'GRUPO001', 'PROF005', 'AULA004', 0, '08:00:00', '09:00:00'),
-- Grupo 104B
('HOR006', '2025-1', 'MAT001', 'GRUPO002', 'PROF001', 'AULA001', 1, '08:00:00', '09:00:00'),
('HOR007', '2025-1', 'MAT002', 'GRUPO002', 'PROF002', 'AULA002', 2, '17:00:00', '18:00:00'),
('HOR008', '2025-1', 'MAT003', 'GRUPO002', 'PROF006', 'AULA003', 3, '16:00:00', '17:00:00'),
('HOR009', '2025-1', 'MAT004', 'GRUPO002', 'PROF004', 'AULA001', 4, '12:00:00', '13:00:00'),
('HOR010', '2025-1', 'MAT005', 'GRUPO002', 'PROF007', 'AULA005', 0, '08:00:00', '09:00:00'),
-- Grupo 304
('HOR011', '2025-1', 'MAT006', 'GRUPO003', 'PROF004', 'AULA006', 1, '09:00:00', '10:00:00'),
('HOR012', '2025-1', 'MAT007', 'GRUPO003', 'PROF008', 'AULA004', 2, '12:00:00', '13:00:00'),
('HOR013', '2025-1', 'MAT008', 'GRUPO003', 'PROF009', 'AULA006', 3, '17:00:00', '18:00:00'),
('HOR014', '2025-1', 'MAT009', 'GRUPO003', 'PROF010', 'AULA006', 4, '11:00:00', '12:00:00'),
('HOR015', '2025-1', 'MAT010', 'GRUPO003', 'PROF011', 'AULA007', 0, '10:00:00', '11:00:00'),
-- Grupo 504
('HOR016', '2025-1', 'MAT011', 'GRUPO004', 'PROF012', 'AULA003', 1, '09:00:00', '10:00:00'),
('HOR017', '2025-1', 'MAT012', 'GRUPO004', 'PROF008', 'AULA007', 2, '13:00:00', '14:00:00'),
('HOR018', '2025-1', 'MAT013', 'GRUPO004', 'PROF002', 'AULA008', 3, '10:00:00', '11:00:00'),
('HOR019', '2025-1', 'MAT014', 'GRUPO004', 'PROF001', 'AULA007', 4, '11:00:00', '12:00:00'),
('HOR020', '2025-1', 'MAT015', 'GRUPO004', 'PROF013', 'AULA007', 0, '16:00:00', '17:00:00'),
-- Grupo 704
('HOR021', '2025-1', 'MAT016', 'GRUPO005', 'PROF011', 'AULA009', 4, '08:00:00', '09:00:00'),
('HOR022', '2025-1', 'MAT017', 'GRUPO005', 'PROF012', 'AULA010', 0, '11:00:00', '12:00:00'),
-- Grupo 904
('HOR023', '2025-1', 'MAT018', 'GRUPO006', 'PROF014', 'AULA011', 1, '11:00:00', '12:00:00'),
('HOR024', '2025-1', 'MAT019', 'GRUPO006', 'PROF011', 'AULA011', 2, '12:00:00', '13:00:00'),
('HOR025', '2025-1', 'MAT020', 'GRUPO006', 'PROF010', 'AULA011', 3, '16:00:00', '17:00:00'),
('HOR026', '2025-1', 'MAT021', 'GRUPO006', 'PROF015', 'AULA010', 4, '13:00:00', '14:00:00'),
('HOR027', '2025-1', 'MAT022', 'GRUPO006', 'PROF002', 'AULA011', 0, '09:00:00', '10:00:00'),
-- Ciencias Biomédicas - Grupo 116A
('HOR028', '2025-1', 'MAT023', 'GRUPO007', 'PROF016', 'AULA012', 1, '16:00:00', '17:00:00'),
('HOR029', '2025-1', 'MAT004', 'GRUPO007', 'PROF017', 'AULA012', 2, '16:00:00', '17:00:00'),
('HOR030', '2025-1', 'MAT024', 'GRUPO007', 'PROF018', 'AULA013', 3, '10:00:00', '11:00:00'),
('HOR031', '2025-1', 'MAT025', 'GRUPO007', 'PROF019', 'AULA014', 4, '09:00:00', '10:00:00'),
('HOR032', '2025-1', 'MAT026', 'GRUPO007', 'PROF020', 'AULA015', 0, '13:00:00', '14:00:00'),
-- Grupo 116B
('HOR033', '2025-1', 'MAT023', 'GRUPO008', 'PROF021', 'AULA016', 1, '16:00:00', '17:00:00'),
('HOR034', '2025-1', 'MAT004', 'GRUPO008', 'PROF017', 'AULA016', 2, '16:00:00', '17:00:00'),
('HOR035', '2025-1', 'MAT024', 'GRUPO008', 'PROF007', 'AULA001', 3, '10:00:00', '11:00:00'),
('HOR036', '2025-1', 'MAT025', 'GRUPO008', 'PROF019', 'AULA017', 4, '09:00:00', '10:00:00'),
('HOR037', '2025-1', 'MAT026', 'GRUPO008', 'PROF022', 'AULA001', 0, '13:00:00', '14:00:00'),
-- Grupo 316
('HOR038', '2025-1', 'MAT027', 'GRUPO009', 'PROF023', 'AULA013', 1, '17:00:00', '18:00:00'),
('HOR039', '2025-1', 'MAT028', 'GRUPO009', 'PROF024', 'AULA018', 2, '08:00:00', '09:00:00'),
('HOR040', '2025-1', 'MAT029', 'GRUPO009', 'PROF025', 'AULA019', 3, '11:00:00', '12:00:00'),
('HOR041', '2025-1', 'MAT030', 'GRUPO009', 'PROF006', 'AULA020', 4, '10:00:00', '11:00:00'),
('HOR042', '2025-1', 'MAT031', 'GRUPO009', 'PROF026', 'AULA013', 0, '11:00:00', '12:00:00'),
-- Sistemas Computacionales - Grupo 106B
('HOR043', '2025-1', 'MAT032', 'GRUPO010', 'PROF027', 'AULA021', 1, '12:00:00', '13:00:00'),
('HOR044', '2025-1', 'MAT033', 'GRUPO010', 'PROF028', 'AULA022', 2, '13:00:00', '14:00:00'),
('HOR045', '2025-1', 'MAT004', 'GRUPO010', 'PROF029', 'AULA023', 3, '16:00:00', '17:00:00'),
('HOR046', '2025-1', 'MAT034', 'GRUPO010', 'PROF030', 'AULA023', 4, '10:00:00', '11:00:00'),
('HOR047', '2025-1', 'MAT035', 'GRUPO010', 'PROF031', 'AULA024', 0, '11:00:00', '12:00:00'),
-- Grupo 306A
('HOR048', '2025-1', 'MAT036', 'GRUPO011', 'PROF032', 'AULA025', 1, '13:00:00', '14:00:00'),
('HOR049', '2025-1', 'MAT037', 'GRUPO011', 'PROF007', 'AULA026', 2, '17:00:00', '18:00:00'),
('HOR050', '2025-1', 'MAT038', 'GRUPO011', 'PROF011', 'AULA027', 3, '11:00:00', '12:00:00'),
('HOR051', '2025-1', 'MAT039', 'GRUPO011', 'PROF033', 'AULA025', 4, '09:00:00', '10:00:00'),
('HOR052', '2025-1', 'MAT040', 'GRUPO011', 'PROF031', 'AULA026', 0, '08:00:00', '09:00:00'),
-- Grupo 306B
('HOR053', '2025-1', 'MAT036', 'GRUPO012', 'PROF018', 'AULA028', 1, '09:00:00', '10:00:00'),
('HOR054', '2025-1', 'MAT037', 'GRUPO012', 'PROF007', 'AULA026', 2, '17:00:00', '18:00:00'),
('HOR055', '2025-1', 'MAT038', 'GRUPO012', 'PROF011', 'AULA027', 3, '11:00:00', '12:00:00'),
('HOR056', '2025-1', 'MAT039', 'GRUPO012', 'PROF033', 'AULA025', 4, '12:00:00', '13:00:00'),
('HOR057', '2025-1', 'MAT040', 'GRUPO012', 'PROF031', 'AULA026', 0, '08:00:00', '09:00:00'),
-- Grupo 506
('HOR058', '2025-1', 'MAT041', 'GRUPO013', 'PROF027', 'AULA021', 1, '13:00:00', '14:00:00'),
('HOR059', '2025-1', 'MAT042', 'GRUPO013', 'PROF034', 'AULA021', 2, '16:00:00', '17:00:00'),
('HOR060', '2025-1', 'MAT043', 'GRUPO013', 'PROF035', 'AULA021', 3, '09:00:00', '10:00:00'),
('HOR061', '2025-1', 'MAT044', 'GRUPO013', 'PROF029', 'AULA028', 4, '10:00:00', '11:00:00'),
('HOR062', '2025-1', 'MAT045', 'GRUPO013', 'PROF032', 'AULA028', 0, '17:00:00', '18:00:00'),
-- Grupo 706
('HOR063', '2025-1', 'MAT046', 'GRUPO014', 'PROF018', 'AULA028', 1, '08:00:00', '09:00:00'),
('HOR064', '2025-1', 'MAT047', 'GRUPO014', 'PROF032', 'AULA028', 2, '12:00:00', '13:00:00'),
('HOR065', '2025-1', 'MAT048', 'GRUPO014', 'PROF036', 'AULA025', 3, '11:00:00', '12:00:00'),
('HOR066', '2025-1', 'MAT049', 'GRUPO014', 'PROF037', 'AULA026', 4, '09:00:00', '10:00:00'),
('HOR067', '2025-1', 'MAT050', 'GRUPO014', 'PROF038', 'AULA029', 0, '17:00:00', '18:00:00'),
-- Grupo 906
('HOR068', '2025-1', 'MAT051', 'GRUPO015', 'PROF033', 'AULA021', 0, '11:00:00', '12:00:00'),
-- Administración Pública - Grupo 105
('HOR069', '2025-1', 'MAT052', 'GRUPO016', 'PROF039', 'AULA030', 1, '09:00:00', '10:00:00'),
('HOR070', '2025-1', 'MAT053', 'GRUPO016', 'PROF040', 'AULA030', 2, '13:00:00', '14:00:00'),
('HOR071', '2025-1', 'MAT004', 'GRUPO016', 'PROF041', 'AULA030', 3, '16:00:00', '17:00:00'),
('HOR072', '2025-1', 'MAT054', 'GRUPO016', 'PROF042', 'AULA031', 4, '12:00:00', '13:00:00'),
('HOR073', '2025-1', 'MAT055', 'GRUPO016', 'PROF005', 'AULA030', 0, '11:00:00', '12:00:00'),
-- Grupo 305
('HOR074', '2025-1', 'MAT056', 'GRUPO017', 'PROF008', 'AULA010', 1, '09:00:00', '10:00:00'),
('HOR075', '2025-1', 'MAT057', 'GRUPO017', 'PROF045', 'AULA032', 2, '17:00:00', '18:00:00'),
('HOR076', '2025-1', 'MAT058', 'GRUPO017', 'PROF043', 'AULA032', 3, '11:00:00', '12:00:00'),
('HOR077', '2025-1', 'MAT059', 'GRUPO017', 'PROF042', 'AULA010', 4, '08:00:00', '09:00:00'),
('HOR078', '2025-1', 'MAT060', 'GRUPO017', 'PROF044', 'AULA032', 0, '12:00:00', '13:00:00'),
-- Grupo 505
('HOR079', '2025-1', 'MAT061', 'GRUPO018', 'PROF046', 'AULA033', 1, '16:00:00', '17:00:00'),
('HOR080', '2025-1', 'MAT060', 'GRUPO018', 'PROF044', 'AULA031', 2, '17:00:00', '18:00:00'),
('HOR081', '2025-1', 'MAT062', 'GRUPO018', 'PROF042', 'AULA034', 3, '09:00:00', '10:00:00'),
('HOR082', '2025-1', 'MAT063', 'GRUPO018', 'PROF012', 'AULA035', 4, '12:00:00', '13:00:00'),
('HOR083', '2025-1', 'MAT015', 'GRUPO018', 'PROF045', 'AULA034', 0, '10:00:00', '11:00:00'),
-- Grupo 705
('HOR084', '2025-1', 'MAT064', 'GRUPO019', 'PROF047', 'AULA036', 3, '11:00:00', '12:00:00'),
('HOR085', '2025-1', 'MAT065', 'GRUPO019', 'PROF040', 'AULA010', 4, '12:00:00', '13:00:00'),
('HOR086', '2025-1', 'MAT066', 'GRUPO019', 'PROF039', 'AULA036', 0, '16:00:00', '17:00:00'),
-- Grupo 905
('HOR087', '2025-1', 'MAT067', 'GRUPO020', 'PROF048', 'AULA036', 1, '10:00:00', '11:00:00'),
('HOR088', '2025-1', 'MAT068', 'GRUPO020', 'PROF049', 'AULA037', 2, '17:00:00', '18:00:00'),
('HOR089', '2025-1', 'MAT069', 'GRUPO020', 'PROF017', 'AULA010', 3, '16:00:00', '17:00:00'),
('HOR090', '2025-1', 'MAT070', 'GRUPO020', 'PROF050', 'AULA036', 4, '09:00:00', '10:00:00'),
('HOR091', '2025-1', 'MAT071', 'GRUPO020', 'PROF051', 'AULA035', 0, '13:00:00', '14:00:00'),
-- Administración Municipal - Grupo 501
('HOR092', '2025-1', 'MAT072', 'GRUPO021', 'PROF041', 'AULA034', 1, '11:00:00', '12:00:00'),
('HOR093', '2025-1', 'MAT073', 'GRUPO021', 'PROF052', 'AULA034', 2, '16:00:00', '17:00:00'),
('HOR094', '2025-1', 'MAT074', 'GRUPO021', 'PROF053', 'AULA010', 3, '17:00:00', '18:00:00'),
('HOR095', '2025-1', 'MAT075', 'GRUPO021', 'PROF054', 'AULA034', 4, '08:00:00', '09:00:00'),
('HOR096', '2025-1', 'MAT015', 'GRUPO021', 'PROF045', 'AULA034', 0, '10:00:00', '11:00:00'),
-- Grupo 701
('HOR097', '2025-1', 'MAT076', 'GRUPO022', 'PROF055', 'AULA033', 1, '12:00:00', '13:00:00'),
('HOR098', '2025-1', 'MAT077', 'GRUPO022', 'PROF056', 'AULA033', 2, '17:00:00', '18:00:00'),
('HOR099', '2025-1', 'MAT078', 'GRUPO022', 'PROF053', 'AULA033', 3, '11:00:00', '12:00:00'),
('HOR100', '2025-1', 'MAT079', 'GRUPO022', 'PROF045', 'AULA033', 4, '08:00:00', '09:00:00'),
('HOR101', '2025-1', 'MAT080', 'GRUPO022', 'PROF054', 'AULA038', 0, '09:00:00', '10:00:00'),
-- Grupo 901
('HOR102', '2025-1', 'MAT081', 'GRUPO023', 'PROF014', 'AULA006', 1, '10:00:00', '11:00:00'),
('HOR103', '2025-1', 'MAT082', 'GRUPO023', 'PROF049', 'AULA035', 2, '08:00:00', '09:00:00'),
('HOR104', '2025-1', 'MAT083', 'GRUPO023', 'PROF053', 'AULA006', 3, '16:00:00', '17:00:00'),
('HOR105', '2025-1', 'MAT084', 'GRUPO023', 'PROF057', 'AULA006', 4, '12:00:00', '13:00:00'),
('HOR106', '2025-1', 'MAT071', 'GRUPO023', 'PROF051', 'AULA035', 0, '13:00:00', '14:00:00'),
-- Nutrición - Grupo 107A
('HOR107', '2025-1', 'MAT085', 'GRUPO024', 'PROF058', 'AULA039', 1, '11:00:00', '12:00:00'),
('HOR108', '2025-1', 'MAT086', 'GRUPO024', 'PROF059', 'AULA039', 2, '08:00:00', '09:00:00'),
('HOR109', '2025-1', 'MAT087', 'GRUPO024', 'PROF060', 'AULA039', 3, '09:00:00', '10:00:00'),
('HOR110', '2025-1', 'MAT088', 'GRUPO024', 'PROF061', 'AULA040', 4, '12:00:00', '13:00:00'),
('HOR111', '2025-1', 'MAT004', 'GRUPO024', 'PROF062', 'AULA039', 0, '16:00:00', '17:00:00'),
-- Grupo 107B
('HOR112', '2025-1', 'MAT085', 'GRUPO025', 'PROF058', 'AULA041', 1, '11:00:00', '12:00:00'),
('HOR113', '2025-1', 'MAT086', 'GRUPO025', 'PROF059', 'AULA041', 2, '08:00:00', '09:00:00'),
('HOR114', '2025-1', 'MAT087', 'GRUPO025', 'PROF060', 'AULA041', 3, '09:00:00', '10:00:00'),
('HOR115', '2025-1', 'MAT088', 'GRUPO025', 'PROF061', 'AULA040', 4, '12:00:00', '13:00:00'),
('HOR116', '2025-1', 'MAT004', 'GRUPO025', 'PROF062', 'AULA041', 0, '16:00:00', '17:00:00'),
-- Grupo 307
('HOR117', '2025-1', 'MAT089', 'GRUPO026', 'PROF063', 'AULA019', 1, '09:00:00', '10:00:00'),
('HOR118', '2025-1', 'MAT090', 'GRUPO026', 'PROF064', 'AULA019', 2, '12:00:00', '13:00:00'),
('HOR119', '2025-1', 'MAT091', 'GRUPO026', 'PROF065', 'AULA019', 3, '16:00:00', '17:00:00'),
('HOR120', '2025-1', 'MAT092', 'GRUPO026', 'PROF021', 'AULA019', 4, '08:00:00', '09:00:00'),
('HOR121', '2025-1', 'MAT093', 'GRUPO026', 'PROF060', 'AULA019', 0, '10:00:00', '11:00:00'),
-- Grupo 507
('HOR122', '2025-1', 'MAT094', 'GRUPO027', 'PROF066', 'AULA042', 1, '13:00:00', '14:00:00'),
('HOR123', '2025-1', 'MAT095', 'GRUPO027', 'PROF067', 'AULA043', 2, '16:00:00', '17:00:00'),
('HOR124', '2025-1', 'MAT096', 'GRUPO027', 'PROF068', 'AULA043', 3, '12:00:00', '13:00:00'),
('HOR125', '2025-1', 'MAT097', 'GRUPO027', 'PROF069', 'AULA042', 4, '17:00:00', '18:00:00'),
('HOR126', '2025-1', 'MAT098', 'GRUPO027', 'PROF070', 'AULA042', 0, '08:00:00', '09:00:00'),
-- Grupo 707
('HOR127', '2025-1', 'MAT099', 'GRUPO028', 'PROF059', 'AULA044', 2, '10:00:00', '11:00:00'),
('HOR128', '2025-1', 'MAT100', 'GRUPO028', 'PROF061', 'AULA044', 3, '08:00:00', '09:00:00'),
('HOR129', '2025-1', 'MAT101', 'GRUPO028', 'PROF071', 'AULA044', 4, '11:00:00', '12:00:00'),
('HOR130', '2025-1', 'MAT102', 'GRUPO028', 'PROF068', 'AULA044', 0, '16:00:00', '17:00:00'),
-- Grupo 907
('HOR131', '2025-1', 'MAT103', 'GRUPO029', 'PROF072', 'AULA039', 1, '13:00:00', '14:00:00'),
('HOR132', '2025-1', 'MAT104', 'GRUPO029', 'PROF073', 'AULA045', 2, '09:00:00', '10:00:00'),
('HOR133', '2025-1', 'MAT105', 'GRUPO029', 'PROF070', 'AULA045', 3, '12:00:00', '13:00:00'),
('HOR134', '2025-1', 'MAT106', 'GRUPO029', 'PROF067', 'AULA039', 4, '17:00:00', '18:00:00'),
('HOR135', '2025-1', 'MAT107', 'GRUPO029', 'PROF061', 'AULA039', 0, '08:00:00', '09:00:00'),
-- Odontología - Grupo 913A
('HOR136', '2025-1', 'MAT108', 'GRUPO030', 'PROF074', 'AULA022', 1, '10:00:00', '11:00:00'),
('HOR137', '2025-1', 'MAT109', 'GRUPO030', 'PROF075', 'AULA022', 2, '09:00:00', '10:00:00'),
('HOR138', '2025-1', 'MAT110', 'GRUPO030', 'PROF076', 'AULA022', 3, '12:00:00', '13:00:00'),
('HOR139', '2025-1', 'MAT111', 'GRUPO030', 'PROF077', 'AULA022', 4, '17:00:00', '18:00:00'),
('HOR140', '2025-1', 'MAT112', 'GRUPO030', 'PROF078', 'AULA022', 0, '11:00:00', '12:00:00'),
-- Grupo 913B
('HOR141', '2025-1', 'MAT108', 'GRUPO031', 'PROF074', 'AULA027', 1, '10:00:00', '11:00:00'),
('HOR142', '2025-1', 'MAT109', 'GRUPO031', 'PROF075', 'AULA027', 2, '09:00:00', '10:00:00'),
('HOR143', '2025-1', 'MAT110', 'GRUPO031', 'PROF079', 'AULA019', 3, '12:00:00', '13:00:00'),
('HOR144', '2025-1', 'MAT111', 'GRUPO031', 'PROF077', 'AULA027', 4, '17:00:00', '18:00:00'),
('HOR145', '2025-1', 'MAT112', 'GRUPO031', 'PROF078', 'AULA019', 0, '11:00:00', '12:00:00'),
-- Grupo 913C
('HOR146', '2025-1', 'MAT108', 'GRUPO032', 'PROF074', 'AULA044', 1, '10:00:00', '11:00:00'),
('HOR147', '2025-1', 'MAT109', 'GRUPO032', 'PROF075', 'AULA044', 2, '09:00:00', '10:00:00'),
('HOR148', '2025-1', 'MAT110', 'GRUPO032', 'PROF079', 'AULA044', 3, '12:00:00', '13:00:00'),
('HOR149', '2025-1', 'MAT111', 'GRUPO032', 'PROF077', 'AULA044', 4, '17:00:00', '18:00:00'),
('HOR150', '2025-1', 'MAT112', 'GRUPO032', 'PROF078', 'AULA044', 0, '11:00:00', '12:00:00'),
-- Enfermería - Grupo 103-A
('HOR151', '2025-1', 'MAT113', 'GRUPO033', 'PROF080', 'AULA048', 1, '09:00:00', '10:00:00'),
('HOR152', '2025-1', 'MAT114', 'GRUPO033', 'PROF063', 'AULA001', 2, '17:00:00', '18:00:00'),
('HOR153', '2025-1', 'MAT004', 'GRUPO033', 'PROF036', 'AULA048', 3, '08:00:00', '09:00:00'),
('HOR154', '2025-1', 'MAT115', 'GRUPO033', 'PROF082', 'AULA048', 4, '10:00:00', '11:00:00'),
('HOR155', '2025-1', 'MAT116', 'GRUPO033', 'PROF083', 'AULA048', 0, '16:00:00', '17:00:00'),
-- Grupo 103-B
('HOR156', '2025-1', 'MAT113', 'GRUPO034', 'PROF080', 'AULA049', 1, '09:00:00', '10:00:00'),
('HOR157', '2025-1', 'MAT114', 'GRUPO034', 'PROF063', 'AULA052', 2, '17:00:00', '18:00:00'),
('HOR158', '2025-1', 'MAT004', 'GRUPO034', 'PROF081', 'AULA050', 3, '08:00:00', '09:00:00'),
('HOR159', '2025-1', 'MAT115', 'GRUPO034', 'PROF082', 'AULA051', 4, '10:00:00', '11:00:00'),
('HOR160', '2025-1', 'MAT116', 'GRUPO034', 'PROF084', 'AULA052', 0, '16:00:00', '17:00:00'),
-- Medicina - Grupo 114A
('HOR161', '2025-1', 'MAT115', 'GRUPO035', 'PROF085', 'AULA046', 1, '16:00:00', '17:00:00'),
('HOR162', '2025-1', 'MAT117', 'GRUPO035', 'PROF086', 'AULA046', 2, '09:00:00', '10:00:00'),
('HOR163', '2025-1', 'MAT118', 'GRUPO035', 'PROF019', 'AULA046', 3, '08:00:00', '09:00:00'),
('HOR164', '2025-1', 'MAT119', 'GRUPO035', 'PROF087', 'AULA046', 4, '11:00:00', '12:00:00'),
('HOR165', '2025-1', 'MAT004', 'GRUPO035', 'PROF017', 'AULA046', 0, '13:00:00', '14:00:00')
ON CONFLICT (id_horario_clase) DO NOTHING;

-- =====================================================
-- HORARIOS PARA PERIODO 2026-1 (Enero-Junio 2026)
-- =====================================================
-- Duplicamos los horarios del periodo 2025-1 pero con periodo 2026-1
-- para que funcionen con fechas de enero 2026
-- =====================================================
INSERT INTO horarios_regulares_de_clase (id_horario_clase, id_periodo, id_materia, id_grupo, id_profesor, id_aula, dia_semana, hora_inicio, hora_fin) VALUES
-- Ciencias Empresariales - Grupo 104A
('HOR201', '2026-1', 'MAT001', 'GRUPO001', 'PROF001', 'AULA001', 1, '08:00:00', '09:00:00'),
('HOR202', '2026-1', 'MAT002', 'GRUPO001', 'PROF002', 'AULA002', 2, '17:00:00', '18:00:00'),
('HOR203', '2026-1', 'MAT003', 'GRUPO001', 'PROF003', 'AULA003', 3, '11:00:00', '12:00:00'),
('HOR204', '2026-1', 'MAT004', 'GRUPO001', 'PROF004', 'AULA001', 4, '12:00:00', '13:00:00'),
('HOR205', '2026-1', 'MAT005', 'GRUPO001', 'PROF005', 'AULA004', 0, '08:00:00', '09:00:00'),
-- Grupo 104B
('HOR206', '2026-1', 'MAT001', 'GRUPO002', 'PROF001', 'AULA001', 1, '08:00:00', '09:00:00'),
('HOR207', '2026-1', 'MAT002', 'GRUPO002', 'PROF002', 'AULA002', 2, '17:00:00', '18:00:00'),
('HOR208', '2026-1', 'MAT003', 'GRUPO002', 'PROF006', 'AULA003', 3, '16:00:00', '17:00:00'),
('HOR209', '2026-1', 'MAT004', 'GRUPO002', 'PROF004', 'AULA001', 4, '12:00:00', '13:00:00'),
('HOR210', '2026-1', 'MAT005', 'GRUPO002', 'PROF007', 'AULA005', 0, '08:00:00', '09:00:00'),
-- Grupo 304
('HOR211', '2026-1', 'MAT006', 'GRUPO003', 'PROF004', 'AULA006', 1, '09:00:00', '10:00:00'),
('HOR212', '2026-1', 'MAT007', 'GRUPO003', 'PROF008', 'AULA004', 2, '12:00:00', '13:00:00'),
('HOR213', '2026-1', 'MAT008', 'GRUPO003', 'PROF009', 'AULA006', 3, '17:00:00', '18:00:00'),
('HOR214', '2026-1', 'MAT009', 'GRUPO003', 'PROF010', 'AULA006', 4, '11:00:00', '12:00:00'),
('HOR215', '2026-1', 'MAT010', 'GRUPO003', 'PROF011', 'AULA007', 0, '10:00:00', '11:00:00'),
-- Grupo 504
('HOR216', '2026-1', 'MAT011', 'GRUPO004', 'PROF012', 'AULA003', 1, '09:00:00', '10:00:00'),
('HOR217', '2026-1', 'MAT012', 'GRUPO004', 'PROF008', 'AULA007', 2, '13:00:00', '14:00:00'),
('HOR218', '2026-1', 'MAT013', 'GRUPO004', 'PROF002', 'AULA008', 3, '10:00:00', '11:00:00'),
('HOR219', '2026-1', 'MAT014', 'GRUPO004', 'PROF001', 'AULA007', 4, '11:00:00', '12:00:00'),
('HOR220', '2026-1', 'MAT015', 'GRUPO004', 'PROF013', 'AULA007', 0, '16:00:00', '17:00:00'),
-- Grupo 604
('HOR221', '2026-1', 'MAT016', 'GRUPO005', 'PROF011', 'AULA009', 4, '08:00:00', '09:00:00'),
('HOR222', '2026-1', 'MAT017', 'GRUPO005', 'PROF012', 'AULA010', 0, '11:00:00', '12:00:00'),
-- Grupo 704
('HOR223', '2026-1', 'MAT018', 'GRUPO006', 'PROF014', 'AULA011', 1, '11:00:00', '12:00:00'),
('HOR224', '2026-1', 'MAT019', 'GRUPO006', 'PROF011', 'AULA011', 2, '12:00:00', '13:00:00'),
('HOR225', '2026-1', 'MAT020', 'GRUPO006', 'PROF010', 'AULA011', 3, '16:00:00', '17:00:00'),
('HOR226', '2026-1', 'MAT021', 'GRUPO006', 'PROF015', 'AULA010', 4, '13:00:00', '14:00:00'),
('HOR227', '2026-1', 'MAT022', 'GRUPO006', 'PROF002', 'AULA011', 0, '09:00:00', '10:00:00'),
-- Ciencias Biomédicas - Grupo 107A
('HOR228', '2026-1', 'MAT023', 'GRUPO007', 'PROF016', 'AULA012', 1, '16:00:00', '17:00:00'),
('HOR229', '2026-1', 'MAT004', 'GRUPO007', 'PROF017', 'AULA012', 2, '16:00:00', '17:00:00'),
('HOR230', '2026-1', 'MAT024', 'GRUPO007', 'PROF018', 'AULA013', 3, '10:00:00', '11:00:00'),
('HOR231', '2026-1', 'MAT025', 'GRUPO007', 'PROF019', 'AULA014', 4, '09:00:00', '10:00:00'),
('HOR232', '2026-1', 'MAT026', 'GRUPO007', 'PROF020', 'AULA015', 0, '13:00:00', '14:00:00'),
-- Grupo 107B
('HOR233', '2026-1', 'MAT023', 'GRUPO008', 'PROF021', 'AULA016', 1, '16:00:00', '17:00:00'),
('HOR234', '2026-1', 'MAT004', 'GRUPO008', 'PROF017', 'AULA016', 2, '16:00:00', '17:00:00'),
('HOR235', '2026-1', 'MAT024', 'GRUPO008', 'PROF007', 'AULA001', 3, '10:00:00', '11:00:00'),
('HOR236', '2026-1', 'MAT025', 'GRUPO008', 'PROF019', 'AULA017', 4, '09:00:00', '10:00:00'),
('HOR237', '2026-1', 'MAT026', 'GRUPO008', 'PROF022', 'AULA001', 0, '13:00:00', '14:00:00'),
-- Grupo 307
('HOR238', '2026-1', 'MAT027', 'GRUPO009', 'PROF023', 'AULA013', 1, '17:00:00', '18:00:00'),
('HOR239', '2026-1', 'MAT028', 'GRUPO009', 'PROF024', 'AULA018', 2, '08:00:00', '09:00:00'),
('HOR240', '2026-1', 'MAT029', 'GRUPO009', 'PROF025', 'AULA019', 3, '11:00:00', '12:00:00'),
('HOR241', '2026-1', 'MAT030', 'GRUPO009', 'PROF006', 'AULA020', 4, '10:00:00', '11:00:00'),
('HOR242', '2026-1', 'MAT031', 'GRUPO009', 'PROF026', 'AULA013', 0, '11:00:00', '12:00:00'),
-- Sistemas Computacionales - Grupo 106
('HOR243', '2026-1', 'MAT032', 'GRUPO010', 'PROF027', 'AULA021', 1, '12:00:00', '13:00:00'),
('HOR244', '2026-1', 'MAT033', 'GRUPO010', 'PROF028', 'AULA022', 2, '13:00:00', '14:00:00'),
('HOR245', '2026-1', 'MAT004', 'GRUPO010', 'PROF029', 'AULA023', 3, '16:00:00', '17:00:00'),
('HOR246', '2026-1', 'MAT034', 'GRUPO010', 'PROF030', 'AULA023', 4, '10:00:00', '11:00:00'),
('HOR247', '2026-1', 'MAT035', 'GRUPO010', 'PROF031', 'AULA024', 0, '11:00:00', '12:00:00'),
-- Grupo 306
('HOR248', '2026-1', 'MAT036', 'GRUPO011', 'PROF032', 'AULA025', 1, '13:00:00', '14:00:00'),
('HOR249', '2026-1', 'MAT037', 'GRUPO011', 'PROF007', 'AULA026', 2, '17:00:00', '18:00:00'),
('HOR250', '2026-1', 'MAT038', 'GRUPO011', 'PROF011', 'AULA027', 3, '11:00:00', '12:00:00'),
('HOR251', '2026-1', 'MAT039', 'GRUPO011', 'PROF033', 'AULA025', 4, '09:00:00', '10:00:00'),
('HOR252', '2026-1', 'MAT040', 'GRUPO011', 'PROF031', 'AULA026', 0, '08:00:00', '09:00:00'),
-- Grupo 306 (segundo grupo)
('HOR253', '2026-1', 'MAT036', 'GRUPO012', 'PROF018', 'AULA028', 1, '09:00:00', '10:00:00'),
('HOR254', '2026-1', 'MAT037', 'GRUPO012', 'PROF007', 'AULA026', 2, '17:00:00', '18:00:00'),
('HOR255', '2026-1', 'MAT038', 'GRUPO012', 'PROF011', 'AULA027', 3, '11:00:00', '12:00:00'),
('HOR256', '2026-1', 'MAT039', 'GRUPO012', 'PROF033', 'AULA025', 4, '12:00:00', '13:00:00'),
('HOR257', '2026-1', 'MAT040', 'GRUPO012', 'PROF031', 'AULA026', 0, '08:00:00', '09:00:00'),
-- Grupo 506
('HOR258', '2026-1', 'MAT041', 'GRUPO013', 'PROF027', 'AULA021', 1, '13:00:00', '14:00:00'),
('HOR259', '2026-1', 'MAT042', 'GRUPO013', 'PROF034', 'AULA021', 2, '16:00:00', '17:00:00'),
('HOR260', '2026-1', 'MAT043', 'GRUPO013', 'PROF035', 'AULA021', 3, '09:00:00', '10:00:00'),
('HOR261', '2026-1', 'MAT044', 'GRUPO013', 'PROF029', 'AULA028', 4, '10:00:00', '11:00:00'),
('HOR262', '2026-1', 'MAT045', 'GRUPO013', 'PROF032', 'AULA028', 0, '17:00:00', '18:00:00'),
-- Grupo 706
('HOR263', '2026-1', 'MAT046', 'GRUPO014', 'PROF018', 'AULA028', 1, '08:00:00', '09:00:00'),
('HOR264', '2026-1', 'MAT047', 'GRUPO014', 'PROF032', 'AULA028', 2, '12:00:00', '13:00:00'),
('HOR265', '2026-1', 'MAT048', 'GRUPO014', 'PROF036', 'AULA025', 3, '11:00:00', '12:00:00'),
('HOR266', '2026-1', 'MAT049', 'GRUPO014', 'PROF037', 'AULA026', 4, '09:00:00', '10:00:00'),
('HOR267', '2026-1', 'MAT050', 'GRUPO014', 'PROF038', 'AULA029', 0, '17:00:00', '18:00:00'),
-- Grupo 906
('HOR268', '2026-1', 'MAT051', 'GRUPO015', 'PROF033', 'AULA021', 0, '11:00:00', '12:00:00'),
-- Administración Pública - Grupo 501
('HOR269', '2026-1', 'MAT052', 'GRUPO016', 'PROF039', 'AULA030', 1, '09:00:00', '10:00:00'),
('HOR270', '2026-1', 'MAT053', 'GRUPO016', 'PROF040', 'AULA030', 2, '13:00:00', '14:00:00'),
('HOR271', '2026-1', 'MAT004', 'GRUPO016', 'PROF041', 'AULA030', 3, '16:00:00', '17:00:00'),
('HOR272', '2026-1', 'MAT054', 'GRUPO016', 'PROF042', 'AULA031', 4, '12:00:00', '13:00:00'),
('HOR273', '2026-1', 'MAT055', 'GRUPO016', 'PROF005', 'AULA030', 0, '11:00:00', '12:00:00'),
-- Grupo 701
('HOR274', '2026-1', 'MAT056', 'GRUPO017', 'PROF008', 'AULA010', 1, '09:00:00', '10:00:00'),
('HOR275', '2026-1', 'MAT057', 'GRUPO017', 'PROF045', 'AULA032', 2, '17:00:00', '18:00:00'),
('HOR276', '2026-1', 'MAT058', 'GRUPO017', 'PROF043', 'AULA032', 3, '11:00:00', '12:00:00'),
('HOR277', '2026-1', 'MAT059', 'GRUPO017', 'PROF042', 'AULA010', 4, '08:00:00', '09:00:00'),
('HOR278', '2026-1', 'MAT060', 'GRUPO017', 'PROF044', 'AULA032', 0, '12:00:00', '13:00:00'),
-- Grupo 705
('HOR279', '2026-1', 'MAT061', 'GRUPO018', 'PROF046', 'AULA033', 1, '16:00:00', '17:00:00'),
('HOR280', '2026-1', 'MAT060', 'GRUPO018', 'PROF044', 'AULA031', 2, '17:00:00', '18:00:00'),
('HOR281', '2026-1', 'MAT062', 'GRUPO018', 'PROF042', 'AULA034', 3, '09:00:00', '10:00:00'),
('HOR282', '2026-1', 'MAT063', 'GRUPO018', 'PROF012', 'AULA035', 4, '12:00:00', '13:00:00'),
('HOR283', '2026-1', 'MAT015', 'GRUPO018', 'PROF045', 'AULA034', 0, '10:00:00', '11:00:00'),
-- Grupo 905
('HOR284', '2026-1', 'MAT064', 'GRUPO019', 'PROF047', 'AULA036', 3, '11:00:00', '12:00:00'),
('HOR285', '2026-1', 'MAT065', 'GRUPO019', 'PROF040', 'AULA010', 4, '12:00:00', '13:00:00'),
('HOR286', '2026-1', 'MAT066', 'GRUPO019', 'PROF039', 'AULA036', 0, '16:00:00', '17:00:00'),
-- Grupo 905 (segundo grupo)
('HOR287', '2026-1', 'MAT067', 'GRUPO020', 'PROF048', 'AULA036', 1, '10:00:00', '11:00:00'),
('HOR288', '2026-1', 'MAT068', 'GRUPO020', 'PROF049', 'AULA037', 2, '17:00:00', '18:00:00'),
('HOR289', '2026-1', 'MAT069', 'GRUPO020', 'PROF017', 'AULA010', 3, '16:00:00', '17:00:00'),
('HOR290', '2026-1', 'MAT070', 'GRUPO020', 'PROF050', 'AULA036', 4, '09:00:00', '10:00:00'),
('HOR291', '2026-1', 'MAT071', 'GRUPO020', 'PROF051', 'AULA035', 0, '13:00:00', '14:00:00'),
-- Administración Municipal - Grupo 501
('HOR292', '2026-1', 'MAT072', 'GRUPO021', 'PROF041', 'AULA034', 1, '11:00:00', '12:00:00'),
('HOR293', '2026-1', 'MAT073', 'GRUPO021', 'PROF052', 'AULA034', 2, '16:00:00', '17:00:00'),
('HOR294', '2026-1', 'MAT074', 'GRUPO021', 'PROF053', 'AULA010', 3, '17:00:00', '18:00:00'),
('HOR295', '2026-1', 'MAT075', 'GRUPO021', 'PROF054', 'AULA034', 4, '08:00:00', '09:00:00'),
('HOR296', '2026-1', 'MAT015', 'GRUPO021', 'PROF045', 'AULA034', 0, '10:00:00', '11:00:00'),
-- Grupo 701
('HOR297', '2026-1', 'MAT076', 'GRUPO022', 'PROF055', 'AULA033', 1, '12:00:00', '13:00:00'),
('HOR298', '2026-1', 'MAT077', 'GRUPO022', 'PROF056', 'AULA033', 2, '17:00:00', '18:00:00'),
('HOR299', '2026-1', 'MAT078', 'GRUPO022', 'PROF053', 'AULA033', 3, '11:00:00', '12:00:00'),
('HOR300', '2026-1', 'MAT079', 'GRUPO022', 'PROF045', 'AULA033', 4, '08:00:00', '09:00:00'),
('HOR301', '2026-1', 'MAT080', 'GRUPO022', 'PROF054', 'AULA038', 0, '09:00:00', '10:00:00'),
-- Grupo 901
('HOR302', '2026-1', 'MAT081', 'GRUPO023', 'PROF014', 'AULA006', 1, '10:00:00', '11:00:00'),
('HOR303', '2026-1', 'MAT082', 'GRUPO023', 'PROF049', 'AULA035', 2, '08:00:00', '09:00:00'),
('HOR304', '2026-1', 'MAT083', 'GRUPO023', 'PROF053', 'AULA006', 3, '16:00:00', '17:00:00'),
('HOR305', '2026-1', 'MAT084', 'GRUPO023', 'PROF057', 'AULA006', 4, '12:00:00', '13:00:00'),
('HOR306', '2026-1', 'MAT071', 'GRUPO023', 'PROF051', 'AULA035', 0, '13:00:00', '14:00:00'),
-- Nutrición - Grupo 107A
('HOR307', '2026-1', 'MAT085', 'GRUPO024', 'PROF058', 'AULA039', 1, '11:00:00', '12:00:00'),
('HOR308', '2026-1', 'MAT086', 'GRUPO024', 'PROF059', 'AULA039', 2, '08:00:00', '09:00:00'),
('HOR309', '2026-1', 'MAT087', 'GRUPO024', 'PROF060', 'AULA039', 3, '09:00:00', '10:00:00'),
('HOR310', '2026-1', 'MAT088', 'GRUPO024', 'PROF061', 'AULA040', 4, '12:00:00', '13:00:00'),
('HOR311', '2026-1', 'MAT004', 'GRUPO024', 'PROF062', 'AULA039', 0, '16:00:00', '17:00:00'),
-- Grupo 107B
('HOR312', '2026-1', 'MAT085', 'GRUPO025', 'PROF058', 'AULA041', 1, '11:00:00', '12:00:00'),
('HOR313', '2026-1', 'MAT086', 'GRUPO025', 'PROF059', 'AULA041', 2, '08:00:00', '09:00:00'),
('HOR314', '2026-1', 'MAT087', 'GRUPO025', 'PROF060', 'AULA041', 3, '09:00:00', '10:00:00'),
('HOR315', '2026-1', 'MAT088', 'GRUPO025', 'PROF061', 'AULA040', 4, '12:00:00', '13:00:00'),
('HOR316', '2026-1', 'MAT004', 'GRUPO025', 'PROF062', 'AULA041', 0, '16:00:00', '17:00:00'),
-- Grupo 307
('HOR317', '2026-1', 'MAT089', 'GRUPO026', 'PROF063', 'AULA019', 1, '09:00:00', '10:00:00'),
('HOR318', '2026-1', 'MAT090', 'GRUPO026', 'PROF064', 'AULA019', 2, '12:00:00', '13:00:00'),
('HOR319', '2026-1', 'MAT091', 'GRUPO026', 'PROF065', 'AULA019', 3, '16:00:00', '17:00:00'),
('HOR320', '2026-1', 'MAT092', 'GRUPO026', 'PROF021', 'AULA019', 4, '08:00:00', '09:00:00'),
('HOR321', '2026-1', 'MAT093', 'GRUPO026', 'PROF060', 'AULA019', 0, '10:00:00', '11:00:00'),
-- Grupo 507
('HOR322', '2026-1', 'MAT094', 'GRUPO027', 'PROF066', 'AULA042', 1, '13:00:00', '14:00:00'),
('HOR323', '2026-1', 'MAT095', 'GRUPO027', 'PROF067', 'AULA043', 2, '16:00:00', '17:00:00'),
('HOR324', '2026-1', 'MAT096', 'GRUPO027', 'PROF068', 'AULA043', 3, '12:00:00', '13:00:00'),
('HOR325', '2026-1', 'MAT097', 'GRUPO027', 'PROF069', 'AULA042', 4, '17:00:00', '18:00:00'),
('HOR326', '2026-1', 'MAT098', 'GRUPO027', 'PROF070', 'AULA042', 0, '08:00:00', '09:00:00'),
-- Grupo 707
('HOR327', '2026-1', 'MAT099', 'GRUPO028', 'PROF059', 'AULA044', 2, '10:00:00', '11:00:00'),
('HOR328', '2026-1', 'MAT100', 'GRUPO028', 'PROF061', 'AULA044', 3, '08:00:00', '09:00:00'),
('HOR329', '2026-1', 'MAT101', 'GRUPO028', 'PROF071', 'AULA044', 4, '11:00:00', '12:00:00'),
('HOR330', '2026-1', 'MAT102', 'GRUPO028', 'PROF068', 'AULA044', 0, '16:00:00', '17:00:00'),
-- Grupo 907
('HOR331', '2026-1', 'MAT103', 'GRUPO029', 'PROF072', 'AULA039', 1, '13:00:00', '14:00:00'),
('HOR332', '2026-1', 'MAT104', 'GRUPO029', 'PROF073', 'AULA045', 2, '09:00:00', '10:00:00'),
('HOR333', '2026-1', 'MAT105', 'GRUPO029', 'PROF070', 'AULA045', 3, '12:00:00', '13:00:00'),
('HOR334', '2026-1', 'MAT106', 'GRUPO029', 'PROF067', 'AULA039', 4, '17:00:00', '18:00:00'),
('HOR335', '2026-1', 'MAT107', 'GRUPO029', 'PROF061', 'AULA039', 0, '08:00:00', '09:00:00'),
-- Odontología - Grupo 913A
('HOR336', '2026-1', 'MAT108', 'GRUPO030', 'PROF074', 'AULA022', 1, '10:00:00', '11:00:00'),
('HOR337', '2026-1', 'MAT109', 'GRUPO030', 'PROF075', 'AULA022', 2, '09:00:00', '10:00:00'),
('HOR338', '2026-1', 'MAT110', 'GRUPO030', 'PROF076', 'AULA022', 3, '12:00:00', '13:00:00'),
('HOR339', '2026-1', 'MAT111', 'GRUPO030', 'PROF077', 'AULA022', 4, '17:00:00', '18:00:00'),
('HOR340', '2026-1', 'MAT112', 'GRUPO030', 'PROF078', 'AULA022', 0, '11:00:00', '12:00:00'),
-- Grupo 913B
('HOR341', '2026-1', 'MAT108', 'GRUPO031', 'PROF074', 'AULA027', 1, '10:00:00', '11:00:00'),
('HOR342', '2026-1', 'MAT109', 'GRUPO031', 'PROF075', 'AULA027', 2, '09:00:00', '10:00:00'),
('HOR343', '2026-1', 'MAT110', 'GRUPO031', 'PROF079', 'AULA019', 3, '12:00:00', '13:00:00'),
('HOR344', '2026-1', 'MAT111', 'GRUPO031', 'PROF077', 'AULA027', 4, '17:00:00', '18:00:00'),
('HOR345', '2026-1', 'MAT112', 'GRUPO031', 'PROF078', 'AULA019', 0, '11:00:00', '12:00:00'),
-- Grupo 913C
('HOR346', '2026-1', 'MAT108', 'GRUPO032', 'PROF074', 'AULA044', 1, '10:00:00', '11:00:00'),
('HOR347', '2026-1', 'MAT109', 'GRUPO032', 'PROF075', 'AULA044', 2, '09:00:00', '10:00:00'),
('HOR348', '2026-1', 'MAT110', 'GRUPO032', 'PROF079', 'AULA044', 3, '12:00:00', '13:00:00'),
('HOR349', '2026-1', 'MAT111', 'GRUPO032', 'PROF077', 'AULA044', 4, '17:00:00', '18:00:00'),
('HOR350', '2026-1', 'MAT112', 'GRUPO032', 'PROF078', 'AULA044', 0, '11:00:00', '12:00:00'),
-- Enfermería - Grupo 103-A
('HOR351', '2026-1', 'MAT113', 'GRUPO033', 'PROF080', 'AULA048', 1, '09:00:00', '10:00:00'),
('HOR352', '2026-1', 'MAT114', 'GRUPO033', 'PROF063', 'AULA001', 2, '17:00:00', '18:00:00'),
('HOR353', '2026-1', 'MAT115', 'GRUPO033', 'PROF081', 'AULA048', 3, '08:00:00', '09:00:00'),
('HOR354', '2026-1', 'MAT116', 'GRUPO033', 'PROF082', 'AULA048', 4, '11:00:00', '12:00:00'),
-- Grupo 103-B
('HOR355', '2026-1', 'MAT113', 'GRUPO034', 'PROF080', 'AULA050', 1, '09:00:00', '10:00:00'),
('HOR356', '2026-1', 'MAT114', 'GRUPO034', 'PROF063', 'AULA001', 2, '17:00:00', '18:00:00'),
('HOR357', '2026-1', 'MAT115', 'GRUPO034', 'PROF081', 'AULA050', 3, '08:00:00', '09:00:00'),
('HOR358', '2026-1', 'MAT116', 'GRUPO034', 'PROF082', 'AULA050', 4, '11:00:00', '12:00:00'),
-- Medicina - Grupo 114A
('HOR359', '2026-1', 'MAT117', 'GRUPO035', 'PROF083', 'AULA046', 1, '09:00:00', '10:00:00'),
('HOR360', '2026-1', 'MAT118', 'GRUPO035', 'PROF084', 'AULA046', 2, '10:00:00', '11:00:00'),
('HOR361', '2026-1', 'MAT119', 'GRUPO035', 'PROF085', 'AULA046', 3, '11:00:00', '12:00:00'),
('HOR362', '2026-1', 'MAT115', 'GRUPO035', 'PROF085', 'AULA046', 1, '16:00:00', '17:00:00'),
('HOR363', '2026-1', 'MAT117', 'GRUPO035', 'PROF086', 'AULA046', 2, '09:00:00', '10:00:00'),
('HOR364', '2026-1', 'MAT118', 'GRUPO035', 'PROF019', 'AULA046', 3, '08:00:00', '09:00:00'),
('HOR365', '2026-1', 'MAT119', 'GRUPO035', 'PROF087', 'AULA046', 4, '11:00:00', '12:00:00'),
('HOR366', '2026-1', 'MAT004', 'GRUPO035', 'PROF017', 'AULA046', 0, '13:00:00', '14:00:00')
ON CONFLICT (id_horario_clase) DO NOTHING;

-- =====================================================
-- 11. PERMISOS SINODALES POR MATERIA
-- =====================================================
-- Crear permisos para que los profesores puedan ser sinodales de sus materias
-- (Se pueden agregar más según sea necesario)
INSERT INTO permisos_sinodales_por_materia (id_regla, id_profesor, id_materia) VALUES
-- Ciencias Empresariales
('PERM014', 'PROF001', 'MAT001'),
('PERM015', 'PROF002', 'MAT002'),
('PERM016', 'PROF003', 'MAT003'),
('PERM017', 'PROF004', 'MAT004'),
('PERM018', 'PROF005', 'MAT005'),
('PERM019', 'PROF006', 'MAT003'),
('PERM020', 'PROF007', 'MAT005'),
('PERM021', 'PROF008', 'MAT007'),
('PERM022', 'PROF009', 'MAT008'),
('PERM023', 'PROF010', 'MAT009'),
('PERM024', 'PROF011', 'MAT010'),
('PERM025', 'PROF012', 'MAT011'),
('PERM026', 'PROF013', 'MAT015'),
('PERM027', 'PROF014', 'MAT018'),
('PERM028', 'PROF015', 'MAT021'),
-- Ciencias Biomédicas
('PERM029', 'PROF016', 'MAT023'),
('PERM030', 'PROF017', 'MAT004'),
('PERM031', 'PROF018', 'MAT024'),
('PERM032', 'PROF019', 'MAT025'),
('PERM033', 'PROF020', 'MAT026'),
('PERM034', 'PROF021', 'MAT023'),
('PERM035', 'PROF022', 'MAT026'),
('PERM036', 'PROF023', 'MAT027'),
('PERM037', 'PROF024', 'MAT028'),
('PERM038', 'PROF025', 'MAT029'),
('PERM039', 'PROF006', 'MAT030'),
('PERM040', 'PROF026', 'MAT031'),
-- Sistemas Computacionales
('PERM041', 'PROF027', 'MAT032'),
('PERM042', 'PROF028', 'MAT033'),
('PERM043', 'PROF029', 'MAT004'),
('PERM044', 'PROF030', 'MAT034'),
('PERM045', 'PROF031', 'MAT035'),
('PERM046', 'PROF032', 'MAT036'),
('PERM047', 'PROF007', 'MAT037'),
('PERM048', 'PROF011', 'MAT038'),
('PERM049', 'PROF033', 'MAT039'),
('PERM050', 'PROF034', 'MAT042'),
('PERM051', 'PROF035', 'MAT043'),
('PERM052', 'PROF018', 'MAT046'),
('PERM053', 'PROF036', 'MAT048'),
('PERM054', 'PROF037', 'MAT049'),
('PERM055', 'PROF038', 'MAT050'),
-- Administración Pública
('PERM056', 'PROF039', 'MAT052'),
('PERM057', 'PROF040', 'MAT053'),
('PERM058', 'PROF041', 'MAT004'),
('PERM059', 'PROF042', 'MAT054'),
('PERM060', 'PROF005', 'MAT055'),
('PERM061', 'PROF008', 'MAT056'),
('PERM062', 'PROF045', 'MAT057'),
('PERM063', 'PROF043', 'MAT058'),
('PERM064', 'PROF044', 'MAT060'),
('PERM065', 'PROF046', 'MAT061'),
('PERM066', 'PROF012', 'MAT063'),
('PERM067', 'PROF047', 'MAT064'),
('PERM068', 'PROF048', 'MAT067'),
('PERM069', 'PROF049', 'MAT068'),
('PERM070', 'PROF017', 'MAT069'),
('PERM071', 'PROF050', 'MAT070'),
('PERM072', 'PROF051', 'MAT071'),
-- Administración Municipal
('PERM073', 'PROF041', 'MAT072'),
('PERM074', 'PROF052', 'MAT073'),
('PERM075', 'PROF053', 'MAT074'),
('PERM076', 'PROF054', 'MAT075'),
('PERM077', 'PROF055', 'MAT076'),
('PERM078', 'PROF056', 'MAT077'),
('PERM079', 'PROF014', 'MAT081'),
('PERM080', 'PROF057', 'MAT084'),
-- Nutrición
('PERM081', 'PROF058', 'MAT085'),
('PERM082', 'PROF059', 'MAT086'),
('PERM083', 'PROF060', 'MAT087'),
('PERM084', 'PROF061', 'MAT088'),
('PERM085', 'PROF062', 'MAT004'),
('PERM086', 'PROF063', 'MAT089'),
('PERM087', 'PROF064', 'MAT090'),
('PERM088', 'PROF065', 'MAT091'),
('PERM089', 'PROF021', 'MAT092'),
('PERM090', 'PROF066', 'MAT094'),
('PERM091', 'PROF067', 'MAT095'),
('PERM092', 'PROF068', 'MAT096'),
('PERM093', 'PROF069', 'MAT097'),
('PERM094', 'PROF070', 'MAT098'),
('PERM095', 'PROF071', 'MAT101'),
('PERM096', 'PROF072', 'MAT103'),
('PERM097', 'PROF073', 'MAT104'),
-- Odontología
('PERM098', 'PROF074', 'MAT108'),
('PERM099', 'PROF075', 'MAT109'),
('PERM100', 'PROF076', 'MAT110'),
('PERM101', 'PROF077', 'MAT111'),
('PERM102', 'PROF078', 'MAT112'),
('PERM103', 'PROF079', 'MAT110'),
-- Enfermería
('PERM104', 'PROF080', 'MAT113'),
('PERM105', 'PROF063', 'MAT114'),
('PERM106', 'PROF036', 'MAT004'),
('PERM107', 'PROF082', 'MAT115'),
('PERM108', 'PROF083', 'MAT116'),
('PERM109', 'PROF081', 'MAT004'),
('PERM110', 'PROF084', 'MAT116'),
-- Medicina
('PERM111', 'PROF085', 'MAT115'),
('PERM112', 'PROF086', 'MAT117'),
('PERM113', 'PROF019', 'MAT118'),
('PERM114', 'PROF087', 'MAT119'),
('PERM115', 'PROF017', 'MAT004')
ON CONFLICT (id_regla) DO NOTHING;

-- =====================================================
-- VERIFICAR DATOS INSERTADOS
-- =====================================================
-- SELECT 'Carreras' as tabla, COUNT(*) as total FROM carreras
-- UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuarios
-- UNION ALL SELECT 'Profesores', COUNT(*) FROM profesores
-- UNION ALL SELECT 'Periodos', COUNT(*) FROM periodos_academicos
-- UNION ALL SELECT 'Materias', COUNT(*) FROM materias
-- UNION ALL SELECT 'Evaluaciones', COUNT(*) FROM tipos_de_evaluacion
-- UNION ALL SELECT 'Aulas', COUNT(*) FROM aulas
-- UNION ALL SELECT 'Grupos', COUNT(*) FROM grupos_escolares
-- UNION ALL SELECT 'Ventanas', COUNT(*) FROM ventanas_de_aplicacion_por_periodo
-- UNION ALL SELECT 'Horarios', COUNT(*) FROM horarios_regulares_de_clase
-- UNION ALL SELECT 'Permisos', COUNT(*) FROM permisos_sinodales_por_materia;

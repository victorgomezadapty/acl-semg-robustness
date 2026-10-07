# Literatura y decisiones metodológicas

Fecha de búsqueda: **2026-10-04**. Revisión dirigida para este portfolio; no es una revisión sistemática ni garantiza exhaustividad. Prioridad: trabajos 2023–2026, referencias metodológicas necesarias y publicaciones que reutilicen el DOI del dataset. Se consultaron páginas editoriales, PubMed, PMC y el repositorio original. Se distingue lectura del texto completo de lectura del resumen. No se han descargado ni redistribuido PDFs.

## Registro reproducible de búsqueda

Consultas: `"66t1g1k4j"`; `Gutierrez Hart Boukhechba ACL electromyography`; `2024 2025 ACL reconstruction return sport quadriceps strength limb symmetry`; `ACL reconstruction surface electromyography 2025 2026`; `Aspetar clinical practice guideline ACL reconstruction 2023`; `CEDE amplitude normalization matrix`.

Criterios de selección: relación con sEMG/activación, interpretación de simetría, fuerza y RTS; publicación científica o consenso metodológico; enlace editorial o registro bibliográfico verificable. Se omitieron fuentes comerciales, redes sociales y recomendaciones sin artículo científico. Publicación reciente no implica datos recientes o mayor calidad. No se hizo búsqueda formal de retractaciones ni evaluación completa de riesgo de sesgo.

## Lecturas prioritarias

### 1. Khafagy y Hamza — mismo dataset, 2026

**Velocity-dependent quadriceps neuromuscular activation asymmetry after anterior cruciate ligament reconstruction: A pilot secondary analysis of a public electromyographic dataset.** J Musculoskelet Surg Res. 2026;10:429–435. Publicación: 2026-07-01; online: 2026-05-26. [DOI y artículo](https://doi.org/10.25259/JMSR_129_2026). Texto completo consultado.

Análisis secundario del mismo DOI y 22 participantes. Usa pico, RMS y cocientes entre miembros; denomina las condiciones 90/180°/s. Aporta una referencia directa para comparar decisiones analíticas, pero no una muestra independiente. No documenta suficientemente la implementación del procesamiento, normalización, identificación de ciclos o manejo del reloj para reproducirla desde el texto consultado. El README describe procesamiento Delsys; por ello no adoptamos automáticamente la etiqueta «raw» del artículo. Las unidades/escala de la tabla necesitan aclaración antes de comparar valores. Sus resultados y propuestas clínicas no se transfieren al portfolio sin reproducción verificable.

**Decisión:** citar como antecedente; registrar grados/s como interpretación de esta publicación, manteniendo la limitación de la documentación original. No copiar umbrales ni asumir validación clínica del cociente sEMG.

### 2. Scott et al. — activación voluntaria y fuerza, 2026

**Deficits in quadriceps voluntary activation following anterior cruciate ligament reconstruction do not improve over time despite increases in quadriceps strength: A systematic review with meta-regression analyses of temporal trends.** J Sport Health Sci. Online 2026-07-22. [DOI](https://doi.org/10.1016/j.jshs.2026.101160) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/42486364/). Resumen consultado.

Incluye 50 estudios y 1.772 participantes; búsqueda hasta marzo de 2025. Describe trayectorias diferentes de fuerza y activación voluntaria; certeza muy baja. La activación evaluada mediante técnicas de estimulación no equivale a amplitud sEMG superficial.

**Decisión:** mantener separadas fuerza, amplitud sEMG y activación voluntaria; no diagnosticar inhibición artrogénica mediante nuestro canal VL aislado.

### 3. Wu et al. — sEMG y tarea, 2025

**Surface Electromyography and Gait Features in Patients after Anterior Cruciate Ligament Reconstruction.** Orthopaedic Surgery. [Texto editorial/DOI](https://doi.org/10.1111/os.14256). Resumen y secciones metodológicas disponibles consultados.

Estudia 41 adultos agrupados por intervalo postoperatorio; compara sEMG/RMS normalizado y marcha en tareas diferentes. El comportamiento depende de músculo y tarea. Grupos temporales distintos no representan automáticamente seguimiento longitudinal de los mismos sujetos.

**Decisión:** una señal de extensión isocinética de VL no representa carrera, aterrizaje ni todos los músculos. Nuestro dataset carece de tiempo postoperatorio y referencia de normalización documentada; no replicar esa estratificación.

### 4. Girdwood et al. — fuerza y referencia contralateral, 2025

**Tale of quadriceps and hamstring muscle strength after ACL reconstruction: a systematic review with longitudinal and multivariate meta-analysis.** Br J Sports Med. 2025;59:423–434 (registro online en 2024). [DOI](https://doi.org/10.1136/bjsports-2023-107977) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/39389762/). Resumen consultado.

232 estudios, 34.220 participantes; búsqueda hasta febrero de 2023. Las comparaciones con el miembro contralateral y con controles ofrecen referencias diferentes de déficit de fuerza.

**Decisión:** si posteriormente obtenemos torque, mostrar valores absolutos y controles junto con simetría. Este artículo no permite reconstruir torque a partir de sEMG.

### 5. Pronóstico de RTS — revisión 2025

**Return to sport after anterior cruciate ligament reconstruction – prognostic factors and prognostic models: A systematic review.** Ann Phys Rehabil Med. 2025;68:101921. [DOI](https://doi.org/10.1016/j.rehab.2024.101921) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/39892026/). Resumen editorial consultado; autores pendientes de completar en una revisión bibliográfica posterior.

Identifica factores físicos y psicológicos con certeza muy baja. La evidencia pronóstica no justifica un criterio aislado de clearance.

**Decisión:** no convertir nuestras métricas descriptivas en predicciones de RTS; carecemos de outcomes y variables contextuales necesarios.

### 6. Kotsifaki et al. — guía Aspetar, 2023

**Aspetar clinical practice guideline on rehabilitation after anterior cruciate ligament reconstruction.** Br J Sports Med. 2023;57:500–514. [DOI](https://doi.org/10.1136/bjsports-2022-106158) · [Texto completo PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11785408/). Resumen y secciones clínicas consultados.

Guía con GRADE y consenso experto; señala incertidumbre en criterios de progresión/alta y certeza baja para muchos componentes. Ofrece un marco clínico que incluye más dimensiones que una medida de simetría.

**Decisión:** conservar el carácter multidimensional del perfil; no presentar nuestros gráficos como herramienta validada de alta deportiva.

### 7. Besomi et al. — normalización sEMG, 2020

**Consensus for experimental design in electromyography (CEDE) project: Amplitude normalization matrix.** J Electromyogr Kinesiol. 2020;53:102438. [DOI](https://doi.org/10.1016/j.jelekin.2020.102438) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/32569878/). Resumen consultado. Referencia anterior al dataset, incluida por pertinencia metodológica.

Presenta opciones de normalización para preguntas y contextos diferentes, incluida la amplitud sin normalizar.

**Decisión:** conservar voltios originales y no inventar referencia MVC. Normalizar cada señal a su propio máximo puede borrar diferencias de amplitud que se desea estudiar; no se implementa por defecto.

## Qué cambia en el proyecto

### Actualización: publicación de los autores originales localizada

Gutierrez, Hart, Barnes y Boukhechba. **Using Inertial Measurement Units (IMU) and Comparative Trajectory Analysis for Modeling Micro-Level Human Motion Dysfunction.** Human Factors and Wearable Technologies. 2022;29:29–35. [DOI](https://doi.org/10.54941/ahfe1001471) · [PDF editorial](https://openaccess-api.cms-conferences.org/articles/download/978-1-958651-05-6_3). Se consultó el texto, especialmente Study Design. Describe un estudio más amplio de 11 pacientes y 10 controles, Delsys Trigno/Biodex y dos momentos de evaluación. No establece la correspondencia de visitas/IDs con los 12 pacientes del ZIP, ni resuelve la configuración de muestreo y filtrado de esta exportación. Se incorpora como contexto de adquisición, sin inventar metadatos por participante.

La literatura nueva aporta contexto y un antecedente directo de reutilización, pero no resuelve la ausencia de torque, IMU o metadatos clínicos. La inspección precede a los features. RMS y media absoluta de toda la grabación se permiten en QA, etiquetadas como magnitud del registro completo; no como activación normalizada ni ciclo identificado. No se filtra, reconstruye tiempo o excluyen sujetos sin justificación.

## Para futuras revisiones

### Antecedente metodológico de la auditoría de sensibilidad (2026-10-06)

Simonsohn, Simmons y Nelson (2020), [Specification curve analysis](https://doi.org/10.1038/s41562-020-0912-z), Nature Human Behaviour 4:1208–1214. La evaluación de distintas decisiones analíticas tiene antecedentes establecidos; no reivindicamos su invención. Se localizó la fuente primaria mediante búsqueda dirigida. Nuestro producto es una matriz descriptiva de resúmenes sEMG, no la implementación completa de su procedimiento inferencial. La búsqueda específica no demuestra ausencia de trabajos previos en sEMG ni prioridad científica de este caso.

Repetir las consultas y registrar fecha, ventana temporal y cambios en `literature_search_log.csv`. Revisar especialmente nuevas citas al DOI; erratas del artículo de reutilización; información original del dispositivo, muestreo, ciclos y control de amplitud. Antes de adoptar métodos, leer texto completo y suplementos. Añadir bibliografía nueva como registros independientes; no sustituir silenciosamente esta revisión.

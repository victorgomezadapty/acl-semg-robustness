# Extensión propuesta y búsqueda de datos complementarios

Fecha de revisión: 2026-10-06. Búsqueda dirigida, no revisión sistemática. No se descargaron ni analizaron nuevos datos todavía.

**Actualización posterior:** se descargaron y verificaron los archivos del candidato de sinergias y de un segundo depósito ACLR. La evaluación directa de archivos no permite validación del protocolo actual; ver [factibilidad externa](external_validation_feasibility.md). La tabla siguiente conserva las hipótesis iniciales de selección y no sustituye esa auditoría. ACL-RSI no apareció como columna independiente en los archivos inspeccionados.

## Pregunta prioritaria

¿Se relaciona la asimetría neuromuscular con medidas funcionales o clínicas observadas en las mismas personas? La primera extensión propuesta es una cohorte separada de sEMG multimuscular con covariables clínicas. Esto agrega contexto medido sin inventar fuerza para el dataset actual.

| Fuente primaria | Información descrita | Encaje y estado |
|---|---|---|
| [Bilateral lower limb muscle synergy patterns, Scientific Data 2026](https://www.nature.com/articles/s41597-026-07543-2); [depósito Figshare](https://doi.org/10.6084/m9.figshare.30928694) | 17 pacientes, sEMG bilateral de ocho músculos durante marcha, sinergias, edad, ACL-RSI y variables de marcha; licencia CC BY 4.0 según descriptor | Candidato prioritario para asociar características musculares con contexto clínico. Descriptor localizado mediante búsqueda; apertura directa falló. Archivos, diccionario y granularidad de ACL-RSI pendientes de inspección. No contiene fuerza de cuádriceps confirmada. |
| [Jump-landings under fatigue, Scientific Data 2025](https://www.nature.com/articles/s41597-025-05934-5) | 43 personas, captura 3D y fuerzas de reacción del suelo, seis tareas antes/después de fatiga y cuestionarios; 21 con lesión previa, de los cuales 19 reconstruidos y dos tratados conservadoramente | Descriptor leído. Alternativa para biomecánica funcional; separar reconstruidos de tratados conservadoramente. Fuerza de reacción del suelo no equivale a fuerza muscular isocinética. No es seguimiento longitudinal de recuperación. |
| [Raw ACL Data.xlsx, Figshare](https://figshare.com/articles/dataset/Raw_ACL_Data_xlsx/16620421) | Archivo candidato localizado por título | Acceso al registro devolvió 403. Variables, licencia y estudio asociado no confirmados; no seleccionado por ahora. |

## Protocolo concreto de la próxima etapa

1. Inspeccionar metadatos, licencia y archivos del candidato de sEMG/ACL-RSI; verificar que las covariables clínicas tienen una fila por persona y se pueden vincular a las señales.
2. Crear una carpeta y diccionario independientes. Verificar unidades, frecuencia, fases de marcha, normalización, covariables y valores ausentes antes de definir métricas.
3. Si la vinculación individual existe, fijar una única asociación exploratoria principal: balance bilateral de una característica muscular documentada frente a ACL-RSI. Conservar datos individuales e intervalos; no entrenar un predictor con 17 personas. ACL-RSI es preparación psicológica autoinformada, no retorno deportivo observado.
4. Si no existe vinculación, limitarse a reproducir descriptivos y sinergias; registrar que la pregunta clínica sigue abierta. No fabricar correspondencias ni combinar IDs entre cohortes.

## Ruta de fuerza y seguimiento real

Para estudiar fuerza–sEMG hace falta torque en Nm de las mismas personas, miembro identificado, protocolo/velocidad, masa para Nm/kg y medición sincronizada o de la misma visita. Para recuperación hacen falta fechas o meses postoperatorios, visitas repetidas y desenlaces observados. Ninguna fuente seleccionada en esta búsqueda está confirmada como suficiente para ambas preguntas.

Solicitar esos campos a un estudio o colaboración sería una ruta posterior; no se contactó a nadie. Datos de cohortes distintas pueden formar dos casos comparables de portfolio, pero no completan retrospectivamente a los 22 participantes actuales.

## Criterio de éxito

Una segunda cohorte auditada, una pregunta predefinida, una tabla por participante, un análisis reproducible y una conclusión ajustada a las mediciones. Esta propuesta es una extensión transversal con covariables clínicas; el seguimiento longitudinal permanece como objetivo separado.

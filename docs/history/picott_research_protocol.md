# PICOTT y protocolo de investigación de métodos

Versión 1 · 2026-10-06 · Estado: protocolo de validación propuesto, no ensayo clínico ni revisión sistemática completa.

Se aplicó el skill picott-builder proporcionado por el usuario (archivo local picott-builder.skill), incluyendo su checklist. La población, el enfoque y el contexto ya estaban definidos en la conversación; no se repitió la entrevista. Se adaptó I a «método analítico» y T-type a un estudio de medición, porque no se evalúa una intervención terapéutica. No se aplicó el requisito de tres ensayos aleatorizados del pipeline de metaanálisis del skill.

| Componente | Definición |
|---|---|
| P — Población | Personas con reconstrucción unilateral de LCA y registros sEMG bilaterales del vasto lateral en la misma tarea y visita. Edad según cada cohorte; no asumir que la cohorte Dryad es adulta si no se documenta. Controles de Dryad son referencia exploratoria separada. |
| I — Método | Auditoría de especificaciones RMS: registro completo, limitación absoluta p99,5 y selección de bloques de 256/512/1024 muestras con umbrales q20 + f(q90−q20), f=0,1/0,2/0,3. Sin filtrado adicional ni reconstrucción temporal del ZIP Dryad. |
| C — Comparador | Cociente bilateral RMS sobre todo el registro exportado, conservando ambas amplitudes. |
| O — Resultado | **Principal:** rango de log(inv/uninv) entre las 11 especificaciones RMS por persona-tarea. **Secundarios:** máximo cambio absoluto respecto a RMS completo, cambios de dirección, dependencia del denominador y sensibilidad entre RMS/MAV. No son desenlaces clínicos ni estimaciones de fiabilidad test-retest. |
| T — Tiempo | Una visita de medición; si existen sesiones repetidas documentadas, analizarlas por separado con un protocolo adicional. Sin ventana postoperatoria impuesta; registrar la disponible. |
| T — Tipo | Estudio secundario de métodos, retrospectivo en Dryad; evaluación de transportabilidad en otra cohorte independiente, si sus archivos cumplen requisitos. Revisión dirigida de antecedentes para definir el vacío. |

**Pregunta:** En personas con reconstrucción unilateral de LCA, ¿cuánto difiere la interpretación descriptiva de la asimetría bilateral del vasto lateral entre una auditoría de especificaciones RMS y el RMS del registro completo en una visita, y se observa esa dependencia en otra cohorte independiente?

## Elegibilidad para validación directa

Inclusión:

- Cohorte independiente de Dryad con reconstrucción unilateral documentada y acceso permitido a datos desidentificados.
- Señales bilaterales identificables por participante y músculo; unidades/escalado y procesamiento documentados.
- Registros originales o exportaciones con amplitud conservada; suficientes muestras para todas las especificaciones y denominadores positivos.
- Misma tarea/visita para ambos miembros, con muestreo y límites de tarea o ciclos documentados.

Exclusión de la validación directa:

- Solo estadísticas grupales, pesos de sinergias o etiquetas sin correspondencia individual.
- Señales reducidas a un ciclo de 101 puntos y/o normalizadas por máximo propio sin amplitudes originales para recuperar escala.
- Imposibilidad de establecer lado, músculo, unidades o identidad de la cohorte.
- Licencia incompatible o acceso no autorizado.

Una cohorte excluida puede servir para una pregunta distinta sobre forma temporal normalizada, pero no como validación de amplitud conservada. Un cambio de tarea es transportabilidad metodológica, no reproducción del porcentaje de cambios de signo de Dryad.

## Plan previo a inspección de valores externos

Este archivo se redactó antes de descargar/abrir las hojas de datos externos. Ya se habían consultado metadatos y métodos del descriptor. No es un preregistro en un registro público y no elimina sesgo por elegir una fuente conocida. Las decisiones Dryad son retrospectivas; su n=22 no se mezcla con la cohorte externa.

1. Auditar licencia, versión, hashes, hojas, IDs, forma, unidades, valores ausentes, amplitud y muestras. Documentar elegibilidad antes de calcular endpoints.
2. Si cumple: aplicar código de las 11 especificaciones RMS sin optimizar parámetros para el resultado. Reportar todos los participantes elegibles, exclusiones justificadas y variantes indefinidas.
3. Resumir por persona; para múltiples tareas preservar repetición, sin contar tareas o músculos como personas. Intervalos sobre personas, no sobre especificaciones correlacionadas. No habrá test confirmatorio de eficacia ni elección por p-value.
4. Informar resultados negativos o de inelegibilidad. No elegir otra definición de asimetría para salvar la validación.
5. Una revisión experta ciega con referencia independiente y repeticiones reales sería otro estudio para evaluar detección de problemas de calidad. No inventar sensibilidad/especificidad, SEM, MDC, ICC o utilidad clínica con datos que no lo permiten.

## Métodos establecidos y citas

- [Besomi et al., CEDE 2020](https://doi.org/10.1016/j.jelekin.2020.102438): elegir normalización según el objetivo de interpretación.
- [Devaprakash et al., 2016](https://doi.org/10.1016/j.jelekin.2016.10.001): antecedentes de dependencia de interpretación respecto a decisiones sEMG.
- [Simonsohn, Simmons y Nelson, 2020](https://doi.org/10.1038/s41562-020-0912-z): antecedente de evaluación de especificaciones; no se reproduce su procedimiento inferencial completo.
- Datos de desarrollo: [Gutierrez, Hart y Boukhechba, 2022](https://doi.org/10.5061/dryad.66t1g1k4j).

El rango entre especificaciones no es un intervalo de confianza ni identifica la medida fisiológicamente correcta. La limitación p99,5 es una perturbación de sensibilidad; no un criterio validado de eliminación de artefactos.

# Revisión sEMG y tiempo — 2026-10-04

Este paso conserva los originales e implementa acceso reproducible y QA. No es un análisis de recuperación clínica.

## Decisiones implementadas

`src/data/semg.py` verifica el hash del ZIP y entrega registros por participante, condición y miembro. Elimina únicamente celdas vacías terminales; mantiene cada valor sEMG en voltios, índice original y timestamp exportado. Rechaza huecos internos y valores no finitos. `long_rows()` permite consumir filas tidy sin guardar millones de filas duplicadas. Se verificaron 88 registros, 22 IDs y correspondencia de longitudes señal/tiempo.

La primera opción de visualización es el **índice original de muestra**, porque dos relojes contienen timestamps duplicados. La alternativa de reconstruir un tiempo uniforme requeriría una frecuencia confirmada o una hipótesis documentada. No se adoptó esa alternativa ni se eliminaron muestras con timestamps iguales: representan observaciones sEMG distintas.

`scripts/review_signals.py` genera cuatro paneles con todos los participantes y ambas etiquetas de miembro. Para visualizar registros largos utiliza una envolvente min/max por bloque de índices; conserva extremos visibles. Esta reducción es gráfica y no altera los datos del loader. Las escalas verticales son independientes y se indican en el título; no comparar alturas aparentes entre paneles.

También genera un gráfico del reloj de patient1 en ambas condiciones, mostrando el detalle de los escalones alrededor de diez segundos. El patrón es compatible con pérdida de precisión decimal en la exportación, pero su causa no está confirmada. No se calcula una frecuencia de muestreo a partir de la mediana cero.

## Archivos de resultados

- `reports/figures/healthy_iso90_signal_review.png`
- `reports/figures/healthy_iso180_signal_review.png`
- `reports/figures/patient_iso90_signal_review.png`
- `reports/figures/patient_iso180_signal_review.png`
- `reports/figures/patient_involved_time_review.png`
- `reports/signal_quality.csv`: magnitudes, negativos, ceros, secuencias constantes, padding y anomalías temporales por registro.
- `reports/signal_review_summary.json`: resumen reproducible.

RMS = sqrt(mean(x²)) y MAV = mean(abs(x)) se calculan sobre **todo el registro exportado** como QA. No se denominan activación MVC, amplitud por contracción ni resultados clínicos. Incluyen cualquier reposo o transición presente y duraciones diferentes. El pico absoluto es sensible a artefactos. Ceros y repeticiones de valores pueden proceder de cuantización o exportación y no justifican exclusión automática. Ningún registro se excluye.

## Qué sigue pendiente

## Hallazgos de la revisión visual y numérica

Se revisaron los cinco PNG generados. Se observan ráfagas repetidas y tramos de baja amplitud en numerosos registros; no se asignaron automáticamente límites de contracción. healthy8/iso90/uninv tiene una forma y escala distintas a las ráfagas de su registro inv: pico absoluto 8.22461 microvoltios, 14.397% de ceros y 3.848 muestras. Esto lo hace prioritario para comprobar adquisición/tarea; no prueba menor activación fisiológica. healthy1/iso180/uninv y healthy3/iso180/uninv muestran transitorios prominentes que justifican revisar picos antes de usarlos como features. No se diagnosticó artefacto ni saturación porque faltan límites del equipo.

Las 88 señales tienen algún valor negativo. La secuencia más larga de ceros es de 936 muestras; se registra como QA, sin convertirla a duración mientras la frecuencia no esté confirmada. No hubo exclusiones, filtros o reconstrucción temporal. El problema de los timestamps permanece **caracterizado, no resuelto**.

Las señales contienen valores positivos y negativos; esto impide asumir que la exportación sea una envolvente enteramente rectificada, pero no identifica los filtros previos. No se aplican band-pass, notch, rectificación, resampling, ventanas temporales, análisis espectral o segmentación de ciclos. Primero confirmar procesamiento Delsys, frecuencia, límites de tarea/ciclo y normalización. El registro corto healthy8/iso90/uninv permanece visible y conservado; su duración no demuestra por sí sola tarea incompleta.

El [artículo de reutilización de 2026](https://doi.org/10.25259/JMSR_129_2026) ofrece antecedente para RMS/pico, pero no resuelve de manera reproducible el reloj o la segmentación. Sus condiciones se expresan en °/s: se registra como evidencia de la publicación, sin modificar retrospectivamente el significado documentado en el README.

## Reproducir

Desde la raíz, instalar `requirements.txt` y ejecutar `python scripts/review_signals.py`. La revisión bibliográfica está en [literature_review.md](literature_review.md); la auditoría previa en [phase_1_data_understanding.md](phase_1_data_understanding.md).

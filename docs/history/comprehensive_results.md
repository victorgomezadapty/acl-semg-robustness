# Análisis ampliado con el dataset disponible

Fecha: 2026-10-04. Resultados exploratorios reproducibles, sin ML ni etiquetas de alta deportiva.

Se analizaron 88 registros, 44 pares condición-miembro y 22 personas. Se ejecutaron 60 comparaciones y 24 correlaciones, y se generaron 22 perfiles.

## Comparación con la publicación

Estas cifras contrastan cocientes RMS de registro completo con los reportados. No se afirma reproducción exacta.

| Cohorte | Condición | Nuestro promedio ± SD (%) | Publicado ± SD (%) |
|---|---|---|---|
| patient | iso90 | 86.71 ± 31.23 | 90.20 ± 7.90 |
| patient | iso180 | 85.45 ± 36.02 | 87.50 ± 9.80 |
| healthy | iso90 | 328.56 ± 771.13 | 96.80 ± 3.50 |
| healthy | iso180 | 86.13 ± 39.28 | 96.10 ± 4.20 |

En controles iso90, omitir el par corto healthy8 solo como sensibilidad cambia la media a 84.91% y SD a 33.71%. El análisis principal lo conserva. Un cociente con denominador pequeño puede distorsionar la media; por eso se muestran medianas y valores absolutos.

El pico positivo y el absoluto producen cocientes diferentes. Ninguna variante fue elegida para hacer coincidir resultados. Unidades de amplitud, procesamiento y ciclos publicados no permiten una reproducción numérica exacta desde el texto disponible.

Referencia: [Khafagy y Hamza, 2026](https://doi.org/10.25259/JMSR_129_2026), tabla 2.

## Inferencia exploratoria

Tests t con p-Holm <0,05: 0; tests de rangos con p-Holm <0,05: 0. Esto no demuestra equivalencia ni ausencia de diferencias. El pequeño tamaño y la calidad/normalización limitan la evidencia.

Todas las estimaciones, tamaños de efecto e intervalos están en [exploratory_tests.csv](../../reports/exploratory_tests.csv). Los 60 endpoints pertenecen a familias explicitadas en comprehensive_methods.md; no se selecciona un test a partir del p-value. Comparar varias familias sigue siendo exploratorio.

## Sensibilidad y relaciones

Se evaluaron 792 combinaciones registro/bloque/umbral, resumidas en 36 filas cohorte-condición. La selección matemática de amplitud permite estudiar cuánto cambia el cociente al reducir periodos de baja amplitud; no identifica ciclos clínicos ni elimina el problema del registro corto. Los gráficos y todas las variantes permanecen disponibles.

Se incluyen correlaciones por cohorte, condición y miembro. RMS y MAV comparten los mismos datos: no interpretar su asociación como mecanismo clínico. Longitud–RMS es un diagnóstico de posible dependencia de la duración del registro.

## Planificación educativa de muestra

Se calculó tamaño hipotético para dos grupos independientes, alfa 0,05 y potencia 80%, usando efectos supuestos (no estimaciones fiables de este piloto). No incluye multiplicidad, pérdidas ni medidas repetidas.

| Efecto supuesto | Personas por grupo |
|---|---|
| 0.3 | 176 |
| 0.5 | 64 |
| 0.62 | 42 |
| 0.8 | 26 |

## Perfiles y reproducibilidad

El [índice local de perfiles](../../reports/analysis_index.html) permite elegir entre las 22 personas. Cada perfil contiene ambas condiciones, señal exportada, amplitud y referencia descriptiva de controles. No muestra torque, reinjury risk ni puntuación RTS.

Código: scripts/comprehensive_semg.py y scripts/build_analysis_report.py. Validación: scripts/check_statistics.py y check_amplitude.py; conteos y hashes comprobados. [Métodos](comprehensive_methods.md) y [cobertura](analysis_coverage.md) documentan lo implementado y los límites.

Conclusión: el dataset permite análisis completos de magnitud y simetría sEMG exportada. Nuestros resultados no justifican adoptar las conclusiones clínicas publicadas sin más; diferencias de procesamiento y tareas pueden cambiar los resultados. Los puntos pendientes ya no impiden estos análisis, y cualquier extensión posterior parte de estos entregables.
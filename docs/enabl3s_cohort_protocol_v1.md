# ENABL3S: reglas previas para los nueve participantes restantes

Versión 1.0 · 2026-10-08. **Reglas definidas después del piloto AB191 y antes de abrir los resultados de los otros nueve participantes.** No es una preregistración pública ni un protocolo independiente del aprendizaje del piloto. Se conserva el piloto original y su protocolo sin reescribir sus resultados.

## Pregunta y alcance

¿Cuánto depende la razón derecha/izquierda del vasto lateral de las especificaciones RMS, de la duración del bloque y de seleccionar los mismos instantes para ambas piernas durante marcha en llano? Es transporte metodológico en personas sanas; no valida fuerza, retorno al deporte o utilidad clínica en LCA.

Fuente: Hu, Rouse y Hargrove, [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2), CC BY 4.0. El [artículo](https://doi.org/10.3389/frobt.2018.00014) describe etiquetas de actividad y anotaciones de incidencias, y advierte que los archivos postprocesados incluyen ensayos con perturbaciones. Esa documentación justifica revisar etiquetas y notas, pero no establece nuestros márgenes o longitudes mínimas. Parámetros legibles por máquina: [configuración v1](../config/enabl3s_cohort_v1.json).

## Selección y transiciones

1. Analizar los nueve participantes diferentes de AB191 del depósito v2. Verificar tamaño, MD5 y SHA-256 antes de calcular resultados. AB191 queda como desarrollo exploratorio separado, sin mezclarlo con el resumen principal.
2. Usar señales Processed, canales Right_VL/Left_VL y Mode=1, a los 1.000 Hz documentados. No añadir filtrado, centrar, interpolar ni convertir a voltios sin confirmar unidades. Registrar escalado y procesamiento disponibles; si la compatibilidad de escala bilateral no puede establecerse, no interpretar la razón como amplitud fisiológica comparable.
3. Solo son elegibles para el principal ensayos con una fila de metadatos identificada inequívocamente y campo Notes presente y vacío tras quitar espacios. Cualquier nota no vacía, incluso ambigua, excluye el ensayo del principal; una nota ausente también lo excluye. Esto es conservador y puede seleccionar una submuestra. No demuestra que los ensayos sin notas estén libres de artefactos. Se conserva una tabla de todas las exclusiones y de sus textos.
4. Recorrer ensayos por número y tramos por orden temporal. Un tramo es una secuencia contigua de Mode=1 con ambos canales finitos. Cambios de modo, valores no finitos y extremos del archivo delimitan tramos. Nunca unirlos ni rellenar huecos.
5. Recortar **500 ms de cada extremo** del tramo, también si empieza o termina en el archivo o junto a un dato inválido. Es un margen práctico fijado por el equipo, no una garantía de eliminar toda transición mal etiquetada. Exigir **4.096 muestras restantes**: al menos cuatro bloques completos de 1.024. El mínimo reduce el caso de solo dos bloques del piloto; tampoco es un umbral validado de estabilidad.
6. Seleccionar el primer tramo que cumple, completo después del recorte, con los mismos límites para las dos piernas. Si ninguno cumple, informar participante no elegible sin relajar reglas para alcanzar n=9. Guardar ensayo, límites originales y recortados, duración, notas y exclusiones anteriores.

## Ventanas y selección temporal

| Análisis | Bloques ENABL3S a 1.000 Hz | Selección | Motivo |
|---|---|---|---|
| Principal | 256, 512, 1.024 muestras | Independiente por lado | Mantiene las 11 especificaciones RMS originales. |
| Sensibilidad temporal | 133, 266, 532 muestras | Independiente por lado | Aproxima las duraciones de 256/512/1.024 muestras a 1.925,9239 Hz en Dryad. |
| Sensibilidad de emparejamiento | Ambas familias anteriores, separadas | Intersección de bloques seleccionados por los dos lados | Calcula cada razón sobre los mismos instantes; permite identificar dependencia de la selección temporal. |

Para cada familia: RMS completo, RMS con límite absoluto p99,5 y nueve variantes de selección de bloques, con umbral estricto q20 + f(q90−q20), f=0,1/0,2/0,3, calculado por lado. Conservar el código original para el principal. La sensibilidad compartida usa la intersección de sus selecciones; no añade bloques para obtener un resultado. Intersección vacía o denominador no positivo = razón indefinida, nunca cero ni sustitución por otra selección.

Las duraciones equivalentes se obtienen con redondeo a la muestra más cercana, mitades hacia arriba, usando la mediana del reloj Dryad ya estimada; error inferior a 0,5 ms. Esto aproxima duración, no iguala tareas, filtrado, población o fases de marcha. No ajustar frecuencia o tamaños a los resultados de cada participante.

Anclar bloques en el comienzo del tramo recortado. Descartar únicamente la cola incompleta, registrando muestras y porcentaje por tamaño. Conservar índices seleccionados por lado, su intersección y número de bloques; cuatro bloques disponibles no garantizan cuatro seleccionados. La intersección tampoco es un patrón oro fisiológico: puede favorecer periodos de coactivación.

## Comprobación de los márgenes

Recalcular con márgenes de **250 y 1.000 ms**, sobre el **mismo tramo original elegido para el principal**. No buscar otro ensayo o tramo para mejorar el resultado. Aplicar el mismo mínimo de 4.096 muestras tras cada recorte; si no alcanza, registrar sensibilidad no disponible y motivo. Los subconjuntos comparados deben identificarse para no confundir cambio metodológico con cambio de participantes. No introducir margen cero como comparación confirmatoria; el piloto anterior sigue siendo exploratorio.

## Resultados y límites de inferencia

Principal por participante: rango de log-razones entre las 11 variantes RMS. Calcularlo como endpoint completo solo si las 11 razones son positivas y finitas; si faltan, informar razones disponibles y rango parcial etiquetado, sin equipararlo al completo. Secundarios: cambio frente a RMS completo, cruces de 1, diferencias entre selecciones independientes/compartidas y dependencia de bloques y colas descartadas.

Resumir descriptivamente entre participantes (mediana, mínimo, máximo y n disponible). No contar bloques, métodos o ensayos como sujetos; no combinar n=9 con Dryad ni AB191. Sin pruebas de eficacia, ICC, sensibilidad/especificidad clínica, búsqueda de significación o afirmaciones de prioridad científica. Informar casos indefinidos y exclusiones aunque reduzcan la muestra. Ensayos anotados no se rescatan silenciosamente: cualquier análisis posterior será exploratorio y etiquetado.

## Control de cambios y ejecución

La implementación de elegibilidad y selección está en [enabl3s_windows.py](../src/features/enabl3s_windows.py), con pruebas sintéticas de transiciones, huecos, redondeo e intersecciones vacías. Este paso define y prueba reglas; **todavía no ejecuta la cohorte**. Antes de hacerlo, registrar SHA-256 del protocolo y configuración junto a los resultados. Cualquier cambio posterior requiere otra versión, fecha, motivo y declaración de qué datos ya se habían visto; no sobrescribir v1 ni elegir parámetros por el efecto observado. Mantener separada esta extensión de la publicación Kaggle existente hasta tener resultados revisados.

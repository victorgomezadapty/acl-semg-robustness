# ENABL3S: protocolo de transporte metodológico

2026-10-07. Definido después de leer metadatos y descripción, antes de abrir valores de señales. No es una preregistración pública. Es una extensión del estudio Dryad, no una validación clínica en pacientes con reconstrucción de LCA.

## Pregunta y alcance

En adultos sanos, ¿cuánto cambia la razón derecha/izquierda de amplitud del vasto lateral durante marcha en llano al aplicar las mismas 11 especificaciones RMS? La derecha no se interpretará como miembro operado. La razón 1 no constituye un umbral clínico.

Fuente: [ENABL3S, versión 2](https://doi.org/10.6084/m9.figshare.5362627.v2), licencia CC BY 4.0; [artículo de métodos](https://doi.org/10.3389/frobt.2018.00014) y [corrección del enlace del depósito](https://doi.org/10.3389/frobt.2018.00127). Se conservarán atribución, originales e integridad. La documentación descargada llama «Raw Data» a archivos postprocesados; no se afirmará que son voltajes originales sin filtrar.

## Fase piloto y selección previa

Se inspeccionará primero AB191, elegido únicamente porque su ZIP es el menor del depósito (577.792.654 bytes), antes de conocer sus resultados. Este piloto verifica lectura, canales y segmentación; un participante no valida la cohorte. La cohorte completa contiene diez ZIP, aproximadamente 6,49 GB. Se registrarán exclusiones técnicas sin seleccionar participantes por el resultado.

Se identificarán RVL y LVL y la etiqueta de modo de marcha en llano (1 según descripción). Dentro del primer ensayo por orden numérico se elegirá el primer segmento contiguo de modo 1 con ambos canales finitos y longitud mínima de 2.048 muestras. No se concatenarán periodos separados. Si ningún ensayo cumple, el participante se declarará no elegible. Se conservarán índices, nombre del archivo, frecuencia, unidades y cualquier anotación disponible. Si el modo o los canales no pueden identificarse inequívocamente, se detendrá el cálculo para ese archivo.

## Análisis congelado

Primario: reutilizar `src.features.specifications.specifications`, retener únicamente sus 11 variantes RMS y calcular derecha/izquierda. Informar el rango de log-razones entre métodos y los cruces de 1 como sensibilidad descriptiva, sin significado clínico. No añadir filtrado ni centrar señales en este análisis; describir el procesamiento de la fuente. Escala desconocida impide informar amplitudes en voltios; se usarán unidades de exportación. Las razones requieren escala compatible entre canales.

Los bloques de 256, 512 y 1.024 muestras tienen duraciones distintas a las del estudio Dryad: a 1.000 Hz son 256, 512 y 1.024 ms. Por tanto, este análisis transporta el algoritmo por número de muestras, no una ventana temporal equivalente. Una extensión con ventanas de igual duración o normalización MVC requerirá especificación separada; no se mezclará con los resultados primarios.

Registrar variantes indefinidas y denominadores nulos; no reemplazarlos por cero. No tratar bloques o ensayos como participantes independientes. El piloto no llevará pruebas de hipótesis, bootstrap de población ni afirmaciones de fiabilidad, novedad o utilidad clínica. Una aplicación completa informará resultados por participante y resumen entre participantes, sin combinar esta población con pacientes Dryad.

## Condiciones para avanzar

Verificar ZIP por tamaño y MD5 de Figshare, guardar SHA-256 propio, inventariar miembros antes de extracción, confirmar encabezados y anotaciones. El contraste con MVC es una pregunta posterior: disponer de MVC no establece por sí solo una referencia válida de asimetría clínica.

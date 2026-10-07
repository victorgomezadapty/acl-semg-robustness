# Métodos de la ampliación exploratoria

## Comparaciones

Las unidades son participantes. Tres métricas centrales (RMS, MAV y pico absoluto) se calculan sobre el registro entero, preservando reposo y transiciones. La versión de pico positivo se utiliza además en la comparación con el artículo, cuya definición verbal del pico no aclara si se rectificó previamente. Todos los picos permanecen sin limpiar en la versión principal.

Los tests se ejecutan en familias predefinidas: diferencias de miembro, diferencias de condición y diferencias de cohorte. Se reportan t pareado/Welch y Wilcoxon/Mann–Whitney como análisis paralelos, no se selecciona el resultado más favorable. Shapiro–Wilk es diagnóstico; con n pequeño no prueba que la distribución sea normal. Holm se aplica a todos los endpoints de cada familia por separado para tests t y rangos; no representa control global de cualquier análisis futuro. Todas las inferencias son exploratorias.

Ratios orientados se analizan en logaritmos para reducir la influencia de cocientes extremos y preservar dirección. Balance min/max ×100 es independiente de orientación pero oculta dirección; se presenta junto al ratio y amplitudes. Los controles no tienen dominancia mapeada, de modo que diferencias de ratio orientado entre grupos tienen una limitación adicional.

Cohen dz = mean(a−b)/SD(a−b) para pares; Hedges g usa SD combinada y corrección aproximada 1−3/(4df−1) para grupos independientes. Rank-biserial usa rangos signados para pares y 2U/(n_a n_b)−1 para grupos. El signo sigue a−b. Intervalos bootstrap percentil de diferencia de medias remuestrean personas; en pares se conserva cada pareja. Se muestran estimaciones y dispersión, no solo p-values.

Las condiciones son medidas repetidas, no visitas longitudinales. Ninguna prueba de condición establece un mecanismo de fatiga o recuperación. Entre cohortes no existen ajustes por sexo, edad o tiempo postoperatorio porque no se suministran.

## Selección de bloques como sensibilidad

Para cada registro y tamaño (256, 512, 1.024 muestras), RMS por bloques no solapados. Umbral = q20 + f × (q90−q20), con f = 0,1 / 0,2 / 0,3. Se calculan RMS y MAV de los bloques superiores al umbral, fracción seleccionada y número de muestras terminales no incluidas. Todas las combinaciones quedan en block_selection_sensitivity.csv. Esta regla fue elegida por el analista para explorar el efecto de periodos de baja amplitud; no procede del artículo ni identifica actividad/reposo validada, contracciones o ciclos. No se usa para escoger p-values.

## Publicación y discrepancias

La comparación utiliza cocientes adimensionales, evitando inventar las unidades de la tabla de amplitud publicada. Se muestran media y SD de nuestros cocientes de registro completo, separados de los reportados. No se aplican normalización a máximos, cortes o exclusiones para hacer coincidir resultados. Tampoco se atribuyen discrepancias a error de los autores: el procesamiento/ciclo distinto y detalles no disponibles pueden explicarlas.

## Correlaciones y perfiles

Spearman se ejecuta por cohorte-condición-miembro; cada punto es una persona. RMS y MAV comparten muestras, por lo que correlación alta no constituye evidencia biomecánica independiente. Longitud–RMS estudia posible confusión por duración de registro. Holm sobre todas las correlaciones. Los perfiles muestran el control como referencia descriptiva sin percentiles de normalidad ni clearance; para un control la referencia incluye su propio registro, y se avisa. Las señales superpuestas conservan índice original y no están sincronizadas fisiológicamente.

# Primer análisis exploratorio sEMG — 2026-10-04

Se analizaron 88 registros, formando 44 pares miembro-condición de **22 participantes independientes**. Ningún registro se excluyó del análisis principal. Se generaron métricas absolutas, cocientes, sensibilidad y gráficos. El paso de adquisición está completado como revisión/documentación; varios parámetros permanecen sin resolver, como se detalla en acquisition_resolution.md.

## Resultados descriptivos

Cociente RMS de registro completo = inv/uninv. Son razones de amplitud sEMG exportada, no porcentajes de fuerza recuperada. Los intervalos son bootstrap exploratorio de la mediana por participante.

| Cohorte | Condición original | n | Mediana | IQR | IC bootstrap 95% |
|---|---|---|---|---|---|
| healthy | iso90 | 10 | 0,937 | 0,767–1,177 | 0,634–1,179 |
| healthy | iso180 | 10 | 0,933 | 0,579–1,033 | 0,499–1,151 |
| patient | iso90 | 12 | 0,779 | 0,649–1,080 | 0,646–1,086 |
| patient | iso180 | 12 | 0,933 | 0,573–1,037 | 0,570–1,064 |

Los cocientes MAV medianos son 1,005 y 1,013 en controles, y 0,841 y 0,891 en pacientes (iso90/iso180 respectivamente). La distinta ponderación de valores extremos y el tiempo de reposo pueden contribuir a las diferencias entre RMS y MAV; no se atribuyen a un mecanismo clínico específico.

La mediana de pacientes es menor en iso90 que iso180, pero estas cifras no prueban una diferencia de velocidad. Mismas personas, amplitud sin normalizar, diferentes periodos de actividad/reposo y metadatos incompletos limitan la interpretación. No se ejecutaron pruebas de significación ni se concluye que una condición revele mayor déficit.

## Sensibilidad y calidad

- Sin el par corto healthy8/iso90, la mediana RMS de controles cambia de 0,937 (n=10) a 0,868 (n=9). Se mantiene el resultado principal con todos los registros.
- Limitar amplitudes al percentil 99,5 reduce RMS un 29,1% en healthy3/iso180/uninv y un 25,9% en healthy1/iso180/uninv. Los transitorios influyen materialmente en esas magnitudes; no se determina si son artefactos.
- En patient12/iso90/inv la reducción es de aproximadamente 15,0%; revisar el pico antes de interpretar su cociente.
- Los 27 registros con alguna bandera QA incluyen los 24 registros patient/inv con timestamps duplicados. Esto no significa 27 señales descartables o dañadas.
- La mediana entre registros de p90 del RMS por bloques / RMS total es 1,852, 1,846 y 1,719 para 256/512/1024 muestras. La agregación cambia con el bloque; no equivale a identificar contracciones o elegir automáticamente una ventana óptima.

## Gráficos y datos

- [Valores individuales RMS por miembro](../../reports/figures/rms_V_paired_amplitude.png)
- [Valores individuales MAV por miembro](../../reports/figures/mav_V_paired_amplitude.png)
- [Cocientes RMS identificados por participante](../../reports/figures/individual_rms_ratios.png)
- [Distribuciones por cohorte, condición y miembro](../../reports/figures/rms_cohort_distributions.png)

Las distribuciones comparan las señales exportadas, no activación fisiológica equivalente. Controles y pacientes no están emparejados por características demográficas; la orientación dominante/no dominante en controles no está establecida. El ratio grande del registro corto healthy8 hace visible la fragilidad de resumir simetría sin revisar valores y calidad.

Tablas: data/processed/semg_amplitude_features.csv (88 filas), semg_paired_amplitude.csv (44 filas), reports/amplitude_group_summary.csv y amplitude_eda_summary.json. La tabla de features conserva número de muestras, flags, métricas absolutas y bloques; la de pares conserva ambos miembros junto a los cocientes. Todos son regenerables.

## Conclusión permitida

El pipeline permite caracterizar amplitud y variabilidad de registros sEMG y detectar sensibilidad a calidad/agregación. No permite inferir fuerza, inhibición artrogénica, recuperación longitudinal, reinjury risk o preparación deportiva. Antes de un análisis por contracción o filtrado temporal se necesita documentación de adquisición y segmentación. La reproducción del artículo secundario de 2026 requeriría detalles adicionales y no se ha afirmado que sus resultados estén reproducidos.

Validación: pruebas analíticas de RMS/MAV, invariancia al signo, manejo del bloque incompleto, entradas inválidas y denominador cero; verificación de hash y estructura al cargar. Código: scripts/check_amplitude.py y scripts/exploratory_amplitude.py. No se usó ML.

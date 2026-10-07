# Presentación final — guion de 8 diapositivas

6 de octubre de 2026 · Duración orientativa: 8–10 minutos. Este archivo es el guion editable; no es un archivo PowerPoint.

## 1. Pregunta y propuesta

**ACL Rehabilitation Analytics: medir simetría sin perder el contexto de la señal.** ¿Cómo varía la amplitud sEMG entre miembros y condiciones, y cuánto depende de la decisión analítica? Aportación: análisis reproducible y perfiles auditables.

## 2. Datos y decisiones

22 participantes, 88 registros, sEMG del vasto lateral en voltios. Dos condiciones y ambos miembros. Hashes verificados, padding final retirado, todas las personas incluidas. RMS/MAV/picos, bootstrap por persona y comparaciones pareadas; Holm por familia. Torque, IMU y desenlaces no están en el archivo.

## 3. Mostrar amplitudes antes de cocientes

![Valores RMS](../../reports/figures/rms_V_paired_amplitude.png)

Mensaje oral: conservar ambos valores permite distinguir señales pequeñas de señales grandes aunque sus cocientes sean similares. La amplitud exportada no mide fuerza.

## 4. Distribución y evidencia

![Balance individual](../../reports/figures/extended_balance_distributions.png)

Medianas RMS dirigidas en pacientes: 77,9% en iso90 y 93,3% en iso180. Ninguna de 60 comparaciones permanece por debajo de p-Holm 0,05. Descriptivos diferentes no prueban un efecto de velocidad; falta evidencia de equivalencia.

## 5. Revisar el denominador

![Perfil healthy8](../../reports/figures/profiles/healthy8.png)

Un registro corto y pequeño cambia la media RMS de controles iso90: 328,56% con todos frente a 84,91% sin ese par como sensibilidad. La mediana cambia menos: 93,7% a 86,8%. El participante sigue incluido en el resultado principal.

## 6. Cuantificar dependencia del método

![Sensibilidad](../../reports/figures/block_ratio_sensitivity.png)

Tres tamaños de bloque × tres umbrales. No representan contracciones validadas. Los resultados completos no coinciden exactamente con el artículo de 2026: el efecto del registro corto está observado; procesamiento y límites de contracción siguen como explicaciones posibles no confirmadas.

## 7. Producto consultable

![Perfil patient12](../../reports/figures/profiles/patient12.png)

Demostración del [visor de 22 perfiles](../../reports/analysis_index.html). Cada perfil permite revisar señal, ambas condiciones y amplitudes. Código, tablas, literatura y métodos acompañan la presentación. No hay puntuación de alta deportiva.

## 8. Conclusión y extensión

La auditoría adicional ya evaluada encuentra cambios de dirección en 13 de 44 pares entre 21 especificaciones, y en 10 pares si solo se comparan variantes RMS. Las señales sintéticas comprueban cómo reposo, transitorios y un denominador pequeño alteran el resumen. Mostrar la [matriz de sensibilidad](../../reports/figures/robustness_matrix.png) como figura de respaldo. Esta es la aportación propia del caso: hacer visible la dependencia del método. No se afirma novedad científica ni relevancia clínica de cualquier cambio de signo.

La simetría es interpretable cuando conserva las magnitudes y la calidad que la producen. El siguiente estudio candidato agrega sEMG de varios músculos y covariables clínicas en otra cohorte. Primero se verificará la correspondencia individual con ACL-RSI; después una asociación exploratoria predefinida. No se mezclan cohortes ni se interpreta preparación psicológica como retorno deportivo observado.

Fuentes y cifras: [caso completo](portfolio_case_study.md), [resultados](comprehensive_results.md), [métodos](comprehensive_methods.md), [búsqueda de extensión](extension_plan.md).

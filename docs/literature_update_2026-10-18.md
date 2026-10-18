# Revisión crítica: cómo mejorar la auditoría sEMG y qué datos faltan

Actualización: 2026-10-18. Revisión dirigida y trazable para el portfolio; no revisión sistemática exhaustiva, metaanálisis, preregistro ni evaluación clínica. Complementa la [revisión anterior](history/literature_review.md), sin reemplazar su fecha ni sus observaciones. [Consultas](literature_search_2026-10-18.csv) · [matriz de evidencia](literature_evidence_2026-10-18.csv).

## Pregunta y alcance

**PICOTT:** personas con reconstrucción unilateral de LCA; diferentes resúmenes y selecciones temporales de sEMG bilateral; comparación con RMS completo y, en una fase futura, torque medido y repeticiones; sensibilidad, error de medición y validez para una tarea definida; misma visita para la auditoría, sesiones repetidas para fiabilidad y seguimiento para relevancia clínica; estudio secundario de métodos, seguido de estudios de medición. Los controles sanos y ENABL3S se mantienen separados de los pacientes.

La búsqueda priorizó 2023–2026, con referencias anteriores esenciales. Se usó búsqueda web dirigida hacia artículos editoriales, registros PubMed/PMC, repositorios institucionales y depósitos originales. Las consultas literales y las restricciones de acceso constan en el registro. Se seleccionaron fuentes relacionadas con procesamiento, normalización, fuerza, asimetría o datos reutilizables. Se excluyeron páginas comerciales y fuentes secundarias como soporte de conclusiones científicas. No hubo búsquedas nativas completas en Embase/SPORTDiscus, exportación exhaustiva, cribado independiente por dos revisores ni evaluación formal de riesgo de sesgo. No se informa un diagrama PRISMA ni un número de estudios recuperados que no se haya contado. La búsqueda no demuestra prioridad científica ni ausencia de otros trabajos.

Se distinguen resumen, secciones de texto completo accesibles y archivos realmente inspeccionados. Fallos de acceso directo se resolvieron cuando fue posible con pasajes indexados de la fuente primaria; esto no equivale a leer íntegramente un artículo o su suplemento. Doce fuentes seleccionadas se resumen en la matriz. Son heterogéneas y no se combinaron numéricamente. Los siguientes juicios de aplicabilidad son nuestros, no conclusiones atribuidas a los autores.

## Qué aporta la evidencia

### Normalización, informe y relación con fuerza

- **L01 — Besomi et al., 2020, CEDE:** ofrece opciones de normalización según contexto. Para nuestro caso, conservar escala y documentar la referencia tiene prioridad sobre aplicar MVC o normalización al máximo por costumbre. No hay MVC documentada en Dryad que podamos reconstruir. [Artículo](https://doi.org/10.1016/j.jelekin.2020.102438).
- **L02 — Besomi et al., 2024, CEDE-Check:** estructura el reporte de tarea, electrodos y adquisición/procesamiento. Proponemos registrar para cada campo «documentado», «inferido» o «desconocido», con ubicación de la evidencia. No declarar cumplimiento completo cuando los metadatos originales faltan. [Artículo](https://doi.org/10.1016/j.jelekin.2024.102874).
- **L03 — Dick et al., 2024, CEDE fuerza:** la inferencia de fuerza mediante EMG depende del contexto biomecánico y de supuestos. Nuestro cociente eléctrico no identifica fuerza individual del VL; una futura referencia de torque representa la acción neta de varios músculos. [Artículo](https://doi.org/10.1016/j.jelekin.2024.102910).

**Mejora propuesta:** convertir las incertidumbres de adquisición en un registro visible por fuente y decidir el método según el objetivo. Esa documentación mejora auditabilidad; no recupera información ausente.

### Estudios que permiten un contraste útil

- **L04 — Khafagy y Hamza, 2026:** reutiliza el mismo Dryad. Es el comparador directo de decisiones y definiciones; no constituye una muestra externa. Contrastar población, pico/RMS, escala, ventanas y denominador antes de comparar cifras. Las diferencias de implementación incompletamente descritas no prueban un error del artículo ni una superioridad nuestra. [Artículo](https://doi.org/10.25259/JMSR_129_2026).
- **L05 — Cobian et al., 2024:** estudia 30 atletas con torque y sEMG en visitas a 4, 6 y 12 meses. Analiza una meseta de contracción y variabilidad, no nuestro rango entre once razones. Es un buen modelo para separar control del torque, amplitud y tiempo de recuperación. No se confirmó un depósito abierto de señales individuales. [Texto](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168251/).
- **L06 — Sherman et al., 2025:** compara 20 personas con ACLR y 20 controles durante extensión al 50% del esfuerzo máximo, con EMG de alta densidad del VM. El artículo enlaza datos de descomposición y EEG en OSF. Es candidato para estudiar control neuromuscular, pero no se confirmó que incluya amplitud bilateral original del VL y torque sincronizado reutilizable. [Artículo](https://doi.org/10.1152/japplphysiol.00641.2024) · [depósito](https://osf.io/hv6x2/).
- **L07 — Nuccio et al., 2024:** registra EMG de alta densidad del VL/VM y salida de fuerza para explorar control motor tras ACLR. Los datos se ofrecen por solicitud razonable; no se localizaron archivos abiertos en esta revisión. Su pregunta sobre unidades motoras requiere adquisición y procesamiento distintos de nuestro resumen bipolar. [Artículo](https://doi.org/10.1152/japplphysiol.00056.2024).
- **L08 — Forquignon et al., 2026:** compara 60 pacientes con distintos injertos mediante fuerza isométrica, sEMG normalizada y resultados clínicos. No encontrar diferencias significativas de sEMG no establece equivalencia ni ausencia de debilidad. Los datos no son públicos por privacidad, según su declaración. [Artículo](https://doi.org/10.1002/ksa.70342).
- **L09 — Ledesma-Clopés et al., septiembre de 2026:** estudio transversal de 13 deportistas con fuerza y EMG durante sentadilla con volante de inercia, con análisis por fases y complejidad. Sugiere una pregunta distinta sobre estructura temporal; no valida nuestros cocientes ni permite trasladar parámetros de complejidad a registros de longitud/filtrado diferente. La disponibilidad de archivos reutilizables no quedó confirmada. [Artículo](https://doi.org/10.3390/s26185745).

**Contraste que sí podemos presentar ahora:** una tabla de preguntas, tareas, señales, normalización y desenlaces. No se pueden sumar los pacientes de esos estudios a nuestros datos ni comparar porcentajes de «recuperación» como si midieran lo mismo. Un contraste numérico con resultados publicados exigiría igual definición, escala y unidad de análisis; datos agrupados no permiten recuperar la sensibilidad individual entre métodos.

### Datos abiertos: separar promesa de elegibilidad

- **L10 — Zhang et al., 2026 / Figshare v2:** el descriptor presenta marcha bilateral de 17 pacientes. Este candidato **ya estaba inspeccionado el 2026-10-06**: las hojas contienen 101 puntos y no cumplen las ventanas de al menos 256 muestras del protocolo. El artículo menciona ACL-RSI, pero el libro clínico inspeccionado contiene K-STARTS, sin una columna ACL-RSI independiente identificada. No igualamos ambas medidas ni inferimos un enlace de IDs no documentado. [Descriptor](https://doi.org/10.1038/s41597-026-07543-2) · [auditoría de archivos](history/external_validation_feasibility.md). No se repitió la descarga ni se lo presenta como nuevo hallazgo.
- **L11 — Hu, Rouse y Hargrove, ENABL3S:** sirve para transporte metodológico en marcha sana, ya completado. No añade pacientes ACLR, torque de validación o seguimiento clínico al análisis actual. [Dataset versionado](https://doi.org/10.6084/m9.figshare.5362627.v2).
- **L12 — Kotsifaki et al., Aspetar 2023:** ofrece un marco de rehabilitación con múltiples dimensiones. No proporciona un umbral validado para nuestra razón sEMG. [Guía](https://doi.org/10.1136/bjsports-2022-106158).

## Ruta recomendada y criterios para avanzar

| Prioridad | Acción | Datos o verificación requerida | Qué permitiría afirmar |
|---|---|---|---|
| Ahora | Cerrar auditoría y mostrar casos individuales, exclusiones y decisiones | Resultados actuales, hashes y código | Sensibilidad del resultado al método, con trazabilidad |
| Próxima, sin nueva recogida | Auditar metadatos, licencia e inventario OSF HV6X2 | Confirmar archivos, músculos, bilateralidad, escala, torque, reloj y repeticiones; aún pendiente | Elegibilidad o inelegibilidad real; no validez por el nombre del depósito |
| Extensión alternativa | Estudiar forma temporal/sinergias en Zhang con protocolo propio | Resolver escala, correspondencia de IDs y medida clínica; no interpolar para fingir señal original | Resultado exploratorio de una pregunta distinta |
| Validación de medición | Comparar métodos con torque medido en una tarea acotada | Señal original bilateral sincronizada, unidades, metadatos y repeticiones; participantes separados para evaluación | Error fuera de muestra y acuerdo para esa tarea |
| Fiabilidad | Repetir en condiciones estables con recolocación documentada | Al menos dos sesiones, varias repeticiones y tamaño muestral por precisión | ICC apropiado, error absoluto y límites de acuerdo |
| Relevancia clínica | Evaluar cambio y aporte adicional frente a evaluación habitual | Seguimiento, función, dolor, medidas validadas y desenlaces definidos previamente | Asociación longitudinal y posible valor adicional; utilidad de decisión exige validación posterior |

La [hoja de ruta clínica](clinical_validation_roadmap.md) desarrolla el diseño. Proponemos empezar por extensión isométrica con varios niveles de esfuerzo: permite alinear ventanas con una referencia mecánica. Es una elección de diseño, no un protocolo óptimo demostrado. Fijar antes de ver nuevos resultados: tarea/ángulo, métodos, normalización, criterio de exclusión, error primario y partición por persona. Comparar modelos simples, evaluar calibración y error en personas reservadas; no repartir sus bloques entre entrenamiento y evaluación. La precisión y las pérdidas determinan el tamaño de muestra; seis participantes sanos no lo justifican.

## Qué cambia y qué no cambia en esta entrega

Se mejora presentación, descarga y procedencia de paquetes. Se incorpora un mapa crítico de estudios y datos candidatos. No se recalcularon ni cambiaron los endpoints congelados, no se analizaron nuevos pacientes y no se demuestra utilidad clínica, causalidad ni novedad científica. El contraste bibliográfico orienta el siguiente estudio; no sustituye una medición independiente.

## Autoría, atribución y futuras revisiones

La síntesis y las decisiones son redacción propia. Se enlazan las fuentes; no se redistribuyen figuras, tablas, cuestionarios ni PDFs de terceros. Los artículos y depósitos conservan sus licencias. Las figuras del portfolio se generan con resultados propios derivados y conservan atribución CC BY 4.0 para ENABL3S; el código/texto original conserva MIT. La licencia de un artículo no certifica la de cada archivo enlazado.

Para actualizar: repetir consultas con fecha y rango explícitos, añadir registros sin borrar los anteriores, comprobar correcciones/retractaciones en las páginas editoriales y registrar versiones de cada depósito. En esta revisión no se realizó una búsqueda independiente exhaustiva de retractaciones; las limitaciones de acceso y las verificaciones pendientes figuran en la matriz. El usuario hará la revisión científica final. No se contactó con autores ni se solicitó acceso a datos privados.

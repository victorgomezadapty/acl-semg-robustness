# Revisión dirigida de novedad y posicionamiento científico

Fecha: 2026-10-06. Pregunta y elegibilidad: [protocolo PICOTT](picott_research_protocol.md).

## Método y alcance

Revisión dirigida reproducible de antecedentes, con cribado por un único evaluador asistido por IA. No es revisión sistemática ni metaanálisis, no tiene doble cribado independiente y no permite demostrar ausencia de trabajos previos. Se consultaron PubMed mediante E-utilities, búsquedas web hacia fuentes primarias editoriales y depósitos institucionales, y repositorios de datos. No se consultaron Embase ni Scopus de forma completa. No se impusieron límites de idioma o año.

Cinco consultas PubMed recuperaron 12, 16, 7, 0 y 9 registros, respectivamente: 44 registros únicos tras deduplicación por PMID. La consulta de frase exacta CEDE produjo un aviso de frase no reconocida; se conservó el fallo y se añadió CEDE AND electromyograph*. Los cero resultados de esa consulta no son evidencia de ausencia. Todas las consultas, fechas y límites se guardan en [search_log.csv](../../data/literature/pubmed_methods_20261006/search_log.csv); las traducciones/avisos están en [pubmed_search_audit.json](../../reports/pubmed_search_audit.json).

Las decisiones de relevancia de los 44 títulos se conservan en [novelty_screening.csv](../../reports/novelty_screening.csv). Se leyeron resúmenes de los antecedentes centrales y del contexto ACLR seleccionado; el nivel de lectura de cada fuente se indica, sin afirmar lectura completa cuando el acceso fue parcial. El resto se descartó por título para esta pregunta de métodos, no por calidad científica. Fuentes adicionales localizadas fuera de PubMed se describen como búsqueda complementaria.

## Antecedentes que impiden reivindicar la idea general como nueva

| Referencia | Evidencia consultada y relación con el proyecto |
|---|---|
| Benoit DL, Lamontagne M, Cerulli G, Liti A. 2003. [Clinical significance of EMG normalisation in ACL injury](https://doi.org/10.1016/S0966-6362(02)00194-7); [PMID 14654208](https://pubmed.ncbi.nlm.nih.gov/14654208/) | Resumen: compara tres referencias de normalización durante marcha en personas con lesión de LCA y describe cambios en interpretación. Lesión de LCA no equivale a nuestra población reconstruida. Aun así, la pregunta general sobre normalización e interpretación en LCA tiene antecedente directo. |
| Devaprakash D et al. 2016. [Influence of filter, normalisation and co-contraction algorithm](https://doi.org/10.1016/j.jelekin.2016.10.001); [PMID 27810649](https://pubmed.ncbi.nlm.nih.gov/27810649/) | Resumen y extractos: evaluación de elecciones analíticas sEMG en tareas deportivas. No demuestra que todas las opciones de filtro alteren interpretación. Nuestro proyecto no inventa la sensibilidad al procesamiento. |
| Shuman BR, Schwartz MH, Steele KM. 2017. [Processing impacts muscle synergies during gait](https://doi.org/10.3389/fncom.2017.00050); [PMID 28634449](https://pubmed.ncbi.nlm.nih.gov/28634449/) | Resumen: dependencia de resultados de sinergias respecto a procesamiento en población distinta. Antecedente de sensibilidad, no validación de nuestra métrica. |
| Rutkowska JM et al. 2024. [Optimal processing of facial EMG](https://doi.org/10.3758/s13428-024-02421-4) | Métodos y disponibilidad: compara 72 pipelines con datos y código públicos. Existe investigación multiverse en EMG; la aplicación facial no es una cohorte clínica de LCA. |
| Simonsohn U, Simmons JP, Nelson LD. 2020. [Specification curve analysis](https://doi.org/10.1038/s41562-020-0912-z) | Antecedente general localizado en búsqueda complementaria. Nuestra matriz es descriptiva y no implementa su procedimiento inferencial completo. |

## Referencias para diseñar y reportar correctamente

[Besomi et al., CEDE normalización 2020](https://doi.org/10.1016/j.jelekin.2020.102438) fundamenta explicitar la referencia y el objetivo de interpretación. [Besomi et al., CEDE-Check 2024](https://doi.org/10.1016/j.jelekin.2024.102874) orienta la descripción de tarea, electrodos y adquisición/procesamiento. [CEDE fuerza, 2024](https://doi.org/10.1016/j.jelekin.2024.102910) es contexto para evitar tratar directamente sEMG como torque. No se ha reproducido ni puntuado el checklist CEDE completo.

El [estudio secundario exacto de Dryad, Khafagy y Hamza 2026](https://doi.org/10.25259/JMSR_129_2026) ya compara amplitud y cocientes. Nuestra tabla preserva la discrepancia y no fuerza una reproducción. El [estudio de flywheel squat de 2026](https://doi.org/10.3390/s26185745), consultado mediante resumen y métodos editoriales, aporta contexto sobre análisis por fases y revisión de señales; no avala los umbrales de nuestro código.

## Conclusión de novedad

**No es defendible afirmar que descubrimos que el procesamiento cambia la interpretación sEMG, ni que inventamos el análisis multiverse.** Tampoco se ha demostrado que nuestra auditoría de bloques mejore decisiones clínicas.

La aportación defendible actual es un caso reproducible del dataset concreto: conservar valores absolutos, cuantificar dependencia de resúmenes, mostrar problemas de cocientes, ofrecer matriz individual y perturbaciones sintéticas conocidas. La comparación bibliográfica dirigida no identificó una reproducción exacta de este conjunto completo de decisiones en el ZIP Dryad, pero su ausencia en esta búsqueda no prueba prioridad científica.

El objetivo publicable propuesto es una nota de métodos/reproducibilidad, con resultados descriptivos y limitaciones, no un método clínico nuevo validado. La [evaluación externa](external_validation_feasibility.md) aún no proporciona validación directa. Se deben informar tanto los resultados de sensibilidad como los candidatos descartados.

## Control de integridad de fuentes

En la búsqueda web complementaria aparecieron registros con expresión de preocupación o retractación (PMID 31598766 y 33159260). No se usaron como soporte positivo de conclusiones. La ausencia de avisos en otros registros consultados no garantiza integridad absoluta ni constituye una auditoría exhaustiva de todas las publicaciones.

No se copiaron figuras, tablas de artículos, párrafos o código externo para estos documentos. Las síntesis son propias, con citas cercanas y acceso declarado. La publicación final requerirá revisión humana de citas, licencias y contenido; no se afirma una garantía automática de ausencia de plagio.

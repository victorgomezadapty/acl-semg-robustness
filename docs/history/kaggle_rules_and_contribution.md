# Reglas de Kaggle y aportación del proyecto

Revisión: 2026-10-06. No se publicó contenido ni se hizo una entrega de competición.

## Estado del reto

### Comprobación adicional de publicación

Búsqueda web del 2026-10-06 por DOI exacto, título del dataset y ACL rehabilitation en dominios Kaggle: no se encontró una competición asociada inequívocamente al dataset. Los resultados relacionados con resonancia de rodilla u otros hackathons no corresponden a este análisis.

La [documentación oficial de datasets](https://www.kaggle.com/docs/datasets) permite cargar archivos locales y publicar datasets públicos o privados; recomienda notebooks desde EDA hasta reproducción de investigación. La [documentación de notebooks](https://www.kaggle.com/docs/notebooks) permite incorporar datos propios. Por tanto, el formato dataset documentado + notebook de este proyecto tiene una vía de publicación sin pertenecer a una competición. Esto no confirma la ejecución técnica del notebook actual en Kaggle ni garantiza aceptación de cualquier contenido: siguen aplicando licencias y normas de la plataforma.

La expresión «reto» utilizada en el proyecto se refiere actualmente a un reto personal de portfolio, no a una competición oficial identificada. No existe aquí un leaderboard, premio o formato de submission verificado.

El planteamiento original define un proyecto de portfolio con datos Dryad; no identifica una competición Kaggle, organizador, reglas, métrica ni plazo. Una búsqueda dirigida no identificó una competición inequívoca de este proyecto. Esto no demuestra que no exista: falta el enlace proporcionado por el usuario.

No se pueden confirmar reglas de datos externos, equipos, uso de herramientas, formato de entrega o evaluación sin la página específica del reto. Publicar un notebook y participar en una competición son acciones diferentes.

## Reglas generales revisadas

[Community Guidelines](https://www.kaggle.com/community-guidelines), actualizadas el 4 de marzo de 2026 según el resultado oficial indexado: aplican a notebooks, datasets y discusiones; prohíben plagio, contenido engañoso, infracciones de propiedad intelectual y manipulación de reputación. También restringen pedir votos y autopromoción fuera de contexto. Citar fuentes y distinguir trabajo propio de reutilización es esencial.

[Documentación de datasets](https://www.kaggle.com/docs/datasets): contempla publicar datasets con licencia y metadatos. La fuente original es [Gutierrez, Hart y Boukhechba, Dryad 2022](https://doi.org/10.5061/dryad.66t1g1k4j). El manifiesto consultado anteriormente registra CC0; debe conservarse esa procedencia y verificarse la licencia al preparar la carga. No presentar los datos como recogidos por nosotros.

[Terms of Use](https://www.kaggle.com/terms): enlace oficial localizado, pero la apertura no devolvió texto legible. No se afirma auditoría completa de sus cláusulas. Las reglas específicas de una eventual competición siguen pendientes.

## Auditoría de originalidad

| Componente | Clasificación honesta |
|---|---|
| Dataset | Creado por los autores originales, no por nosotros |
| RMS, picos, simetría y tests habituales | Métodos establecidos; el artículo de reutilización ya aplica categorías similares |
| Pipeline y documentación del proyecto | Implementación propia del proyecto; no constituye por sí misma descubrimiento científico |
| Sensibilidad a denominador pequeño, picos y bloques | Exploración propia documentada; no se ha demostrado que nadie la haya publicado antes |
| Perfiles y visor | Producto propio de comunicación, sin validación clínica |
| Conclusión clínica o método nuevo validado | No logrado |

El análisis actual es una base reproducible y una crítica metodológica exploratoria. No debe anunciarse como novedad científica demostrada. Tampoco es una reproducción exacta del artículo secundario.

## Aportación propuesta: robustez de la interpretación de simetría

Pregunta: ¿qué participantes y comparaciones conservan su dirección y magnitud de asimetría sEMG cuando cambian decisiones razonables de resumen?

Propuesta: una matriz por participante que muestre la distribución de log(inv/uninv), dirección de la diferencia y variación de magnitud bajo especificaciones explícitas. Sin score de retorno deportivo ni umbral clínico. Las reglas de bloque existentes, RMS/MAV y límite de picos serían especificaciones de sensibilidad, no muestras independientes.

Evaluación antes de reivindicar utilidad:

1. Congelar especificaciones y resultados que se evaluarán. Como los datos ya fueron explorados, etiquetar el estudio como retrospectivo; no fingir preregistro.
2. Usar señales sintéticas con relación bilateral conocida para comprobar invariancia a ganancia común y cambios inducidos por pausas, transitorios o denominador pequeño. Esto prueba comportamiento matemático, no fisiología clínica.
3. Contrastar la matriz con el resumen RMS único: cuantificar participantes que cambian de dirección y cuánto cambia la magnitud. Las especificaciones no se tratarán como réplicas estadísticas independientes.
4. Separar incertidumbre entre personas de sensibilidad a especificación. No interpretar ventanas temporales como nuevas personas o repeticiones clínicas.
5. Revisar literatura de specification-curve/multiverse y robustez sEMG antes de afirmar novedad; contrastar después en una cohorte independiente con protocolo documentado.

Resultado útil incluso sin inventar una métrica: identificar qué interpretaciones dependen del método, ofrecer un informe auditable y mostrar cuándo un cociente único es insuficiente. La aportación queda demostrada únicamente si la evaluación muestra información adicional concreta; aún no está implementada ni validada.

# Evaluación externa: elegibilidad y resultado de la inspección

2026-10-06 · Protocolo previo a apertura de valores: [PICOTT](picott_research_protocol.md). **Estado: validación directa pendiente; factibilidad evaluada en fuentes concretas.**

## Candidato 1: Zhang et al., marcha bilateral

Fuente: [descriptor Scientific Data 2026](https://doi.org/10.1038/s41597-026-07543-2); depósito [Figshare versión 2](https://doi.org/10.6084/m9.figshare.30928694.v2), autor del depósito Hongxiang Zhang. Licencia del depósito: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Se descargaron los nueve archivos (573.312 bytes), sin modificar originales. Todos coinciden en tamaño y MD5 con la API; se retuvieron SHA-256 propios en download_manifest.json. Inventario completo: [external_cohort_audit.json](../../reports/external_cohort_audit.json).

Observación directa de archivos:

- Cada libro bilateral de EMG tiene 17 hojas identificadas 1–17. Cada hoja tiene 101 filas numéricas y ocho canales, más una columna «X [s]».
- El canal VL está presente. Los valores observados son positivos y pequeños; esto no establece por sí solo unidad, filtrado, normalización o naturaleza de la señal.
- El libro clínico contiene datos básicos (P01–P17), K-STARTS y dos hojas cinemáticas. No se observó una columna ACL-RSI independiente. No se fabricó una equivalencia entre K-STARTS y ACL-RSI ni entre formatos de ID.

El descriptor informa adquisición a 2.000 Hz y procesamiento/normalización a una representación de 101 puntos. No se supone que esa frecuencia describa la exportación de 101 filas. Los nombres del repositorio hablan de EMG; no se considera «raw» en el sentido de señal original por esa etiqueta. La conexión exacta entre valores exportados, escala y pipeline requiere aclaración.

**Decisión:** no elegible para ejecutar sin cambios las 11 especificaciones RMS (los bloques más pequeños son de 256 muestras). No se inventaron muestras por interpolación para aparentar cumplimiento. Una evaluación de forma temporal normalizada sería un protocolo diferente, no validación de amplitud del estudio Dryad.

## Candidato 2: Konrath et al., sidestep cutting

Fuente: [PLOS ONE 2023](https://doi.org/10.1371/journal.pone.0292867); depósito [Figshare versión 1](https://doi.org/10.6084/m9.figshare.22139915.v1), Jason Konrath. Licencia: CC BY 4.0 según API.

Se verificaron dos ZIP, 12.232.902 bytes en total, por tamaño y MD5; SHA-256 guardados. Se inspeccionaron miembros sin extracción. Cada ZIP tiene 1.260 archivos útiles de configuraciones y salidas del modelo. El inventario incluye Activations.sto, MuscleForces.sto y Torques.sto; una cabecera de Activations.sto dice «CEINMS output». Los dos paquetes corresponden a modelos de músculo dañado/no dañado; no deben interpretarse como si sus nombres identificaran automáticamente miembros operado/contralateral.

**Decisión:** los archivos disponibles inspeccionados son salidas modeladas y configuraciones, no originales de adquisición sEMG. No se usaron fuerzas simuladas como torque medido ni activaciones del modelo como amplitud eléctrica. Inventario: [konrath_source_inventory.json](../../reports/konrath_source_inventory.json).

## Candidato 3: AMI, Zenodo

[Schilaty, Zenodo 6427111](https://doi.org/10.5281/zenodo.6427111) describe EMG descompuesta en lesión de LCA. La versión consultada restringe los archivos. La página indica una versión posterior, cuya apertura no se logró confirmar. No se descargaron datos restringidos; ACL lesionado no demuestra reconstrucción ni elegibilidad bilateral. Estado: no elegible actualmente para validación abierta con los datos accesibles.

## Qué se consiguió y qué falta

### Actualización 2026-10-07: vía metodológica en población sana

Se verificaron metadatos de [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2), con diez paquetes de participantes y licencia CC BY 4.0. La descripción del depósito se descargó y coincide con el MD5 publicado. Identifica canales RVL/LVL y etiquetas de tarea, pero denomina «Raw Data» a señales postprocesadas. Antes de abrir sus valores se definió un [protocolo separado](enabl3s_transport_protocol.md) y un piloto AB191 elegido por tamaño del archivo. La descarga e inspección del piloto no equivalen a haber validado la cohorte. Esta población sana permite explorar transporte del método, no validar resultados clínicos de reconstrucción de LCA.

El piloto se completó: ZIP verificado, 11 especificaciones RMS ejecutadas y auditoría posterior de selección temporal. [Resultados, decisiones y límites](../enabl3s_pilot_review.md). No se modificó la conclusión de inelegibilidad de las fuentes ACLR anteriores.

Se completaron adquisición legal de fuentes públicas, verificación de integridad, lectura de métodos e inspección de archivos de dos depósitos. **No se completó una validación externa positiva:** ninguna de esas exportaciones cumple los requisitos del protocolo actual. Este resultado negativo forma parte del estudio y evita una conclusión de validación falsa.

Para continuar se necesitan registros bilaterales originales del VL, unidades, parámetros de adquisición y procesamiento, límites de tarea/ciclos, escalas de normalización y relación explícita de IDs/visita. Repeticiones o sesiones independientes son necesarias si se quiere estimar fiabilidad test-retest. Datos funcionales no son una referencia automática de calidad de señal.

Un [borrador de solicitud de datos](data_request_draft.md) especifica los campos requeridos. No se contactó a autores ni se envió información. Los datos externos no se incorporaron al paquete Kaggle previamente preparado; ese paquete sigue correspondiendo a Dryad y su evaluación local.

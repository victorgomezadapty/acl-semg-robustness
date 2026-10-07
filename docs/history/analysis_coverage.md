# Alcance implementado con los datos disponibles

Fecha de corte: **2026-10-04**. Búsqueda dirigida por DOI exacto, autores originales y título del trabajo de reutilización; fuentes primarias editoriales. Se encontró un análisis secundario explícito del ZIP: [Khafagy y Hamza, 2026](https://doi.org/10.25259/JMSR_129_2026). El [trabajo de autores originales, 2022](https://doi.org/10.54941/ahfe1001471) usa un estudio más amplio y señales de marcha/IMU que no están en este paquete. No se afirma cobertura exhaustiva de toda la literatura.

| Método / producto | Implementación y estado |
|---|---|
| Inventario, unidad, padding y calidad temporal | Completo para todos los archivos y participantes |
| RMS, pico, media absoluta | Exportación completa; pico positivo y absoluto diferenciados |
| Simetría de amplitud | inv/uninv ×100, log-ratio y min/max ×100; ambos valores absolutos conservados |
| Descriptivos | Media, SD, mediana, IQR, dispersión individual |
| Normalidad (Shapiro–Wilk) | Diagnóstico exportado; no selector automático del test |
| Miembro inv vs uninv | t pareado y Wilcoxon; participantes pareados |
| Condiciones iso180 vs iso90 | t pareado y Wilcoxon sobre amplitudes y ratios |
| Pacientes vs controles | Welch t y Mann–Whitney sobre amplitudes y ratios |
| Tamaños de efecto | Cohen dz pareado, Hedges g independiente y correlación rank-biserial |
| Incertidumbre | Bootstrap participante, 5.000 réplicas; diferencia de medias e intervalos previos de mediana |
| Multiplicidad | Holm separado por familia y tipo de test; tablas conservan p originales y ajustados |
| Relaciones entre variables | Spearman de RMS–MAV, RMS–pico y longitud–RMS; no pooling de muestras |
| Sensibilidad a picos/registro corto | Implementada, separada del análisis principal |
| Selección de bloques de mayor amplitud | 3 tamaños × 3 umbrales; exploración propia, no segmentación validada |
| Comparación con publicación | Tabla con nuestros cocientes y valores reportados; no reproducción exacta |
| Perfiles individuales | 22 figuras: ambas condiciones, señales, RMS/pico y referencia descriptiva de controles |

Implementamos las categorías de análisis descritas en el artículo de reutilización, con decisiones explícitas. Exactamente replicar sus números requiere una definición reproducible de ciclos, procesamiento, unidades de amplitud y selección/normalización; esos detalles no están establecidos en el texto. La tabla de comparación no ajusta el pipeline para forzar concordancia.

No se ejecutan estimaciones de torque, fuerza, IMU, coactivación entre músculos, seguimiento longitudinal, diagnóstico de AMI, clasificación RTS o predicción de reinjuria: faltan las mediciones correspondientes. No se añade ML porque no responde una pregunta adicional justificada con este pequeño conjunto. Esta exclusión preserva el objetivo original del usuario.

## Política de supuestos

Los nombres iso90/iso180 se conservan; °/s tiene respaldo en el artículo secundario. Se mantienen las etiquetas de miembros del ZIP. No se requiere contactar a los autores para los análisis presentes. La orientación dominante en controles y configuración del equipo se registran como límites interpretativos. Toda segmentación propuesta se etiqueta como selección matemática de amplitud, sin afirmar que recupera contracciones clínicas.

## Reproducir

1. Instalar requirements.txt (entorno de ejecución probado: Python 3.14.6).
2. Ejecutar scripts/check_amplitude.py y scripts/check_statistics.py.
3. Ejecutar scripts/exploratory_amplitude.py y scripts/comprehensive_semg.py.
4. Ejecutar scripts/build_analysis_report.py para regenerar el informe y el índice local.

Los scripts verifican el ZIP por hash antes de usar los datos. Todos los participantes permanecen en el análisis principal. Reportes y perfiles son reproducibles, no una herramienta clínica validada.

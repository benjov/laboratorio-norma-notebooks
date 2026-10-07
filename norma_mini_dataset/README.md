# Mini-dataset Norma+ para el diplomado

Tres resoluciones **ficticias**, escritas con el formato de la COFECE y del PJF, para ilustrar el flujo de extracción de Norma+. Los agentes, expedientes, cifras y personas son inventados. El objetivo es didáctico: cada documento incluye a propósito los casos que cada lab necesita mostrar.

## Archivos

| Archivo | Contenido | Lab |
|---|---|---|
| `pdf/R1_COFECE_PMR_lacteos.pdf` | Investigación por práctica monopólica relativa (exclusividad en refrigeradores), 3 pp. | 1–4 |
| `pdf/R2_COFECE_CNT_farmacias.pdf` | Concentración autorizada con condiciones (desinversión de farmacias), 2 pp. | 1–4 |
| `pdf/R3_PJF_JD_amparo_lacteos.pdf` | Amparo indirecto contra R1; concede solo respecto de la multa, 2 pp. | 1–4 |
| `taxonomia.json` | 24 nodos (`id`, `ruta_tema`), con dos nodos distractores sin criterios (T16, T20) | 2, 3 |
| `gold_criterios.csv` | 22 criterios con cita literal, página, tema, artículos y columna `duplicado_de` | 2, 3, 4 |
| `negativos_validacion.csv` | 8 fragmentos literales que NO son criterios: transcripción, hecho, valoración de prueba, argumento de parte, trámite, aplicación al caso | Validación |
| `pares_fidelidad.csv` | 6 abstracciones de criterios, etiquetadas como fieles o generalizaciones no sostenidas | Validación |
| `salidas/chunks_lab1.jsonl` | 20 chunks que produce el Lab 1; respaldo para empezar el Lab 2 sin correr el Lab 1 | 2 |
| `salidas/criterios_lab2.jsonl` | Respaldo: 29 criterios extraídos por Claude Haiku 4.5 en la corrida de ensayo (7-oct-2026), con su estado de verificación | 2b, 4 |
| `salidas/criterios_validados.jsonl` | Respaldo: los 27 verificados, con validador y gate (22 aceptados) | 4 |
| `gold_info_general.csv` | Campos estructurados por resolución (expediente, fechas, sentido, multa, monto, votación, artículos) | 4 |

## Lo que cada documento permite mostrar

- **Router por procedimiento:** tres tipos distintos (`COFECE_INV`, `COFECE_CNT`, `PJF_JD`) con secciones de nombre distinto (RESULTANDO/RESULTANDOS, RESUELVE/PUNTOS RESOLUTIVOS).
- **Zona argumentativa:** los criterios viven en los considerandos; resultandos y resolutivos sirven de contraste.
- **Pie de página repetido:** hay que limpiarlo antes de buscar citas; una cita (C07) cruza de la página 2 a la 3.
- **Deduplicación:** C11 duplica a C01 (mercado relevante) y C19 duplica a C02 (poder sustancial), con redacción distinta y en documentos distintos.
- **Validación:** R1 incluye una cláusula transcrita, hechos, valoración de facturas y el argumento de la investigada.
- **Fidelidad:** los pares de `pares_fidelidad.csv` contrastan abstracciones fieles con generalizaciones que el texto no sostiene.
- **Exactitud por campo:** R3 tiene fecha de demanda y de sentencia; R1 tiene multa; R2 tiene monto de operación y voto en contra.

## Regenerar

`python generar.py` (requiere `reportlab` y `pdfplumber`) reconstruye los PDF y recalcula la página de cada cita a partir del texto extraído.

# Laboratorio Norma+ · Notebooks para profundizar

Material de la sesión **«Del documento al dato»** (Diplomado en Ciencia de Datos e IA para Ciencias Sociales, 10 de octubre de 2026). En la sesión recorrimos el pipeline en la app [laboratorio-norma.streamlit.app](https://laboratorio-norma.streamlit.app/). Aquí está el mismo recorrido en código, para reproducirlo y modificarlo.

Cada laboratorio tiene dos versiones: la del alumno, con ejercicios por completar, y la **resuelta**.

| Laboratorio | Alumno | Resuelto |
|---|---|---|
| 1 · Del PDF a la estructura (reglas y regex, sin LLM) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab1_estructura.ipynb) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab1_estructura_resuelto.ipynb) |
| 2 · Extracción con esquema y citas verificadas | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab2_extraccion.ipynb) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab2_extraccion_resuelto.ipynb) |
| 2b · Validación y fidelidad | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab2b_validacion_fidelidad.ipynb) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab2b_validacion_fidelidad_resuelto.ipynb) |
| 3 · Deduplicación y taxonomía | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab3_dedup_taxonomia.ipynb) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab3_dedup_taxonomia_resuelto.ipynb) |
| 4 · Evaluación contra el gold y costos | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab4_evaluacion_costos.ipynb) | [Abrir en Colab](https://colab.research.google.com/github/benjov/laboratorio-norma-notebooks/blob/main/lab4_evaluacion_costos_resuelto.ipynb) |

Se recomienda seguirlos en orden, aunque cada uno corre por separado: en Colab cada notebook vive en su propia máquina, así que `norma_mini_dataset/salidas/` trae de respaldo lo que producen los Labs 1, 2 y 2b (con respuestas reales de Claude Haiku 4.5). Si corres un lab, sus salidas reemplazan al respaldo en esa sesión.

## Antes de empezar

1. **Tu API key de Anthropic.** En Colab, abre el panel 🔑 **Secrets** (barra izquierda), crea un secreto llamado `ANTHROPIC_API_KEY`, pega tu key y activa el acceso del notebook. El Lab 1 no la necesita.
2. **Los datos se descargan solos.** La primera celda clona este repositorio y copia `norma_mini_dataset/`. Si falla, descarga el repositorio como zip, comprime la carpeta `norma_mini_dataset` y súbela cuando el notebook lo pida.
3. **Gasto.** Los notebooks usan `claude-haiku-4-5` y un guardián de presupuesto que detiene las llamadas al llegar a USD 0.50 por notebook. Las respuestas se guardan en caché: volver a correr una celda no cuesta.

## Los datos

`norma_mini_dataset/` contiene tres resoluciones **ficticias**, escritas con el formato de la COFECE y del Poder Judicial para fines didácticos, junto con su gold de criterios, fragmentos negativos etiquetados, pares de fidelidad y una taxonomía simplificada de 24 nodos. Ver su README.

Los prompts y la taxonomía son versiones simplificadas de las que usa Norma+ en producción.

## Contacto

Imanol · Norma+ · [normaplus.ai](https://normaplus.ai) · imanolrzmz@gmail.com

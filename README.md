# textolab-es

`textolab` es una herramienta de línea de comandos para análisis básico de corpus y experimentación con texto.
Proporciona utilidades para inspección estructural, estadísticas léxicas, muestreo aleatorio y generación de texto basada en modelos de Markov.

El proyecto es modular. Todas las funcionalidades están disponibles tanto desde la CLI como desde módulos importables en Python.

---

## Instalación

Clona el repositorio e instálalo en modo editable:

```bash
git clone https://github.com/gabohueck/textolab-es.git
cd textolab-es
pip install -e .
```
Luego de la instalación, el punto de entrada de la CLI estará disponible como:


```bash
textolab-es
```
---

## Uso de la CLI
```bash
textolab-es --help
```
Muestra todos los comandos disponibles y sus opciones.

---

## Comandos

`structure`
Genera una tabla desglosando la estructura de un corpus.


```bash
textolab-es structure path/to/text.txt
textolab-es structure path/to/text.txt --to_csv output.csv
textolab-es structure path/to/text.txt --to_tsv output.tsv
```
La tabla generada muestra:

- cada frase del corpus

- longitud de la frase

- formato minimalista de la frase

- formato minimalista de las categorías gramaticales (POS)

---

`sample`
Extrae una frase aleatoria de un corpus.


```bash
textolab-es sample path/to/text.txt
textolab-es sample path/to/text.txt -n 5
```

Formato de salida:
```css
Frase n de X: "..."
```
Donde:

X es el número total de frases en el corpus

n es el índice de la frase seleccionada aleatoriamente

---

`babbler` (Markov babbler)
Entrena y genera texto utilizando un modelo de Markov a partir de un corpus.

```bash
textolab-es babbler path/to/text.txt
textolab-es babbler path/to/text.txt -n 3 -N 200
```
Donde:

`-n` o `--ngram` corresponde a la orden o tamaño del n-grama del modelo de Markov (default: 2)

`-N` o `--length` corresponde al tamaño del texto a ser generado (default: 50)

El entrenamiento y la generación están implementados en la clase MarkovBabbler

---

`describe`
Genera una descripción general del corpus.

```bash
textolab-es describe path/to/text.txt
```
Revela:

- número total de tokens

- número de tokens únicos

- razón type–token

- palabras más frecuentes (excluyendo partículas comunes)

- número de frases

- longitud promedio, mínima y máxima de frases

- proporción de categorías gramaticales (POS)

Devuelve:

- un diccionario (internamente)

- un reporte formateado

---

## API en Python
Toda la funcionalidad de la CLI está respaldada por módulos importables:

```python
from textolab.phraser import tokenize_text
from textolab.structure import text_to_structure
from textolab.describe import describe_corpus
from textolab.markov_babbler import MarkovBabbler
```
Estos módulos pueden ser reutilizados en notebooks, scripts o proyectos externos.

---

## Estructura del proyecto
```bash
textolab/
├── cli.py               # Definición de la CLI
├── phraser.py           # Tokenización y manejo de frases
├── structure.py         # Análisis estructural y POS
├── describe.py          # Estadísticas a nivel de corpus
├── markov_babbler.py    # Generación de texto con Markov
```
---

## Requisitos
Python ≥ 3.8

Librerías: {"nltk","spacy","pandas"}

Las dependencias están especificadas en `pyproject.toml`

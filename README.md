# Chess Games Data Pipeline

Este proyecto extrae datos de partidas desde la API de Lichess y construye un pequeño pipeline de datos para transformarlos y almacenarlos para un posterior análisis.

El pipeline recupera las partidas de un usuario específico, limpia y reestructura el dataset, y finalmente lo carga tanto en un archivo CSV como en una base de datos SQLite. Una etapa adicional transforma los datos para que estén centrados en la perspectiva del jugador, facilitando el análisis del rendimiento personal.

### Tecnologías

- Python

- pandas

- requests

- NumPy

- SQLite

### Fuente de Datos

Los datos se obtienen a través de la API de Lichess, que devuelve respuestas en formato NDJSON.

Durante la extracción se aplican varios filtros:

- Solo partidas clasificadas (rated)
- Solo partidas provenientes del matchmaking pool
- Tipos de partida: bullet, blitz, rapid y classical

Esto excluye partidas contra bots o partidas privadas con amigos.

### Estructura del Pipeline

El pipeline se compone de tres etapas principales.

#### 1. Extracción de Datos

`extract_games.py` se conecta a la API de Lichess y recupera el historial de partidas del usuario.

Dado que la API devuelve datos en **NDJSON**, cada línea se procesa individualmente y luego se convierte en un DataFrame de pandas.

El dataset sin procesar se guarda en:

```
data/raw_data.csv
```

#### 2. Transformación de Datos

`transform_data.py` toma el dataset crudo y realiza varios pasos de limpieza y reestructuración:

- Eliminación de columnas redundantes (`clock`, `rated`, `perf`)
- Aplanamiento de estructuras JSON anidadas
- Expansión de campos tipo diccionario en columnas
- Limpieza general de datos

El dataset resultante se guarda en:

```
data/clean_data.csv
```

#### 3. Transformación a Perspectiva del Jugador

El módulo `to_personal_data.py` convierte el dataset desde un formato neutral de partida a una vista centrada en el jugador.

Algunos ejemplos de transformaciones incluyen:

- Conversión de *winner* a *who_won* (*player*, *opponent* o *draw*)
- Separación del rating del jugador y del oponente
- Simplificación de campos de fecha
- Eliminación de columnas adicionales redundantes

Este paso hace que el dataset sea más fácil de analizar desde la perspectiva del usuario de Lichess seleccionado.

El dataset resultante se guarda en:

```
data/personal_games.csv
```

Además, una copia se carga en una base de datos SQLite para permitir consultas estructuradas.

### Ejecución

```bash
pip install -r requirements.txt
python main.py
```
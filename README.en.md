[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/JSelemin/chess_analytics/blob/main/README.md)

# Chess Games Data Pipeline

This project extracts game data from the Lichess API and builds a small data pipeline to transform and store it for later analysis. The pipeline retrieves games from a specific user, cleans and restructures the dataset, and loads it into both a CSV file and a SQLite database. An additional step transforms the data into a player-centric perspective, making it easier to analyze personal performance.

### Technologies

- Python

- pandas

- requests

- NumPy

- SQLite

## Data Source

The data is retrieved from the Lichess API, which returns responses in NDJSON format.

During extraction, several filters are applied:

- Only rated games
- Only games from the matchmaking pool
- Game types: bullet, blitz, rapid, and classical

This excludes games against bots or private matches with friends.

## Pipeline Structure

The pipeline consists of three main stages.

#### 1. Data Extraction

`extract_games.py` connects to the Lichess API and retrieves the user's game history.

Since the API returns data in NDJSON format, each line is processed individually and then converted into a pandas DataFrame.

The raw dataset is saved as:

```
data/raw_data.csv
```

#### 2. Data Transformation

`transform_data.py` takes the raw dataset and performs several cleaning and restructuring steps:

- Removal of redundant columns (`clock`, `rated`, `perf`)
- Flattening of nested JSON structures
- Expansion of dictionary-like fields into columns
- General data cleaning

The resulting dataset is saved as:

```
data/clean_data.csv
```

#### 3. Player Perspective Transformation

The `to_personal_data.py` module converts the dataset from a neutral game format into a player-centric view.

Examples of transformations include:

- Converting *winner* into *who_won* (*player*, *opponent*, or *draw*)
- Separating player and opponent ratings
- Simplifying date fields
- Removing additional redundant columns

This step makes the dataset easier to analyze from the perspective of the selected Lichess user.

The resulting dataset is saved as:

```
data/personal_games.csv
```

A copy is also loaded into a SQLite database to allow structured queries.

## Execution

```bash
pip install -r requirements.txt
python main.py
```
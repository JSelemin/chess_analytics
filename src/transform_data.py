import pandas as pd
import ast
import sqlite3

from src.to_personal_data import transformDF
from src.extract_games import USER

def transform_and_load():

    """
    Transforms data and loads it into SQLite 

    """

    raw_csv_path = './data/raw_lichess_games.csv'
    clean_csv_path = './data/clean_lichess_games.csv'
    personal_csv_path = './data/personal_games.csv'

    df_clean = pd.read_csv(raw_csv_path)

    #Explode dicts and other semi-structured JSON data
    df_clean['opening'] = df_clean["opening"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) 
        else x
    )
    df_opening = pd.json_normalize(df_clean['opening'])
    df_clean = df_clean.join(df_opening)

    df_clean['players'] = df_clean["players"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) 
        else x
    )
    df_players = pd.json_normalize(df_clean['players'])
    df_clean = df_clean.join(df_players)

    #Drop irrelevant columns
    df_clean = df_clean.drop(
        columns=['rated',
                'variant',
                'clock',
                'source',
                'perf',
                'lastMoveAt',
                "players",
                "opening",
                "eco",
                "white.user.name",
                "white.provisional",
                "white.analysis.inaccuracy",
                "white.analysis.mistake",
                "white.analysis.blunder",
                "white.analysis.acpl",
                "black.user.name",
                "black.provisional",
                "black.analysis.inaccuracy",
                "black.analysis.mistake",
                "black.analysis.blunder",
                "black.analysis.acpl",
                "black.user.flair",
                "white.user.flair",
                "ply",
                "tournament",
                "black.user.patron",
                "black.user.patronColor",
                "white.user.patron",
                "white.user.patronColor"
    ],
        errors='ignore'
        )

    df_clean.to_csv(clean_csv_path)

    #Transform the same data into a personal perspective

    df_personal = transformDF(df_clean, USER)
    print(df_personal.head())
    df_personal.to_csv(personal_csv_path)


    conn = sqlite3.connect('./data/chess_data.sqlite')
    df_personal.to_sql('user_perspective', conn, if_exists='replace', index=False)
    #test
    print("Transform data done---")
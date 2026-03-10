import requests
import json
import pandas as pd

USER = "selemin"
URL = f"https://lichess.org/api/games/user/{USER}"

params = {
    "max": 1000,
    "perfType": 'bullet,blitz,rapid,classical',
    "opening": True,
    "accuracy": True,
    "moves": False,
    "rated": True
}

headers = {
    "Accept": "application/x-ndjson"
}

def fetch_games():

    """
    Extracts data from the Lichess API and saves it as a raw CSV file

    """

    response = requests.get(URL, params= params, headers= headers)

    txt = response.text

    x = txt.splitlines()

    y = []

    for i in x:
        z = json.loads(i)
        y.append(z)

    raw_df = pd.DataFrame(y)

    path = "./data/raw_lichess_games.csv"

    print(raw_df.head())
    raw_df.to_csv(path, index=False)

    #test
    print("Extract games done---")
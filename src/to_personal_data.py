import pandas as pd
import numpy as np

def transformDF(dataf, username):

    """
    Add player's perspective into the data

    Args: One dataframe and the username
    Returns: Transformed dataframe 

    """

    df = pd.DataFrame(dataf)
    
    #Add draws to winner column
    df['winner'] = df['winner'].fillna('draw')

    #Add perspective to color
    df['player_color'] = 'white'
    df.loc[df['black.user.id'] == username, 'player_color'] = 'black'

    #Add perspective to winner
    df['who_won'] = 'opponent'

    df.loc[(df['winner'] == 'white') & (df['white.user.id'] == username), 'who_won'] = 'player'
    df.loc[(df['winner'] == 'black') & (df['black.user.id'] == username), 'who_won'] = 'player'
    df.loc[df['winner'] == 'draw', 'who_won'] = 'draw'

    #Add perspective to rating
    df['player_rating_before_match'] = np.nan

    df.loc[df['player_color'] == 'white', 'player_rating_before_match'] = df['white.rating']
    df.loc[df['player_color'] == 'black', 'player_rating_before_match'] = df['black.rating']
    
    #Add perspective to accuracy
    df['player_accuracy'] = np.nan

    df.loc[df['player_color'] == 'white', 'player_accuracy'] = df['white.analysis.accuracy']
    df.loc[df['player_color'] == 'black', 'player_accuracy'] = df['black.analysis.accuracy']

    #Add perspective to opponent
    df['opponent_rating_before_match'] = np.nan

    df.loc[df['player_color'] == 'white', 'opponent_rating_before_match'] = df['black.rating']
    df.loc[df['player_color'] == 'black', 'opponent_rating_before_match'] = df['white.rating']

    df['opponent_accuracy'] = np.nan

    df.loc[df['player_color'] == 'white', 'opponent_accuracy'] = df['black.analysis.accuracy']
    df.loc[df['player_color'] == 'black', 'opponent_accuracy'] = df['white.analysis.accuracy']

    #Add no analysis to rows with corresponding NAs
    df['player_accuracy'] = df['player_accuracy'].fillna('no_analysis')
    df['opponent_accuracy'] = df['opponent_accuracy'].fillna('no_analysis')


    #Convert time
    df['createdAt'] = pd.to_datetime(df['createdAt'], unit='ms')

    #Drop unnecessary columns
    df = df.drop(columns=[
        'winner',
        'white.rating',
        'black.rating',
        'white.ratingDiff',
        'black.ratingDiff',
        'white.analysis.accuracy',
        'black.analysis.accuracy'
    ])

    #Rename columns for clarity
    df = df.rename(columns={"name": "opening_played",
                    "id": "lichess_id",
                    "status": "result", 
                    "white.user.id": "white_username",
                    "black.user.id": "black_username",
                    "createdAt": "game_date",
                    "speed": "format"
                    })

    df.index.name = 'id'
    #test
    print("To personal data done---")
    return df
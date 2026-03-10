from src.extract_games import fetch_games
from src.transform_data import transform_and_load

def main():
    fetch_games()
    transform_and_load()



if __name__ == "__main__":
    main()
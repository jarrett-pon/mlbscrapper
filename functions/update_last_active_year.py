"""Get/update last active year for all players."""
import requests

from classes.database import Database

BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
YEARS_PLAYED_EXT = (
    "named.comp_player_has_stats_game_type.bam?"
    "league_list_id='mlb_hist'&player_id="
)
# Get players with no active years
GET_PLAYERS = ("SELECT id, mlb_id FROM players WHERE last_active_year IS NULL")
SET_LAST_ACTIVE_YEAR = (
    "UPDATE players SET last_active_year = %s WHERE id = %s"
)


def update_last_active_year():
    """Find and adds players last active year, 0 otherwise."""
    db = Database()
    database_players = db.query(GET_PLAYERS)
    db.__del__

    all_last_active_year_players = []

    for player in database_players:
        players_id = player[0]
        player_mlb_id = player[1]
        link = BASE_URL + YEARS_PLAYED_EXT + str(player_mlb_id)
        response = requests.get(link).json()
        try:
            game_types_results = (
                response["comp_player_has_stats_game_type"]
                ["player_season_game_type"]["queryResults"]
            )
        except KeyError:
            print("Could not find game_type_results")
            print(players_id)
            continue
        game_types_count = game_types_results["totalSize"]
        if game_types_count == "0":
            years_played = []
        elif (game_types_count == "1" and
                game_types_results["row"]["game_type"] == "R"):
            years_played = [game_types_results["row"]["season"]]
        elif game_types_count != "1":
            years_played = [game_type["season"]
                            for game_type
                            in game_types_results["row"]
                            if game_type["game_type"] == "R"]
        else:
            years_played = []
        print(years_played)
        last_active_year = max(years_played) if len(years_played) > 0 else 0
        all_last_active_year_players.append((last_active_year, players_id))

    print("Players with last active year update", all_last_active_year_players)
    db = Database()
    db.insert(SET_LAST_ACTIVE_YEAR, all_last_active_year_players, many=True)

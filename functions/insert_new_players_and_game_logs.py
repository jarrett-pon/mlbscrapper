"""Get player info for all active players then get their primary stat type."""
import requests

from classes.database import Database
from functions.get_active_players import get_active_players
from functions.insert_game_logs import insert_game_logs
from functions.update_last_active_year import update_last_active_year

# Api Url Constants
BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
PRIMARY_STAT_TYPE_EXT = "named.player_teams.bam?player_id="
# MySQL query constants
GET_ALL_PLAYERS = ("SELECT mlb_id FROM players")
GET_NEW_PLAYERS = (
    "SELECT id, mlb_id, primary_stat_type FROM players WHERE mlb_id IN (%s)"
)
ADD_PLAYERS = (
    "INSERT INTO players (mlb_name, mlb_id, teams_id, primary_stat_type)"
    " VALUES (%s, %s, %s, %s)"
)


def insert_new_players_and_game_logs():
    """Find all new players and insert their game logs."""
    # Get current active players on each team's 40 man roster
    current_player_info = get_active_players()

    # Connect to mysql database
    db = Database()
    # Get all current players in DB
    all_database_players = db.query(GET_ALL_PLAYERS)
    # Unpack list of tuples to list
    all_database_players = [player[0] for player in all_database_players]
    # Only add players that weren't already in the DB based on mlb id
    current_player_info = [player
                           for player
                           in current_player_info
                           if int(player[0]) not in all_database_players]

    all_player_data = []
    # Grab player primary stat type
    for player_info in current_player_info:
        player_id = player_info[0]
        player_name = player_info[1]
        team_id = player_info[2]

        link = BASE_URL + PRIMARY_STAT_TYPE_EXT + player_id
        response = requests.get(link).json()
        results = response["player_teams"]["queryResults"]
        size = results["totalSize"]

        if(size is "0"):
            primary_stat_type = 'unknown'
        elif(size is "1"):
            primary_stat_type = results["row"]["primary_stat_type"]
        else:
            primary_stat_type = results["row"][0]["primary_stat_type"]

        player_data = (player_name, player_id, team_id, primary_stat_type)
        all_player_data.append(player_data)

    print("New Players", all_player_data)
    db.insert(ADD_PLAYERS, all_player_data, many=True)

    all_player_id = [player[1] for player in all_player_data]

    # Format to use SELECT WHERE IN
    new_database_players = []
    if(len(all_player_id) > 0):
        format_strings = ",".join(["%s"] * len(all_player_id))
        query = GET_NEW_PLAYERS % format_strings
        new_database_players = db.query(query, tuple(all_player_id))

    update_last_active_year()
    insert_game_logs(new_database_players)

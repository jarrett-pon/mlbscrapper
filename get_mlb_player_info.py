# Get player id/name for all active players then get their primary stat type
import requests

from classes.database import Database
from functions.get_active_players import get_active_players

# Api Url Constants
BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
PRIMARY_STAT_TYPE_EXT = "named.player_teams.bam?player_id="
# MySQL query constants
GET_PLAYERS = ("SELECT mlb_id FROM players")
ADD_PLAYERS = ("INSERT INTO players (mlb_name, mlb_id, teams_id, primary_stat_type) VALUES (%s, %s, %s, %s)")

# Get current active players on each team's 40 man roster
current_player_info = get_active_players()

# Connect to mysql database
db = Database()
# Get all current players in DB
database_players = db.query(GET_PLAYERS)
# Unpack list of tuples to list
database_players = [player[0] for player in database_players]
# Only add players that weren't already in the DB based on mlb id
current_player_info = [player for player in current_player_info if int(player[0]) not in database_players ]

all_player_data = []
# Grab player primary stat type
for player_info in current_player_info:
    player_id = player_info[0]
    player_name = player_info[1]
    team_id = player_info[2]

    response = requests.get(BASE_URL + PRIMARY_STAT_TYPE_EXT + player_id).json()
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

db.insert(ADD_PLAYERS, all_player_data, many=True)

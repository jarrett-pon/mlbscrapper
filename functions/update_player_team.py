"""Script to check all the mlb players teams are correct."""
from classes.database import Database

from functions.get_active_players import get_active_players

GET_PLAYERS = (
    "SELECT teams.id AS teams_id, players.mlb_id AS players_mlb_id"
    " FROM players"
    " JOIN teams ON teams.id = players.teams_id"
)
SET_PLAYER = ("UPDATE players SET teams_id = %s WHERE mlb_id = %s")


def update_player_team():
    """Get all active players and makes sure they are on correct team."""
    # Get current active players on each team's 40 man roster
    current_player_info = get_active_players()
    # Current players need to be in list of tuples
    # with (teams_id, players_mlb_id)
    current_player_info = [(int(player[2]), int(player[0]))
                           for player
                           in current_player_info]
    # Connect to mysql database
    db = Database()
    # Get all current players in DB
    database_players = db.query(GET_PLAYERS)
    # Players that changed teams
    changed_players = set(current_player_info) - set(database_players)

    print("Players with updated team", changed_players)
    for player in changed_players:
        db.insert(SET_PLAYER, player)

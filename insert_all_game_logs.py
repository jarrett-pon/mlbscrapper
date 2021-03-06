"""Get game logs for all players."""
from classes.database import Database
from functions.insert_game_logs import insert_game_logs

GET_PLAYERS = ("SELECT id, mlb_id, primary_stat_type FROM players")

# Connect to mysql database
db = Database()
# Get all current players in DB
database_players = db.query(GET_PLAYERS)

insert_game_logs(database_players)

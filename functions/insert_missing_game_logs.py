"""Check for players with missed game logs and get the game logs."""
from classes.database import Database
from functions.insert_game_logs import insert_game_logs

GET_HITTERS_MISSING_LOGS = (
    "SELECT p.id, p.mlb_id, p.primary_stat_type FROM players p"
    " LEFT JOIN game_logs_hitting glh ON p.id = glh.players_id"
    " AND glh.game_year = p.last_active_year"
    " WHERE p.primary_stat_type = 'hitting' AND p.last_active_year > 0"
    " GROUP BY p.id"
    " HAVING COUNT(glh.id) = 0"
)

GET_PITCHERS_MISSING_LOGS = (
    "SELECT p.id, p.mlb_id, p.primary_stat_type FROM players p"
    " LEFT JOIN game_logs_pitching glp ON p.id = glp.players_id"
    " AND glp.game_year = p.last_active_year"
    " WHERE p.primary_stat_type = 'pitching' AND p.last_active_year > 0"
    " GROUP BY p.id"
    " HAVING COUNT(glp.id) = 0"
)
# Special both type can only be manually added.
# Only time it is checked is here (not initially adding player/game logs)
GET_BOTH_MISSING_LOGS = (
    "SELECT p.id, p.mlb_id, p.primary_stat_type FROM players p"
    " LEFT JOIN game_logs_pitching glp ON p.id = glp.players_id"
    " AND glp.game_year = p.last_active_year"
    " LEFT JOIN game_logs_hitting glh ON p.id = glh.players_id"
    " AND glh.game_year = p.last_active_year"
    " WHERE p.primary_stat_type = 'both' AND p.last_active_year > 0"
    " GROUP BY p.id"
    " HAVING COUNT(glp.id) = 0 AND COUNT(glh.id) = 0"
)


def insert_missing_game_logs():
    """Get players that don't have their game logs and insert them."""
    db = Database()
    # Get duplicate game logs in DB
    hitters_missing_game_logs = db.query(GET_HITTERS_MISSING_LOGS)
    print("Hitters missing game logs:", hitters_missing_game_logs)
    pitchers_missing_game_logs = db.query(GET_PITCHERS_MISSING_LOGS)
    print("Pitchers missing game logs:", pitchers_missing_game_logs)
    both_missing_game_logs = db.query(GET_BOTH_MISSING_LOGS)
    print("Both missing game logs:", both_missing_game_logs)

    missing_game_logs = (
        hitters_missing_game_logs + pitchers_missing_game_logs +
        both_missing_game_logs
    )
    insert_game_logs(missing_game_logs)

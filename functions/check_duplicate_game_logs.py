"""Check for duplicate game logs, will need manual SQL after check."""
from classes.database import Database

GET_DUPLICATE_PITCHERS = ("SELECT players_id, game_id, COUNT(*)"
                          " FROM game_logs_pitching"
                          " GROUP BY players_id, game_id"
                          " HAVING COUNT(*) > 1")

GET_DUPLICATE_HITTERS = ("SELECT players_id, game_id, COUNT(*)"
                         " FROM game_logs_hitting"
                         " GROUP BY players_id, game_id"
                         " HAVING COUNT(*) > 1")


def check_duplicate_game_logs():
    """Check for duplicate game logs."""
    db = Database()
    # Get duplicate game logs in DB
    duplicate_pitchers = db.query(GET_DUPLICATE_PITCHERS)
    print("Duplicate Pitchers:", duplicate_pitchers)
    duplicate_hitters = db.query(GET_DUPLICATE_HITTERS)
    print("Duplicate Hitters:", duplicate_hitters)

    return [duplicate_pitchers, duplicate_hitters]

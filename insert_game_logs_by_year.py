"""Script to update all game logs by year."""
import sys
import requests
from classes.database import Database
from functions.new_game_logs import new_game_logs
from functions.check_duplicate_game_logs import check_duplicate_game_logs

BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
GAME_LOG_EXT = (
    "named.sport_%s_game_log_composed.bam"
    "?game_type='R'&league_list_id='mlb_hist'&player_id=%s&season=%s"
)
GET_PLAYERS = (
    "SELECT id, mlb_id, primary_stat_type"
    " FROM players"
    " ORDER BY id"
)
GET_GAME_LOGS_HITTING = (
    "SELECT players_id, mlb_team_id, opponent_mlb_team_id, game_date, ab, r,"
    " h, tb, 2b, 3b, hr, rbi, bb, ibb,so, sb ,cs ,hbp, sac, sf, home_away,"
    " game_id, game_year"
    " FROM game_logs_hitting"
    " WHERE game_year = %s"
    " ORDER BY players_id, game_id"
)
GET_GAME_LOGS_PITCHING = (
    "SELECT players_id, mlb_team_id, opponent_mlb_team_id, game_date, g, gs,"
    " cg, sho, sv, svo, ip, h, r, er, hr, bb, ibb, so, np, s , w, l,"
    " home_away, game_id, game_year"
    " FROM game_logs_pitching"
    " WHERE game_year = %s"
    " ORDER BY players_id, game_id"
)
ADD_GAME_LOGS_HITTING = (
    "INSERT INTO game_logs_hitting"
    " (players_id, mlb_team_id, opponent_mlb_team_id, game_date, ab, r, h, tb,"
    " 2b, 3b, hr, rbi, bb, ibb, so, sb, cs, hbp, sac, sf, home_away, game_id,"
    " game_year)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
    " %s, %s, %s, %s, %s, %s, %s)"
)
ADD_GAME_LOGS_PITCHING = (
    "INSERT INTO game_logs_pitching"
    " (players_id, mlb_team_id, opponent_mlb_team_id, game_date, g, gs, cg,"
    " sho, sv, svo, ip, h, r, er, hr, bb, ibb, so, np, s , w, l, home_away,"
    " game_id, game_year)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
    " %s, %s, %s, %s, %s, %s, %s, %s, %s)")


# database_players comes in as a list with tuple/list structure:
# (id, mlb_id, primary_stat_type)
def insert_game_logs_by_year(year):
    [duplicate_pitchers, duplicate_hitters] = check_duplicate_game_logs()

    if (len(duplicate_pitchers) > 0 or len(duplicate_hitters) > 0):
        return

    """Insert only new game logs by year."""
    db = Database()
    database_players = db.query(GET_PLAYERS)
    db.__del__

    all_pitching_game_log_data = []
    all_hitting_game_log_data = []

    for player in database_players:
        players_id = player[0]
        player_mlb_id = player[1]
        primary_stat_type = player[2]
        if (primary_stat_type == "pitching" or primary_stat_type == "both"):
            link = BASE_URL + GAME_LOG_EXT % ("pitching", player_mlb_id, year)
            response = requests.get(link).json()
            try:
                pitching_log_results = (
                    response["sport_pitching_game_log_composed"]
                    ["sport_pitching_game_log"]["queryResults"]
                )
            except KeyError:
                print("Could not find pitching_log_results")
                print(link)
                print(players_id)
                print(year)
                return
            game_logs_count = pitching_log_results["totalSize"]
            if game_logs_count == "0":
                game_logs = []
            else:
                game_logs = pitching_log_results["row"]
                game_logs = (
                    [game_logs] if game_logs_count == "1" else game_logs
                )
            for game_log in game_logs:
                year = game_log["game_date"].split('-')[0]
                game_log_data = (
                    players_id, game_log["team_id"], game_log["opponent_id"],
                    game_log["game_date"], game_log["g"], game_log["gs"],
                    game_log["cg"], game_log["sho"], game_log["sv"],
                    game_log["svo"], game_log["ip"], game_log["h"],
                    game_log["r"], game_log["er"], game_log["hr"],
                    game_log["bb"], game_log["ibb"], game_log["so"],
                    game_log["np"], game_log["s"], game_log["w"],
                    game_log["l"], game_log["home_away"], game_log["game_id"],
                    year
                )
                all_pitching_game_log_data.append(game_log_data)
        if (primary_stat_type == "hitting" or primary_stat_type == "both"):
            link = BASE_URL + GAME_LOG_EXT % ("hitting", player_mlb_id, year)
            response = requests.get(link).json()
            try:
                hitting_log_results = (
                    response["sport_hitting_game_log_composed"]
                    ["sport_hitting_game_log"]["queryResults"]
                )
            except KeyError:
                print("Could not find hitting_log_results")
                print(link)
                print(players_id)
                print(year)
                return
            game_logs_count = hitting_log_results["totalSize"]
            if game_logs_count == "0":
                game_logs = []
            else:
                game_logs = hitting_log_results["row"]
                game_logs = (
                    [game_logs] if game_logs_count == "1" else game_logs
                )
            for game_log in game_logs:
                year = game_log["game_date"].split('-')[0]
                game_log_data = (
                    players_id, game_log["team_id"], game_log["opponent_id"],
                    game_log["game_date"], game_log["ab"], game_log["r"],
                    game_log["h"], game_log["tb"], game_log["d"],
                    game_log["t"], game_log["hr"], game_log["rbi"],
                    game_log["bb"], game_log["ibb"], game_log["so"],
                    game_log["sb"], game_log["cs"], game_log["hbp"],
                    game_log["sac"], game_log["sf"], game_log["home_away"],
                    game_log["game_id"], year
                )
                all_hitting_game_log_data.append(game_log_data)

    db = Database()
    database_pitching_game_log_data = db.query(GET_GAME_LOGS_PITCHING, (year,))
    database_hitting_game_log_data = db.query(GET_GAME_LOGS_HITTING, (year,))

    new_pitching_game_log_data = new_game_logs(all_pitching_game_log_data,
                                               database_pitching_game_log_data,
                                               23)
    new_hitting_game_log_data = new_game_logs(all_hitting_game_log_data,
                                              database_hitting_game_log_data,
                                              21)

    new_game_log_count = (
        len(new_pitching_game_log_data) + len(new_hitting_game_log_data)
    )
    print("Number of new game logs", new_game_log_count)
    db.insert(ADD_GAME_LOGS_PITCHING, new_pitching_game_log_data, many=True)
    db.insert(ADD_GAME_LOGS_HITTING, new_hitting_game_log_data, many=True)

    check_duplicate_game_logs()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
    elif not sys.argv[1].isdigit():
        print("Argument should be a year (digit)")
    else:
        year = sys.argv[1]
        insert_game_logs_by_year(year)

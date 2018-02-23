"""Give list of players, return all related game logs."""
import requests
from classes.database import Database

BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
YEARS_PLAYED_EXT = (
    "named.comp_player_has_stats_game_type.bam?"
    "league_list_id='mlb_hist'&player_id="
)
GAME_LOG_EXT = (
    "named.sport_%s_game_log_composed.bam?"
    "game_type='R'&league_list_id='mlb_hist'&"
    "player_id=%s&season=%s"
)
ADD_GAME_LOGS_PITCHING = (
    "INSERT INTO game_logs_pitching"
    " (players_id, mlb_team_id, opponent_mlb_team_id, game_date, g, gs, cg,"
    " sho, sv, svo, ip, h, r, er, hr, bb, ibb, so, np, s , w, l, home_away,"
    " game_id, game_year)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
    " %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)
ADD_GAME_LOGS_HITTING = (
    "INSERT INTO game_logs_hitting"
    " (players_id, mlb_team_id, opponent_mlb_team_id, game_date, ab, r, h, tb,"
    " 2b, 3b, hr, rbi, bb, ibb, so, sb, cs, hbp, sac, sf, home_away, game_id,"
    " game_year)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
    " %s, %s, %s, %s, %s, %s, %s)"
)


# database_players comes in as a list with tuple/list structure:
# (id, mlb_id, primary_stat_type)
def insert_game_logs(database_players):
    """Insert ALL game logs for a given player."""
    all_pitching_game_log_data = []
    all_hitting_game_log_data = []

    for player in database_players:
        players_id = player[0]
        player_mlb_id = player[1]
        primary_stat_type = player[2]
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
            continue
        game_types = game_types_results["row"]
        if game_types_count == "1" and game_types["game_type"] == "R":
            years_played = [game_types["season"]]
        elif game_types_count != "1":
            years_played = [game_type["season"]
                            for game_type
                            in game_types if game_type["game_type"] == "R"]
        else:
            continue
        for year in years_played:
            if (primary_stat_type == "pitching" or
                    primary_stat_type == "both"):
                link = BASE_URL + \
                    GAME_LOG_EXT % ("pitching", player_mlb_id, year)
                response = requests.get(link).json()
                try:
                    pitching_log_results = (
                        response["sport_pitching_game_log_composed"]
                        ["sport_pitching_game_log"]["queryResults"]
                    )
                except KeyError:
                    print("Could not find pitching_log_results")
                    print(players_id)
                    print(year)
                    continue
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
                        players_id, game_log["team_id"],
                        game_log["opponent_id"], game_log["game_date"],
                        game_log["g"], game_log["gs"], game_log["cg"],
                        game_log["sho"], game_log["sv"], game_log["svo"],
                        game_log["ip"], game_log["h"], game_log["r"],
                        game_log["er"], game_log["hr"], game_log["bb"],
                        game_log["ibb"], game_log["so"], game_log["np"],
                        game_log["s"], game_log["w"], game_log["l"],
                        game_log["home_away"], game_log["game_id"], year
                    )
                    all_pitching_game_log_data.append(game_log_data)
            if (primary_stat_type == "hitting" or primary_stat_type == "both"):
                link = BASE_URL + \
                    GAME_LOG_EXT % ("hitting", player_mlb_id, year)
                response = requests.get(link).json()
                try:
                    hitting_log_results = (
                        response["sport_hitting_game_log_composed"]
                        ["sport_hitting_game_log"]["queryResults"]
                    )
                except KeyError:
                    print("Could not find hitting_log_results")
                    print(players_id)
                    print(year)
                    continue
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
                        players_id, game_log["team_id"],
                        game_log["opponent_id"], game_log["game_date"],
                        game_log["ab"], game_log["r"], game_log["h"],
                        game_log["tb"], game_log["d"], game_log["t"],
                        game_log["hr"], game_log["rbi"], game_log["bb"],
                        game_log["ibb"], game_log["so"], game_log["sb"],
                        game_log["cs"], game_log["hbp"], game_log["sac"],
                        game_log["sf"], game_log["home_away"],
                        game_log["game_id"], year
                    )
                    all_hitting_game_log_data.append(game_log_data)

    new_game_log_count = (
        len(all_pitching_game_log_data) + len(all_hitting_game_log_data)
    )
    print("Number of new game logs", new_game_log_count)
    db = Database()
    db.insert(ADD_GAME_LOGS_PITCHING, all_pitching_game_log_data, many=True)
    db.insert(ADD_GAME_LOGS_HITTING, all_hitting_game_log_data, many=True)

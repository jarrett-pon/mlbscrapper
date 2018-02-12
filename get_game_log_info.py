# TODO: Get all active regular season years from:
# http://lookup-service-prod.mlb.com/json/named.comp_player_has_stats_game_type.bam?player_id=533167&league_list_id=%27mlb_hist%27
# TODO: Get all game logs from
# http://lookup-service-prod.mlb.com/json/named.sport_pitching_game_log_composed.bam?game_type=%27R%27&league_list_id=%27mlb_hist%27&player_id=501625&season=2017
# http://lookup-service-prod.mlb.com/json/named.sport_hitting_game_log_composed.bam?game_type=%27R%27&league_list_id=%27mlb_hist%27&player_id=446359&season=2017

# Update game logs for all players
import requests

from classes.database import Database

BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
YEARS_PLAYED_EXT = "named.comp_player_has_stats_game_type.bam?league_list_id='mlb_hist'&player_id="

response = requests.get(BASE_URL + YEARS_PLAYED_EXT + '533167').json()
game_types = response["comp_player_has_stats_game_type"]["player_season_game_type"]["queryResults"]["row"]

years_played = [game_type["season"] for game_type in game_types if game_type["game_type"] == "R" ]
print(years_played)

# if __name__ == "__main__":
#     lock = thread.allocate_lock()
#     thread.start_new_thread(myfunction, ("Thread #: 1", 2, lock))
#     thread.start_new_thread(myfunction, ("Thread #: 2", 2, lock))

# For cmd arguments import sys and use sys.argv

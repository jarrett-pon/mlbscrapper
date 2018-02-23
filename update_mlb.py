"""Perform all general updates."""
# insert_new_players_and_game_logs, update_player_team,
# insert_missing_game_logs, check_duplicate_game_logs

from functions.insert_new_players_and_game_logs import (
    insert_new_players_and_game_logs
)
from functions.update_player_team import update_player_team
from functions.insert_missing_game_logs import insert_missing_game_logs
from functions.check_duplicate_game_logs import check_duplicate_game_logs

insert_new_players_and_game_logs()
update_player_team()
insert_missing_game_logs()
check_duplicate_game_logs()

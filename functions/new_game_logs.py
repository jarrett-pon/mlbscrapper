"""Given a two lists of game logs, find the new game logs."""
"""Search algorithm that requires the old list to be a sublist to new list
This includes both lists to be sorted the same way."""


def new_game_logs(updated_game_logs, old_game_logs, game_id_index):
    """Algorithm to get new game log with above conditions."""
    new_game_logs = []

    old_index = 0
    old_count = len(old_game_logs)
    updated_index = 0
    updated_count = len(updated_game_logs)

    while updated_index < updated_count:
        try:
            old_players_id = old_game_logs[old_index][0]
        except IndexError:
            print("Error: Old index exceeded range in old game logs")
            print("Old index: {}".format(old_index))
            print("Old count: {}".format(old_count))
            print("Updated index: {}".format(updated_index))
            print("Updated count: {}".format(updated_count))
            updated_index += 1
            continue

        updated_players_id = updated_game_logs[updated_index][0]
        old_game_id = old_game_logs[old_index][game_id_index]
        updated_game_id = updated_game_logs[updated_index][game_id_index]

        if (old_players_id == updated_players_id and
                old_game_id == updated_game_id and old_index < old_count):
            old_index += 1
        else:
            new_game_logs.append(updated_game_logs[updated_index])

        updated_index += 1

    return new_game_logs

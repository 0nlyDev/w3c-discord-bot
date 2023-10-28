from w3c_endpoints.player_stats import RACES
from w3c_endpoints.active_modes import get_game_mode_from_id


def parse_player_stats(player_stats):
    if not player_stats:
        return '🌌 The Dark Portal\'s manifest reveals no stats for this champion.'
    message = '**🛡️ Champion Stats 🛡️:**\n'
    for player_stat in player_stats:
        game_mode = get_game_mode_from_id(player_stat["gameMode"])
        if game_mode is None:
            game_mode = str(game_mode)
        _name = 'player'
        if '1vs1' not in game_mode:
            _name = 'players'
        players = ', '.join([i['name'] for i in player_stat['playerIds']])

        message += f'mode: `{game_mode}` '
        message += f'{_name}: `{players}` '
        if player_stat["race"]:
            message += f'race: `{RACES[player_stat["race"]][1]}` '
        message += f'season: `{player_stat["season"]}`\n'
        message += f'mmr: `{player_stat["mmr"]}` '
        message += f'win rate `{convert_win_rate_to_percentage(player_stat["winrate"])}` '
        message += f'w/l: `{player_stat["wins"]}:{player_stat["losses"]}` '
        message += f'games: `{player_stat["games"]}`\n\n'
    return message


def convert_win_rate_to_percentage(num):
    if 0 <= num <= 1:
        return f"{num * 100:.1f}%"
    else:
        return 0

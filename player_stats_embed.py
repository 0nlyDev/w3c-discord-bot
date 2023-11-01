from discord import Embed, SelectOption, SelectMenu

from w3c_endpoints.player_stats import RACES
from w3c_endpoints.active_modes import get_game_mode_from_id
from w3c_endpoints.player import get_player_participated_in_seasons
from w3c_endpoints.player_search import emojify_number

from discord.ui import Select, View


class MultiSelectMenu(View):
    def __init__(self, player_stats, bnet_tag):
        super().__init__()

        # Seasons menu
        participated_in_seasons = [SelectOption(label=str(emojify_number(s)), value=str(s))
                                   for s in get_player_participated_in_seasons(bnet_tag)]
        if participated_in_seasons:
            participated_in_seasons[0].default = True
            self.add_item(Select(placeholder='Choose season...', options=participated_in_seasons,
                                 custom_id="seasons_menu"))

            # Game modes menu
            game_modes = []
            game_mode_values = set()
            default_season = next((option.value for option in participated_in_seasons
                                   if getattr(option, "default", False)), None)
            default_is_set = False
            for i in player_stats:
                for k, v in i.items():
                    if k == 'gameMode':
                        game_mode = str(get_game_mode_from_id(v))
                        option = SelectOption(label=game_mode, value=game_mode)
                        if default_season and i['season'] == int(default_season) and not default_is_set:
                            option.default = default_is_set = True
                        if game_mode not in game_mode_values:
                            game_modes.append(option)
                            game_mode_values.add(game_mode)
            self.add_item(Select(placeholder='Choose game mode...', options=game_modes, custom_id="game_modes_menu"))


def get_player_stats_embed(player_stats, bnet_tag):
    if not player_stats:
        return Embed(description='🌌 The Dark Portal\'s manifest reveals no stats for this champion.'), None

    embed = Embed(title="🛡️ Champion Stats 🛡️", color=0x3498db)

    for player_stat in player_stats:
        game_mode = get_game_mode_from_id(player_stat["gameMode"])
        if game_mode is None:
            game_mode = str(game_mode)
        _name = 'player'
        if '1vs1' not in game_mode:
            _name = 'players'
        players = ', '.join([i['name'] for i in player_stat['playerIds']])

        field_name = f"Mode: {game_mode} | {_name}: {players}"
        if player_stat["race"]:
            field_name += f" | Race: {RACES[player_stat['race']][1]}"

        field_value = f"Season: {player_stat['season']}\n"
        field_value += f"MMR: {player_stat['mmr']}\n"
        field_value += f"Win Rate: {convert_win_rate_to_percentage(player_stat['winrate'])}\n"
        field_value += f"W/L: {player_stat['wins']}:{player_stat['losses']}\n"
        field_value += f"Games: {player_stat['games']}"

        embed.add_field(name=field_name, value=field_value, inline=False)
        break  # print only first occurrence

    return embed, MultiSelectMenu(player_stats, bnet_tag)


def convert_win_rate_to_percentage(num):
    if 0 <= num <= 1:
        return f"{num * 100:.1f}%"
    else:
        return 0

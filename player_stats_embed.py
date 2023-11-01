from discord import Embed, SelectOption, Interaction
from discord.ui import Select, View

from w3c_endpoints.player_stats import RACES
from w3c_endpoints.active_modes import get_game_mode_from_id
from w3c_endpoints.player import get_player_participated_in_seasons
from w3c_endpoints.player_search import emojify_number
from w3c_endpoints.player_stats import get_player_stats


def get_game_modes_for_season(bnet_tag, selected_season):
    new_player_stats = get_player_stats(bnet_tag, season=selected_season)
    print('new_player_stats', new_player_stats)
    game_modes_in_season = []
    for stats in new_player_stats:
        print(f"Checking stats: {stats}")
        if stats['season'] == int(selected_season):
            game_mode = get_game_mode_from_id(stats['gameMode'])
            print(f"Found game mode: {game_mode}")
            if game_mode not in game_modes_in_season:
                game_modes_in_season.append(game_mode)
                print(f"Added game mode to list: {game_mode}")
    print('game_modes_in_season', game_modes_in_season)
    return game_modes_in_season


class SeasonsSelectMenu(Select):
    def __init__(self, bnet_tag, player_stats, participated_in_seasons, children):
        self.bnet_tag, self.player_stats, self.participated_in_seasons, self.children = (
            bnet_tag, player_stats, participated_in_seasons, children)
        self.last_selected_season = None
        super().__init__(placeholder='Choose season...', options=participated_in_seasons, custom_id="seasons_menu")

    async def callback(self, interaction: Interaction):
        selected_season = interaction.data['values'][0]
        self.last_selected_season = selected_season
        print('selected_season', selected_season)

        # Fetch new game modes based on the selected season
        new_game_modes = get_game_modes_for_season(self.bnet_tag, selected_season)

        # Update the Select component for game modes
        game_mode_select = next((child for child in self.children if child.custom_id == "game_modes_menu"), None)
        if game_mode_select:
            game_mode_select.options = [SelectOption(label=mode, value=mode) for mode in new_game_modes]
            if new_game_modes:
                game_mode_select.options[0].default = True
                for option in self.options:
                    if option.value == self.last_selected_season:
                        option.default = True
                    else:
                        option.default = False
                await interaction.response.edit_message(view=self.view)


class GameModesSelect(Select):
    def __init__(self, player_stats, participated_in_seasons):
        game_modes = []
        game_mode_values = set()
        default_season = next((option.value for option in participated_in_seasons
                               if getattr(option, "default", False)), None)
        default_is_set = False
        for i in player_stats:
            for k, v in i.items():
                if k == 'gameMode':
                    game_mode = get_game_mode_from_id(v)
                    option = SelectOption(label=game_mode, value=game_mode)
                    if default_season and i['season'] == int(default_season) and not default_is_set:
                        option.default = default_is_set = True
                    if game_mode not in game_mode_values:
                        game_modes.append(option)
                        game_mode_values.add(game_mode)

        super().__init__(placeholder='Choose game mode...', options=game_modes, custom_id="game_modes_menu")


class MultiSelectMenu(View):
    def __init__(self, player_stats, bnet_tag):
        self.player_stats = player_stats
        super().__init__()
        participated_in_seasons = [SelectOption(label=str(emojify_number(s)), value=str(s))
                                   for s in get_player_participated_in_seasons(bnet_tag)]
        participated_in_seasons[0].default = True

        self.add_item(GameModesSelect(player_stats, participated_in_seasons))
        self.add_item(SeasonsSelectMenu(bnet_tag, player_stats, participated_in_seasons, self.children))

    def get_default_season(self):
        for item in self.children:
            if item.custom_id == "seasons_menu":
                for option in item.options:
                    if getattr(option, "default", False):
                        return int(option.value)
        return None

    def get_default_game_mode(self):
        for item in self.children:
            if item.custom_id == "game_modes_menu":
                for option in item.options:
                    if getattr(option, "default", False):
                        return option.value
        return None


def get_player_stats_embed(player_stats, bnet_tag):
    if not player_stats:
        return Embed(description='🌌 The Dark Portal\'s manifest reveals no stats for this champion.'), None

    embed = Embed(title="🛡️ Champion Stats 🛡️", color=0x3498db)

    # Create the view and get default values
    view = MultiSelectMenu(player_stats, bnet_tag)
    default_season = view.get_default_season()
    default_game_mode = view.get_default_game_mode()

    # Retrieve the specific stat based on the default values
    player_stat = next((stat for stat in player_stats if stat["season"] == default_season and
                        get_game_mode_from_id(stat["gameMode"]) == default_game_mode), None)

    if player_stat:
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

    return embed, view


def convert_win_rate_to_percentage(num):
    if 0 <= num <= 1:
        return f"{num * 100:.1f}%"
    else:
        return 0

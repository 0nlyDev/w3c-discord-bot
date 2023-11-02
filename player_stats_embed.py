from discord import Embed, SelectOption, Interaction
from discord.ui import Select, View

from w3c_endpoints.player_stats import RACES
from w3c_endpoints.active_modes import get_game_mode_from_id
from w3c_endpoints.player import get_player_participated_in_seasons
from w3c_endpoints.player_search import emojify_number
from w3c_endpoints.player_stats import get_player_stats


def get_new_game_modes_and_player_stats_by_season(bnet_tag, selected_season):
    new_player_stats = get_player_stats(bnet_tag, season=selected_season)
    game_modes_in_season = []
    for stats in new_player_stats:
        if stats['season'] == int(selected_season):
            game_mode = get_game_mode_from_id(stats['gameMode'])
            if game_mode not in game_modes_in_season:
                game_modes_in_season.append(game_mode)
    return game_modes_in_season, new_player_stats


class SeasonsSelectMenu(Select):
    def __init__(self, bnet_tag, player_stats, participated_in_seasons, children, game_modes_select):
        self.bnet_tag, self.player_stats, self.children, self.game_modes_select = (
            bnet_tag, player_stats, children, game_modes_select)
        self.selected_season = None
        super().__init__(placeholder='Choose season...', options=participated_in_seasons, custom_id='seasons_menu')

    async def callback(self, interaction: Interaction):
        self.selected_season = interaction.data['values'][0]

        # Fetch new game modes and player stats based on the selected season
        new_game_modes, self.player_stats = get_new_game_modes_and_player_stats_by_season(
            self.bnet_tag, self.selected_season)
        # Update the player_stats in the game_modes_select here
        self.game_modes_select.player_stats = self.player_stats

        # Update the game_modes_menu
        game_mode_select = next((child for child in self.children if child.custom_id == 'game_modes_menu'), None)
        game_mode_select.options = [SelectOption(label=mode, value=mode) for mode in new_game_modes]
        game_mode_select.options[0].default = True
        for option in self.options:  # Update the season select menu with the user choice
            if option.value == self.selected_season:
                option.default = True
            else:
                option.default = False
        # Update the embed with the new player stats
        player_stats_embed, view = get_player_stats_embed(self.player_stats, self.bnet_tag, view=self.view)
        await interaction.response.edit_message(embed=player_stats_embed, view=view)


class GameModesSelect(Select):
    def __init__(self, bnet_tag, player_stats, participated_in_seasons):
        self.bnet_tag, self.player_stats = bnet_tag, player_stats
        game_modes = []
        game_mode_values = set()
        default_season = next((int(option.value) for option in participated_in_seasons
                               if getattr(option, 'default', False)), None)
        default_is_set = False
        for stat in player_stats:
            game_mode = get_game_mode_from_id(stat.get('gameMode'))
            option = SelectOption(label=game_mode, value=game_mode)
            if default_season and stat.get('season') == default_season and not default_is_set:
                option.default = default_is_set = True
            if game_mode not in game_mode_values:
                game_modes.append(option)
                game_mode_values.add(game_mode)
        super().__init__(placeholder='Choose game mode...', options=game_modes, custom_id='game_modes_menu')

    async def callback(self, interaction: Interaction):
        # Update the game mode select menu with the user choice
        selected_game_mode = interaction.data['values'][0]
        for option in self.options:  
            if option.value == selected_game_mode:
                option.default = True
            else:
                option.default = False
        # Update the embed with the new player stats
        player_stats_embed, view = get_player_stats_embed(self.player_stats, self.bnet_tag, view=self.view)
        await interaction.response.edit_message(embed=player_stats_embed, view=view)


class MultiSelectMenu(View):
    def __init__(self, player_stats, bnet_tag):
        super().__init__()
        participated_in_seasons = [SelectOption(label=str(emojify_number(s)), value=str(s))
                                   for s in get_player_participated_in_seasons(bnet_tag)]
        participated_in_seasons[0].default = True

        game_mode_select = GameModesSelect(bnet_tag, player_stats, participated_in_seasons)
        self.add_item(game_mode_select)
        self.add_item(SeasonsSelectMenu(bnet_tag, game_mode_select.player_stats, participated_in_seasons, self.children,
                                        game_mode_select))

    def get_default_season(self):
        for item in self.children:
            if item.custom_id == 'seasons_menu':
                for option in item.options:
                    if getattr(option, 'default', False):
                        return int(option.value)
        return None

    def get_default_game_mode(self):
        for item in self.children:
            if item.custom_id == 'game_modes_menu':
                for option in item.options:
                    if getattr(option, 'default', False):
                        return option.value
        return None


def get_player_stats_embed(player_stats, bnet_tag, view=None):
    if not player_stats:
        return Embed(description='🌌 The Dark Portal\'s manifest reveals no stats for this champion.'), None

    embed = Embed(title='🛡️ Champion Stats 🛡️', color=0x3498db)

    # Create the view and get default values
    if view is None:
        view = MultiSelectMenu(player_stats, bnet_tag)
    default_season = view.get_default_season()
    default_game_mode = view.get_default_game_mode()

    # Retrieve the specific stat based on the default values
    player_stat = next((stat for stat in player_stats if stat['season'] == default_season and
                        get_game_mode_from_id(stat['gameMode']) == default_game_mode), None)

    if player_stat:
        game_mode = get_game_mode_from_id(player_stat['gameMode'])
        if game_mode is None:
            game_mode = str(game_mode)
        _name = 'player'
        if '1vs1' not in game_mode:
            _name = 'players'
        players = ', '.join([i['name'] for i in player_stat['playerIds']])

        field_name = f'Mode: {game_mode} | {_name}: {players}'
        if player_stat['race']:
            field_name += f' | Race: {RACES[player_stat["race"]][1]}'

        field_value = f'Season: {player_stat["season"]}\n'
        field_value += f'MMR: {player_stat["mmr"]}\n'
        field_value += f'Win Rate: {convert_win_rate_to_percentage(player_stat["winrate"])}\n'
        field_value += f'W/L: {player_stat["wins"]}:{player_stat["losses"]}\n'
        field_value += f'Games: {player_stat["games"]}'

        embed.add_field(name=field_name, value=field_value, inline=False)

    return embed, view


def convert_win_rate_to_percentage(num):
    if 0 <= num <= 1:
        return f'{num * 100:.1f}%'
    else:
        return 0

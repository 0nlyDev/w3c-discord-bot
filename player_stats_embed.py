import discord
from discord import Embed, SelectOption, Interaction
from discord.ui import Select, View, Button

from w3c_endpoints.player_stats import RACES
from w3c_endpoints.active_modes import get_game_mode_from_id
from w3c_endpoints.player import get_player_participated_in_seasons
from w3c_endpoints.player_search import emojify_number
from w3c_endpoints.player_stats import get_player_stats
from responses import responses


def get_new_game_modes_and_player_stats_by_season(bnet_tag, selected_season, gate_way=None):
    new_player_stats, gate_way = get_player_stats(bnet_tag, season=selected_season, gate_way=gate_way)
    game_modes_in_season = []
    for stats in new_player_stats:
        try:
            if stats['season'] == int(selected_season):
                game_mode = get_game_mode_from_id(stats['gameMode'])
                if game_mode not in game_modes_in_season:
                    game_modes_in_season.append(game_mode)
        except TypeError:
            print('selected_season', selected_season)
            print("stats", stats)
    return game_modes_in_season, new_player_stats


def get_race_emoji(race):
    if race == 'ne':
        return '<:night_elf:1172634662418513931>'
    elif race == 'oc':
        return '<:orc:1172634647063187517>'
    elif race == 'hu':
        return '<:human:1172634674087088180>'
    elif race == 'ud':
        return '<:undead:1172633759674273802>'
    elif race == 'rnd':
        return '<:random:1172634634400563271>'


class SeasonsSelectMenu(Select):
    def __init__(self, bnet_tag, player_stats, participated_in_seasons, children, game_modes_select, gate_way):
        self.bnet_tag, self.player_stats, self.children, self.game_modes_select, self.gate_way = (
            bnet_tag, player_stats, children, game_modes_select, gate_way)
        self.selected_season = None
        super().__init__(placeholder='Choose season...', options=participated_in_seasons, custom_id='seasons_menu')

    async def callback(self, interaction: Interaction):
        self.selected_season = interaction.data['values'][0]

        # Fetch new game modes and player stats based on the selected season
        new_game_modes, self.player_stats = get_new_game_modes_and_player_stats_by_season(
            self.bnet_tag, self.selected_season, self.gate_way)
        if not new_game_modes:
            # try to find stats without specified (or fist found) region
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


class MakeMessageVisibleBtn(Button):
    def __init__(self, stored_embed, style=discord.ButtonStyle.blurple, emoji='👀', label='Reveal Me!',
                 custom_id='make_message_visible_btn'):
        super().__init__(style=style, emoji=emoji, label=label, custom_id=custom_id)
        self.stored_embed = stored_embed

    async def callback(self, interaction: discord.Interaction):
        response = f"👀 {interaction.user.mention} {responses['player_stats_by_game_mode']['message_made_visible_by']}"
        await interaction.response.send_message(content=response, embed=self.stored_embed, ephemeral=False)
        original_response = await interaction.original_response()
        print(f'{interaction.user.display_name} from {interaction.guild.name} via {interaction.channel.name} '
              f'revealed stats for: {self.stored_embed.title}, jump_url: {original_response.jump_url}')


class MultiSelectMenu(View):
    def __init__(self, player_stats, bnet_tag, gate_way=None):
        super().__init__()
        participated_in_seasons = [SelectOption(label=str(emojify_number(s)), value=str(s))
                                   for s in get_player_participated_in_seasons(bnet_tag)]
        participated_in_seasons[0].default = True

        game_mode_select = GameModesSelect(bnet_tag, player_stats, participated_in_seasons)
        self.add_item(game_mode_select)
        self.add_item(SeasonsSelectMenu(bnet_tag, game_mode_select.player_stats, participated_in_seasons, self.children,
                                        game_mode_select, gate_way))

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


def get_player_stats_embed(player_stats, bnet_tag, view=None, gate_way=None):
    if not player_stats:
        return Embed(description=responses['embeds']['no_stats_found']), None

    # Create the view and get default values
    if view is None:
        view = MultiSelectMenu(player_stats, bnet_tag, gate_way)
    default_season = view.get_default_season()
    default_game_mode = view.get_default_game_mode()

    # Retrieve the specific stat based on the default values
    if player_stats:
        title = f'🛡️ W3Champion {bnet_tag} 🛡️'
        description = f'### ⚔️️ {default_game_mode} ⚔️'
        color = 7419530  # DarkPurple
        url = f'https://www.w3champions.com/player/{bnet_tag.replace("#", "%23")}'
        embed = Embed(title=title, description=description, color=color, url=url)

        field_counter = 0
        for player_stat in player_stats:
            game_mode = get_game_mode_from_id(player_stat['gameMode'])
            if player_stat['season'] == default_season and game_mode == default_game_mode:
                field_counter += 1
                # Hide player's stats for season 0 (the w3c beta period)
                if default_season == 0:
                    embed.add_field(name='', value=responses['player_stats_by_game_mode']['hide_season_zero'])
                    break
                # build the embed with stats
                if player_stat['race'] is not None:
                    field_name = (f'{get_race_emoji(RACES[player_stat["race"]][0])} '
                                  f'{RACES[player_stat["race"]][1].capitalize()}')
                else:
                    player_s = 'Player'
                    if len(player_stat['playerIds']) > 1:
                        player_s = 'Players'
                    players = ', '.join([i['name'] for i in player_stat['playerIds']])
                    field_name = f'{player_s}: `{players}`'
                field_name += '\n'
                field_value = f'MMR: `{player_stat["mmr"]}`\n'
                field_value += f'Win Rate: `{convert_win_rate_to_percentage(player_stat["winrate"])}`\n'
                field_value += f'W/L: `{player_stat["wins"]}:{player_stat["losses"]}`\n'
                field_value += f'Games: `{player_stat["games"]}`'
                embed.add_field(name=field_name, value=field_value, inline=True)
        if field_counter >= 5 and (field_counter - 5) % 3 == 0:  # fix embed formatting, pattern: n+3 if n >= 5
            embed.add_field(name='', value='', inline=True)
        embed.add_field(name=f'\nSEASON: {emojify_number(default_season)}', value='', inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='', value='[GitHub](https://github.com/0nlyDev/w3c-discord-bot)', inline=False)
        embed.set_footer(text=responses['embeds']['footer'])
        # Create the make_message_visible_btn and pass it the embed
        if not next((item for item in view.children if getattr(item, 'custom_id', None) == 'make_message_visible_btn'),
                    None):
            view.add_item(MakeMessageVisibleBtn(stored_embed=embed))
        # Pass the updated embed to the make_message_visible_btn
        else:
            for item in view.children:
                if getattr(item, 'custom_id', None):
                    item.stored_embed = embed
        return embed, view


def convert_win_rate_to_percentage(num):
    if 0 <= num <= 1:
        return f'{num * 100:.1f}%'
    else:
        return 0

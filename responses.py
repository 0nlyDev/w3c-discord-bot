import json

from parse_player_stats import parse_player_stats
from w3c_endpoints.player_stats import get_player_stats
from w3c_endpoints.active_modes import get_active_modes
from w3c_endpoints.player_search import player_search

import discord

with open('assets/emojis.json', 'r', encoding="utf-8") as file:
    EMOJIS = json.load(file)

player_name = None


def handle_response(message):
    bot_command = '!w3c'
    view = None  # Initialize the view as None

    if message.startswith(bot_command):
        if bot_command + ' help' == message or bot_command == message:
            return response_help_message(), view
        elif bot_command + ' stats ' in message:
            response = response_stats(message)
            if isinstance(response, PlayerSearchResultsSelect):
                view = response
                if len(view.children) > 0:
                    return 'Select a player bellow:', view
                else:
                    return 'No players found.', view

            return response, view
        elif bot_command + ' modes' == message:
            view = GameModeSelect()
            print('view', type(view), view)
            return f"Select a game mode below:", view
        elif bot_command in message:
            return response_command_not_found(), view

    return None, None  # If nothing matches, return None for both response and view


class GameModeSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GameModeSelectMenu())


class GameModeSelectMenu(discord.ui.Select):
    def __init__(self):
        active_modes = get_active_modes()
        active_modes = {k + " " + EMOJIS["1"] + EMOJIS["6"] for k in active_modes.keys()}
        options = [discord.SelectOption(label=mode, value=mode) for mode in active_modes]
        super().__init__(placeholder="Choose a game mode", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You chose: {self.values[0]}")


class PlayerSearchResultsSelect(discord.ui.View):
    def __init__(self, player_name):
        super().__init__()
        search_results = player_search(player_name)
        chunks = split_list(search_results)

        # Add up to 5 chunks to the view
        for idx, chunk in enumerate(chunks[:5]):
            self.add_item(PlayerSearchMenu(chunk,idx))



class PlayerSearchMenu(discord.ui.Select):
    def __init__(self, players, idx):  # Now players is a list of <= 25 players
        options = [discord.SelectOption(label=player, value=player) for player in players]
        super().__init__(placeholder=f'Search result {idx+1} (Players)', options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You chose: {self.values[0]}")



def response_help_message():
    help_message = ('**W3Champions bot commands**:\n'
                    '`Get player stats by game mode`:\n'
                    '\tCommand: `!w3c stats <BattleNetTag> <Region>`\n'
                    '\te.g. `!w3c stats happy#2384 eu`\n'
                    '\tOptional arguments: `<GameMode>`, `<Race>`,  `<Season>`\n'
                    '\tArguments must be in this order: `!w3c stats <BattleNetTag> <Region> <GameMode> '
                    '<Race> <Season>`\n'
                    '\te.g. `!w3c stats happy#2384 eu 1vs1 ud 16`\n'
                    '\te.g. `!w3c stats moon#35134 eu ffa`\n'
                    '`See all available <GameMode> arguments`:\n'
                    '\tCommand: `!w3c modes`\n'
                    '\tPrints all active modes on w3c, e.g: `1vs1`, `2vs2`, `4vs4`, `FFA`, etc.\n'
                    '`Bot usage (help)`:\n'
                    '\tCommand: `!w3c help` or just `!w3c` Prints this message.\n'
                    'Disclaimer: The W3C Bot is in BETA phase and currently being in development, apologies '
                    'if you encounter bugs or the bot is offline. For anything related, feel free to reach out'
                    ' to @SageNoob via Discord or on github: https://github.com/0nlyDev/w3c-discord-bot')
    return help_message


def response_stats(message):
    # try:
    _argument1, _argument2, *remaining_items = message.split(' ')
    bnet_tag_or_player_name = remaining_items[0] if remaining_items else None
    region = remaining_items[1] if len(remaining_items) > 1 else None
    game_mode = remaining_items[2] if len(remaining_items) > 2 else None
    race = remaining_items[3] if len(remaining_items) > 3 else None
    season = remaining_items[4] if len(remaining_items) > 4 else None

    print(bnet_tag_or_player_name)

    if '#' in bnet_tag_or_player_name:  # bnet_tag was provided
        bnet_tag = bnet_tag_or_player_name
        player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)
        return parse_player_stats(player_stats)
    # elif '@' in bnet_tag_or_player_name:  # get bnet_tag from @mentioned discord user
    #     return
    else:  # get bnet_tag by searching w3c for player name and listing the results in a SelectMenu
        global player_name
        player_name = bnet_tag_or_player_name
        return PlayerSearchResultsSelect(player_name)
        # bnet_tag = select_menu_choice
        # player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)

    # print('player stats:', player_stats)
    # return parse_player_stats(player_stats)
    # except Exception as e:
    #     raise(e)
    #     return


def response_command_not_found():
    return ('Command not found, please use `!w3c help` or just `!w3c` in chat, to see available bot commands '
            'and usage examples.')


def split_list(input_list, max_size=25):
    return [input_list[i:i + max_size] for i in range(0, len(input_list), max_size)]
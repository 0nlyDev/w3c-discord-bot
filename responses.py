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
            if isinstance(response, PlayerSearchMenu):
                view = response
                if len(view.children) > 0:
                    return 'Select a player bellow:', view
                else:
                    return 'No players found.', view

            return response, view
        elif bot_command + ' modes' == message:
            # view = GameModeSelect()
            print('view', type(view), view)
            return f"Select a game mode below:", view
        elif bot_command in message:
            return response_command_not_found(), view

    return None, None  # If nothing matches, return None for both response and view


# class GameModeSelect(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(GameModeSelectMenu())
#
#
# class GameModeSelectMenu(discord.ui.Select):
#     def __init__(self):
#         active_modes = get_active_modes()
#         active_modes = {k + " " + EMOJIS["1"] + EMOJIS["6"] for k in active_modes.keys()}
#         options = [discord.SelectOption(label=mode, value=mode) for mode in active_modes]
#         super().__init__(placeholder="Choose a game mode", options=options)
#
#     async def callback(self, interaction: discord.Interaction):
#         await interaction.response.send_message(f"You chose: {self.values[0]}")


class PlayerSearchMenu(discord.ui.View):
    def __init__(self, search_results, player_name, region, game_mode, race, season):
        super().__init__()
        self.add_item(PlayerSearchSelect(search_results, region, game_mode, race, season))


class PlayerSearchSelect(discord.ui.Select):
    def __init__(self, players, region, game_mode, race, season):  # Now players is a list of <= 25 players
        self.region, self.game_mode, self.race, self.season = region, game_mode, race, season
        options = [discord.SelectOption(label=player, value=player) for player in players]
        super().__init__(placeholder='Search results (Players)', options=options)

    async def callback(self, interaction: discord.Interaction):
        user_choice = interaction.data['values'][0]
        print('user_choice', user_choice)
        if 'Load more results...' in user_choice:
            pass
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats = get_player_stats(bnet_tag, self.region, self.game_mode, self.race, self.season)
            parsed_player_stats = parse_player_stats(_player_stats)

            # split in messages in chunks no longer than 2k to ensure we go around discords 2k chars limitation
            delimiter = '\n\n'
            stats_in_chunks = list(split_stats_in_chunks_of_2k_chars(
                parsed_player_stats.split(delimiter), delimiter))
            # Send the first chunk using the response
            await interaction.response.send_message(stats_in_chunks[0])
            # Send subsequent chunks as follow-ups
            for player_stats in stats_in_chunks[1:]:
                await interaction.followup.send(content=player_stats)


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
        search_results = player_search(player_name)
        if search_results:
            return PlayerSearchMenu(search_results, player_name, region, game_mode, race, season)


def response_command_not_found():
    return ('Command not found, please use `!w3c help` or just `!w3c` in chat, to see available bot commands '
            'and usage examples.')


def split_list(input_list, max_size=25):
    return [input_list[i:i + max_size] for i in range(0, len(input_list), max_size)]


def split_stats_in_chunks_of_2k_chars(stats, delimiter='\n\n', max_length=2000):
    current_chunk = []
    char_counter = 0
    for stat in stats:
        if char_counter + len(stat) + len(delimiter) <= max_length:
            current_chunk.append(stat)
            char_counter += len(stat) + len(delimiter)
        else:
            yield delimiter.join(current_chunk)
            current_chunk = [stat]
            char_counter = len(stat) + len(delimiter)
    if current_chunk:  # handle any remaining stats
        yield delimiter.join(current_chunk)

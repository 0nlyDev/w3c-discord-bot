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
                    return '🌌 From the depths of the Dark Portal, select your champion below:', view
            return response, view
        elif bot_command + ' modes' == message:
            battle_modes = ', '.join([f'`{k}`' for k in get_active_modes().keys()])
            return f'⚔️ Available battle modes in the World of W3Champions: {battle_modes}', view
        elif bot_command in message:
            return response_command_not_found(), view

    return None, None  # If nothing matches, return None for both response and view


class PlayerSearchMenu(discord.ui.View):
    def __init__(self, search_results, region, game_mode, race, season):
        super().__init__()
        self.add_item(PlayerSearchSelect(search_results, region, game_mode, race, season))


class PlayerSearchSelect(discord.ui.Select):
    def __init__(self, search_results, region, game_mode, race, season):  # Now players is a list of <= 25 players
        self.search_results, self.region, self.game_mode, self.race, self.season = (
            search_results, region, game_mode, race, season)
        options = [discord.SelectOption(label=player, value=player) for player in search_results]
        super().__init__(placeholder='Champion manifest from the portal\'s depths:', options=options)

    async def callback(self, interaction: discord.Interaction):
        user_choice = interaction.data['values'][0]
        print('user_choice', user_choice)
        if '🌀 Summon more champions from the depths...' in user_choice:
            new_search_results = player_search(player_name, self.search_results[-2])
            print('self.search_results[-2]', self.search_results[-2])
            if new_search_results:
                new_menu_select = PlayerSearchMenu(
                    new_search_results, self.region, self.game_mode, self.race, self.season)
                await interaction.response.send_message('🌌 Through the Dark Portal, more champions emerge!',
                                                        view=new_menu_select)
            else:
                await interaction.response.send_message('🌌 By the Light! It seems like we\'ve reached the end of our '
                                                        'journey! No more champions emerge from the Dark Portal. Try '
                                                        'with a different name...')
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats = get_player_stats(bnet_tag, self.region, self.game_mode, self.race, self.season)
            parsed_player_stats = parse_player_stats(_player_stats)

            # split messages in chunks no longer than 2k to ensure we go around discords 2k chars limitation
            delimiter = '\n\n'
            stats_in_chunks = list(split_stats_in_chunks_of_2k_chars(
                parsed_player_stats.split(delimiter), delimiter))
            # Send the first chunk using the response
            await interaction.response.send_message(stats_in_chunks[0])
            # Send subsequent chunks as follow-ups
            for player_stats in stats_in_chunks[1:]:
                await interaction.followup.send(content=player_stats)


def response_help_message():
    help_message = ('🔥 **W3C Bot Commands to reveal the World of W3Champions** 🔥:\n'
                    
                    '🔎 **Seek champions by player name to reveal their legendary stats** 🔎\n'
                    '\tBy Elune: `!w3c stats <PlayerName>`\n'
                    '\te.g. `!w3c stats Moon`\n'
                    
                    '🌌 **Conjure legendary stats by Battle Tag** 🌌⚡:\n'
                    '\tCommand the spirits: `!w3c stats <BattleNetTag>`\n'
                    '\te.g. `!w3c stats happy#2384`\n'
                    
                    '⚡ **Harness the power of runes (Optional Arguments)** ⚡:\n'
                    '\tAdd arguments: `<Region/GameMode>`, `<Race>`, `<Season>`\n'
                    '\t⚠️ Arguments order must be obeyed (for the time being)!: '
                    '`!w3c stats <PlayerName> <Region> <GameMode> <Race> <Season> ⚠️`\n'
                    '\te.g. `!w3c stats moon eu ffa`\n'
                    '\tOr if you know their Battle Tag, whisper in this order: '
                    '`!w3c stats <BattleNetTag> <Region> <GameMode> <Race> <Season>`\n'
                    '\te.g. `!w3c stats happy#2384 eu 1vs1 ud 16`\n'
                    
                    '⚔️ **Discover all the battle modes in the World of W3Champions** ⚔️:\n'
                    '\tAncient words: `!w3c modes`\n'
                    '\tReveals: `1vs1`, `2vs2`, `4vs4`, `FFA`, etc.\n'
                    
                    '🌙 **Seeking guidance, young adventurer?** 🌙:\n'
                    '\tSpeak thusly: `!w3c help` or simply whisper `!w3c` to hear this tale again.\n'
                    
                    '📜 **Guardian\'s Scroll**: The W3C Bot, safeguarded by Medivh, stands in its **BETA** phase. '
                    'Winds of magic can be unpredictable. Should you encounter misplaced enchantments or if the bot '
                    'drifts into the void, seek **@SageNoob** in the ethereal chambers of Discord. Remember, '
                    'this spellwork is an open grimoire, a testament to the open source magic of our world. Brave '
                    'souls wishing to enrich its pages are welcome to journey to the arcane library of Github: '
                    'https://github.com/0nlyDev/w3c-discord-bot. Your wisdom and contributions illuminate our path.')

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
            return PlayerSearchMenu(search_results, region, game_mode, race, season)


def response_command_not_found():
    return ('🔮 The spirits do not recognize this spell... Use `!w3c help` or simply `!w3c` to seek guidance on the '
            'ancient commands. 🔮')


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

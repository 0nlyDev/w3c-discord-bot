import json

from player_stats_embed import get_player_stats_embed
from w3c_endpoints.player_stats import get_player_stats
from w3c_endpoints.active_modes import get_active_modes
from w3c_endpoints.player_search import player_search

import discord

with open('assets/emojis.json', 'r', encoding="utf-8") as file:
    EMOJIS = json.load(file)


class PlayerSearchMenu(discord.ui.View):
    def __init__(self, player_name, search_results, region, game_mode, race, season):
        super().__init__()
        self.add_item(PlayerSearchSelect(player_name, search_results, region, game_mode, race, season))


class PlayerSearchSelect(discord.ui.Select):
    # Now players is a list of <= 25 players
    def __init__(self, player_name, search_results, region, game_mode, race, season):
        self.player_name, self.search_results, self.region, self.game_mode, self.race, self.season = (
            player_name, search_results, region, game_mode, race, season)
        options = [discord.SelectOption(label=player, value=player) for player in search_results]
        self.load_more_results_string = '🌀 Summon more champions from the depths...'
        if len(options) == 20:
            options.append(discord.SelectOption(label=self.load_more_results_string,
                                                value=self.load_more_results_string))
        super().__init__(placeholder='Champion manifest from the portal\'s depths:', options=options)

    async def callback(self, interaction: discord.Interaction):
        user_choice = interaction.data['values'][0]
        if self.load_more_results_string == user_choice:
            new_search_results = player_search(self.player_name, self.search_results[-2])
            print('self.search_results[-2]', self.search_results[-2])
            if new_search_results:
                new_menu_select = PlayerSearchMenu(
                    self.player_name, new_search_results, self.region, self.game_mode, self.race, self.season)
                await interaction.response.send_message('🌌 Through the Dark Portal, more champions emerge!',
                                                        view=new_menu_select, ephemeral=True)
            else:
                await interaction.response.send_message('🌌 By the Light! It seems like we\'ve reached the end of our '
                                                        'journey! No more champions emerge from the Dark Portal. Try '
                                                        'with a different Champion name...', ephemeral=True)
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats = get_player_stats(bnet_tag, self.region, self.game_mode, self.race, self.season)
            player_stats_embed, view = get_player_stats_embed(_player_stats, bnet_tag)
            if view:
                await interaction.response.send_message(embed=player_stats_embed, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(embed=player_stats_embed, ephemeral=True)


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
                    'souls wishing to enrich its pages are welcome to journey to the arcane library 📚 of Github: '
                    'https://github.com/0nlyDev/w3c-discord-bot. Your wisdom and contributions illuminate our path.')

    return help_message


def response_stats(player_name, region=None, game_mode=None, race=None, season=None):
    if '#' in player_name:  # bnet_tag was provided
        bnet_tag = player_name
        player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)
        return get_player_stats_embed(player_stats, bnet_tag)
    # elif '@' in player_name:  # get bnet_tag from @mentioned discord user
    #     return
    else:  # get bnet_tag by searching w3c for player name and listing the results in a SelectMenu
        search_results = player_search(player_name)
        if search_results and len(search_results) == 1:
            bnet_tag = search_results[0].split(' ')[0]
            player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)
            print('wha play sta', player_stats)
            return get_player_stats_embed(player_stats, bnet_tag)
        else:
            return PlayerSearchMenu(player_name, search_results, region, game_mode, race, season), None


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


def response_modes():
    return ', '.join([f'`{k}`' for k in get_active_modes().keys()])

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
    def __init__(self, player_name, search_results, region, game_mode, race, season):
        self.player_name, self.search_results, self.region, self.game_mode, self.race, self.season = (
            player_name, search_results, region, game_mode, race, season)
        options = [discord.SelectOption(label=player, value=player) for player in search_results]
        self.load_more_results_string = '🌀 Summon more champions from the depths...'
        if len(options) > 0:
            # w3c playerSearch endpoint is not reliable - sometimes returns less than 20 players
            # when there are still more results to be shown. So we keep it if > 0 because we are not sure when is the
            # end of the search, and we will relay on the result to determine end of search.
            options.append(discord.SelectOption(label=self.load_more_results_string,
                                                value=self.load_more_results_string))
        super().__init__(placeholder='Champion manifest from the portal\'s depths:', options=options)

    async def callback(self, interaction: discord.Interaction):
        user_choice = interaction.data['values'][0]
        if self.load_more_results_string == user_choice:
            last_bnet_tag = next(i for i in reversed(self.search_results) if i != self.load_more_results_string)
            new_search_results = player_search(self.player_name, last_bnet_tag)
            print('self.search_results[-2]', self.search_results[-2])
            if isinstance(new_search_results, list) and new_search_results:
                new_menu_select = PlayerSearchMenu(
                    self.player_name, new_search_results, self.region, self.game_mode, self.race, self.season)
                await interaction.response.send_message('🌌 Through the Dark Portal, more champions emerge!',
                                                        view=new_menu_select, ephemeral=True)
            elif isinstance(new_search_results, list):
                await interaction.response.send_message('🌌 By the Light! It seems like we\'ve reached the end of our '
                                                        'journey! No more champions emerge from the Dark Portal. Try '
                                                        'with a different Champion name...', ephemeral=True)
            else:
                await interaction.response.send_message(new_search_results, ephemeral=True)
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats = get_player_stats(bnet_tag, self.region, self.game_mode, self.race, self.season)
            player_stats_embed, view = get_player_stats_embed(_player_stats, bnet_tag)
            if view:
                await interaction.response.send_message(embed=player_stats_embed, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(embed=player_stats_embed, ephemeral=True)


def response_help_message():
    help_message = (
        '🔥 **W3C Bot Slash Commands to reveal the World of W3Champions** 🔥:\n\n'

        '🔎 **Seek champions by Name or Battle Tag to reveal their legendary stats** 🔎:\n'
        'To initiate a search, use the `/player_stats_by_game_mode` command followed by the '
        'player\'s name or Battle Tag.\n'
        'e.g., `/player_stats_by_game_mode Moon` or `/player_stats_by_game_mode happy#2384`\n'
        'Select from the available options or type the player\'s name or Battle Tag to initiate a search.\n'
        'If more champions are available, you can load additional results by selecting '
        'the "🌀 Summon more champions from the depths..." option from the dropdown menu.\n\n'

        '⚡ **Refine your search with Optional Arguments** ⚡:\n'
        'You can refine your search by adding optional arguments such as `[Region]`, `[GameMode]`, '
        '`[Race]`, and `[Season]` to the `/player_stats_by_game_mode` command. These arguments can be '
        'provided in any order:\n'
        '`/player_stats_by_game_mode <PlayerName/BattleNetTag> [Region] [GameMode] [Race] [Season]`\n'
        'e.g., `/player_stats_by_game_mode Moon eu ffa` or `/player_stats_by_game_mode happy#2384 1vs1 ud 16`\n\n'

        '⚔️ **Discover all the battle modes in the World of W3Champions** ⚔️:\n'
        'Use the `/battle_modes` command to reveal all available battle modes.\n\n'

        '🌙 **Seeking guidance, young adventurer?** 🌙:\n'
        'To access this help message again, simply use the `/help` command.\n\n'

        '📜 **Guardian\'s Scroll**: The W3C Bot, safeguarded by Medivh, stands in its **BETA** phase. '
        'Winds of magic can be unpredictable... Should you encounter misplaced enchantments or if the bot '
        'drifts into the void, seek **@SageNoob** in the ethereal chambers of Discord. Remember, '
        'this spellwork is an open grimoire, a testament to the open-source magic of our world. Brave '
        'souls wishing to enrich its pages are welcome to journey to the arcane library 📚 of Github: '
        'https://github.com/0nlyDev/w3c-discord-bot. Your wisdom and contributions illuminate our path.'
    )
    return help_message


def response_stats(player_name, region=None, game_mode=None, race=None, season=None):
    search_results = player_search(player_name)
    if search_results:
        if len(search_results) == 1:
            bnet_tag = search_results[0].split(' ')[0]
            player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)
            return get_player_stats_embed(player_stats, bnet_tag)
        else:
            return PlayerSearchMenu(player_name, search_results, region, game_mode, race, season), None
    return None, None


def response_modes():
    return ', '.join([f'`{k}`' for k in get_active_modes().keys()])

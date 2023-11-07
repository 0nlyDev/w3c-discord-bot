import json

import discord
from discord import app_commands
from discord.ext import commands

from w3c_endpoints.player_search import player_search
from w3c_endpoints.player_stats import get_player_stats
from player_stats_embed import get_player_stats_embed


class PlayerStatsByGameMode(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        with open('assets/emojis.json', 'r', encoding="utf-8") as file:
            self.emojis = json.load(file)

    @app_commands.command(name='player_stats_by_game_mode', description='Get player\'s statistics by game mode.')
    async def player_stats_by_game_mode(self,
                                        interaction,
                                        player_name: str,
                                        gate_way: str = None):

        search_results = player_search(player_name)
        response, view = None, None
        if search_results:
            # If only one player is available, display the stats embed immediately
            if len(search_results) == 1:
                bnet_tag = search_results[0].split(' ')[0]
                player_stats = get_player_stats(bnet_tag, gate_way)
                response, view = get_player_stats_embed(player_stats, bnet_tag)
            # Otherwise, display the search menu
            else:
                response, view = PlayerSearchMenu(player_name, search_results, gate_way), None
        if response:
            if hasattr(response, 'children') and len(response.children) > 0:
                await interaction.response.send_message(
                    '🌌 From the depths of the Dark Portal, select your champion below:', view=response, ephemeral=True)
            else:
                if view:
                    await interaction.response.send_message(embed=response, view=view, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=response, ephemeral=True)
        else:
            await interaction.response.send_message(
                '🌌 In the vastness beyond the Dark Portal, this champion remains a mystery.', ephemeral=True)


class PlayerSearchMenu(discord.ui.View):
    def __init__(self, player_name, search_results, gate_way):
        super().__init__()
        self.add_item(PlayerSearchSelect(player_name, search_results, gate_way))


class PlayerSearchSelect(discord.ui.Select):
    def __init__(self, player_name, search_results, gate_way):
        self.player_name, self.search_results, self.gate_way = player_name, search_results, gate_way
        options = [discord.SelectOption(label=player, value=player) for player in search_results]
        self.load_more_results_string = '🌀 Summon more champions from the depths...'
        if len(options) > 0:
            # w3c playerSearch endpoint is not reliable - sometimes returns less than 20 players
            # when there are still more results to be shown. So we keep it if > 0 because we are not sure when is the
            # end of the search, and we will relay on the result to determine end of search.
            options.append(discord.SelectOption(label=self.load_more_results_string,
                                                value=self.load_more_results_string))
        super().__init__(placeholder='Champion manifest from the portal\'s depths:', options=options)

    async def callback(self, interaction):
        user_choice = interaction.data['values'][0]
        if self.load_more_results_string == user_choice:
            last_bnet_tag = next(i for i in reversed(self.search_results) if i != self.load_more_results_string)
            new_search_results = player_search(self.player_name, last_bnet_tag)
            print('self.search_results[-2]', self.search_results[-2])
            if isinstance(new_search_results, list) and new_search_results:
                new_menu_select = PlayerSearchMenu(
                    self.player_name, new_search_results, self.gate_way)
                await interaction.response.send_message('🌌 Through the Dark Portal, more champions emerge!',
                                                        view=new_menu_select, ephemeral=True)
            elif isinstance(new_search_results, list):
                await interaction.response.send_message(
                    '🌌 By the Light! It seems like we\'ve reached the end of our '
                    'journey! No more champions emerge from the Dark Portal. Try '
                    'with a different Champion name...', ephemeral=True)
            else:
                await interaction.response.send_message(new_search_results, ephemeral=True)
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats = get_player_stats(bnet_tag, self.gate_way)
            player_stats_embed, view = get_player_stats_embed(_player_stats, bnet_tag)
            if view:
                await interaction.response.send_message(embed=player_stats_embed, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(embed=player_stats_embed, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(PlayerStatsByGameMode(client))

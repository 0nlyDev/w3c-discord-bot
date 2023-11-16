import json
import re

import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from w3c_endpoints.player_search import player_search
from w3c_endpoints.player_stats import get_player_stats
from player_stats_embed import get_player_stats_embed
from responses import responses
from db_queries.database import get_engine, create_session
from db_queries.operations import get_user

THIS_RESPONSE = responses['player_stats_by_game_mode']


class PlayerStatsByGameMode(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        with open('assets/emojis.json', 'r', encoding="utf-8") as file:
            self.emojis = json.load(file)

    @app_commands.command(name='player_stats_by_game_mode', description='Get player\'s statistics by game mode.')
    @app_commands.describe(player_name='Player\'s @DiscordName, just a Name, or BattleTag',
                           gate_way='GateWay, Europe or America)')
    @app_commands.choices(gate_way=[Choice(name='Europe', value='europe'), Choice(name='America', value='america')])
    async def player_stats_by_game_mode(self,
                                        interaction,
                                        player_name: str,
                                        gate_way: str = None):

        print(f'{interaction.user.display_name} from {interaction.guild.name} used /player_stats_by_game_mode name:'
              f'{player_name} gate_way:{gate_way}')

        provided_gate_way = gate_way

        user_id = get_user_id_from_mention(player_name)
        engine = get_engine()
        session = create_session(engine)
        user = get_user(session, user_id)
        session.close()
        # If player_name is a discord @mention
        if user:
            search_results = [user.battle_tag]
        elif player_name.startswith('<@') and player_name.endswith('>'):
            this_response = THIS_RESPONSE['discord_user_is_none'].replace('{PLAYER_NAME}', player_name)
            await interaction.response.send_message(this_response, ephemeral=True)
            return  # end search here
        else:
            search_results = player_search(player_name)
        response, view = None, None
        if search_results:
            # If only one player is available, display the stats embed immediately
            if len(search_results) == 1:
                bnet_tag = search_results[0].split(' ')[0]
                player_stats, _ = get_player_stats(bnet_tag, gate_way=gate_way)
                response, view = get_player_stats_embed(player_stats, bnet_tag, gate_way=gate_way)
            # Otherwise, display the search menu
            else:
                response, view = PlayerSearchMenu(player_name, search_results, gate_way, provided_gate_way), None
        if response:
            if hasattr(response, 'children') and len(response.children) > 0:
                await interaction.response.send_message(THIS_RESPONSE['select_player'], view=response, ephemeral=True)
            else:
                if view:
                    await interaction.response.send_message(embed=response, view=view, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=response, ephemeral=True)
        else:
            await interaction.response.send_message(THIS_RESPONSE['no_players_found'], ephemeral=True)


class PlayerSearchMenu(discord.ui.View):
    def __init__(self, player_name, search_results, gate_way, provided_gate_way):
        super().__init__()
        self.add_item(PlayerSearchSelect(player_name, search_results, gate_way, provided_gate_way))


class PlayerSearchSelect(discord.ui.Select):
    def __init__(self, player_name, search_results, gate_way, provided_gate_way):
        self.player_name, self.search_results, self.gate_way, self.provided_gate_way = (
            player_name, search_results, gate_way, provided_gate_way)
        options = [discord.SelectOption(label=player, value=player) for player in search_results]
        if len(options) > 0:
            # w3c playerSearch endpoint is not reliable - sometimes returns less than 20 players
            # when there are still more results to be shown. So we keep it if > 0 because we are not sure when is the
            # end of the search, and we will relay on the result to determine end of search.
            options.append(discord.SelectOption(label=THIS_RESPONSE['load_more_search_results'],
                                                value=THIS_RESPONSE['load_more_search_results']))
        super().__init__(placeholder='Champion manifest from the portal\'s depths:', options=options)

    async def callback(self, interaction):
        if self.provided_gate_way is None:
            self.gate_way = None
        user_choice = interaction.data['values'][0]
        if THIS_RESPONSE['load_more_search_results'] == user_choice:
            last_bnet_tag = next(i for i in reversed(
                self.search_results) if i != THIS_RESPONSE['load_more_search_results'])
            new_search_results = player_search(self.player_name, last_object_id=last_bnet_tag)
            if isinstance(new_search_results, list) and new_search_results:
                new_menu_select = PlayerSearchMenu(
                    self.player_name, new_search_results, self.gate_way, self.provided_gate_way)
                await interaction.response.send_message(THIS_RESPONSE['loaded_more_search_results'],
                                                        view=new_menu_select, ephemeral=True)
            elif isinstance(new_search_results, list):
                await interaction.response.send_message(THIS_RESPONSE['end_of_search'], ephemeral=True)
            else:
                await interaction.response.send_message(new_search_results, ephemeral=True)
        else:
            bnet_tag = user_choice.split(' ')[0]
            _player_stats, self.gate_way = get_player_stats(bnet_tag, gate_way=self.gate_way)
            player_stats_embed, view = get_player_stats_embed(_player_stats, bnet_tag, gate_way=self.gate_way)
            if view:
                await interaction.response.send_message(embed=player_stats_embed, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(embed=player_stats_embed, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(PlayerStatsByGameMode(client))


def get_user_id_from_mention(mention):
    match = re.match(r'<@!?(\d+)>', mention)
    if match:
        return int(match.group(1))
    return None

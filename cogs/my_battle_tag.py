import json

import discord
from discord import app_commands
from discord.ext import commands

from responses import responses
from w3c_endpoints.player import player_endpoint


class MyBattleTag(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='my_battle_tag', description='Add or show your BattleTag.')
    @app_commands.describe(battle_tag='Your BattleTag. e.g. happy#2384')
    async def my_battle_tag(self,
                            interaction,
                            battle_tag: str = None):
        print(f'{interaction.user.display_name} from {interaction.guild.name} used /my_battle_tag')

        if battle_tag is not None and '#' in battle_tag:
            try:
                player_endpoint(battle_tag)
            except json.decoder.JSONDecodeError:
                await interaction.response.send_message(
                    content=responses['my_battle_tag']['player_not_found'].replace('{BATTLE_TAG}', f'{battle_tag}'),
                    ephemeral=True)
                print(f'BattleTag not found on w3champions: "{battle_tag}"')

            await interaction.response.send_message(content=responses['my_battle_tag']['battle_tag_saved'],
                                                    ephemeral=True)
        else:
            if True:  # if battle_tag found in database for this user, show it.
                battle_tag = 'abaddon#2690'
                url = f'https://www.w3champions.com/player/{battle_tag.replace("#", "%23")}'
                this_response = responses['my_battle_tag']['show_user_battle_tag'].replace('{USERNAME}',
                                                                                           interaction.user.mention)
                this_response = this_response.replace('{BATTLE_TAG}', f'[{battle_tag}]({url})')

                await interaction.response.send_message(content=this_response, ephemeral=True)

        # await interaction.response.send_message(content=responses['help']['help_response'], ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(MyBattleTag(client))

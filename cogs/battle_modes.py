import discord
from discord import app_commands
from discord.ext import commands

from responses import active_modes_response


class BattleModes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='battle_modes', description='Discover the currently active battle modes.')
    async def battle_modes(self, interaction: discord.Interaction):
        print(f'{interaction.user.display_name} from {interaction.guild.name} used /battle_modes')
        active_modes = active_modes_response()
        await interaction.response.send_message(content=active_modes, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(BattleModes(client))

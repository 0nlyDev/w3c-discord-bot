import discord
from discord import app_commands
from discord.ext import commands

from w3c_endpoints.active_modes import get_active_modes


class BattleModes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='battle_modes', description='Discover the currently active battle modes.')
    async def battle_modes(self, interaction: discord.Interaction):
        active_modes = ', '.join([f'`{k}`' for k in get_active_modes().keys()])
        await interaction.response.send_message(content=active_modes, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(BattleModes(client))

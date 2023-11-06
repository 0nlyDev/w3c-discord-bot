import discord
from discord import app_commands
from discord.ext import commands

from responses import responses


class PlayerStatsByGameMode(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='player_stats_by_game_mode', description='Get player\'s statistics by game mode.')
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(content='stats...', ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(PlayerStatsByGameMode(client))

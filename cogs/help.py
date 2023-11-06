import discord
from discord import app_commands
from discord.ext import commands

from responses import responses


class Help(commands.Cog):
    def __init__(self, client: commands.bot):
        self.client = client

    @app_commands.command(name='help', description='See all available bot commands and how to use them.')
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=responses['help']['help_response'], ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(Help(client))
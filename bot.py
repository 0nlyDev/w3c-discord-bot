import json
import discord
from discord import app_commands
import responses

# Initialize the client and command tree
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

debugging_mode = True
debugging_guild = 'SageNoobTesting'
debugging_message = ('🔮 Alas, I am temporarily sealed within a magic ward, weaving new spells and '
                     'enchantments. The Dark Portal to the realm of W3Champions shall open again soon. '
                     'For arcane dilemmas, consult `@SageNoob` in the ethereal chambers of Discord '
                     'or traverse the arcane library 📚 of Github: '
                     'https://github.com/0nlyDev/w3c-discord-bot.')


# Help Command
@tree.command(name="help", description="Get help with the bot's commands")
async def _help(interaction):
    help_message = responses.response_help_message()
    await interaction.response.send_message(help_message)


# Player Stats Command
@tree.command(name="player_stats_by_game_mode", description="Get a player's stats by game mode")
async def _stats(
        interaction,
        player_name: str,
        region: str = None,
        game_mode: str = None,
        race: str = None,
        season: str = None
):
    response = responses.response_stats(player_name, region, game_mode, race, season)
    if response and len(response.children) > 0:
        await interaction.response.send_message(
            '🌌 From the depths of the Dark Portal, select your champion below:', view=response)
    else:
        await interaction.response.send_message(
            "🌌 In the vastness beyond the Dark Portal, this champion remains a mystery.")


# Battle Modes Command
@tree.command(name="battle_modes", description="Discover all the available battle modes")
async def _modes(interaction):
    modes_message = responses.response_modes()
    await interaction.response.send_message(modes_message)


# Event to sync commands and print ready message
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} is now running!')


def run_discord_bot():
    with open('./configs/config.json', 'r') as file:
        data = json.load(file)
    token = data["token"]
    client.run(token)


if __name__ == "__main__":
    run_discord_bot()

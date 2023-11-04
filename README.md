# W3C Discord Bot

![w3c_discord_bot.png](assets%2Fw3c_discord_bot.png)

**w3c-discord-bot** is an open-source project that's currently in active development. It aims to provide various statistics from [W3Champions](https://www.w3champions.com/) as bot commands for Discord. If you're interested in contributing, you are more than welcome!

## Features

- Search for player stats by player name or BattleNet Tag.
- Use optional arguments to refine your search.
- Discover all available battle modes.
- Access a helpful list of commands.
- Easy access to player stats using MenuSelects and embeds.

## Usage

To use the bot, simply type in one of the following commands:

- `/player_stats_by_game_mode <PlayerName> or <BattleNetTag>`: Search for player stats.
  - Example: `/player_stats_by_game_mode Moon` or `/player_stats_by_game_mode happy#2384`
  - You can add additional arguments to filter the results: [Region] [GameMode] [Race] [Season]
  - Select from the available options or type the player's name or Battle Tag to initiate a search.
  - If more champions are available, you can load additional results by selecting the "🌀 Summon more champions from the depths..." option.

- `/battle_modes`: Discover all available battle modes.

- `/help`: Access a list of all available commands.

## Invite the Bot

To invite the bot to your Discord server, use the following link:
[Invite W3C Bot](https://discord.com/api/oauth2/authorize?client_id=1166203153654501406&permissions=826781222912&scope=bot)

**NOTE**: Currently, the bot is hosted on the developer's PC, so uptime may not be ideal. 
The page will be updated once the bot is hosted on a more stable server. 
Alternatively, you can clone this repository and run and host the bot yourself if you wish to do so. 
If you host the bot yourself, you will have to create a file named `config.json` inside the `configs` directory,
with a keys/value pairs in the following format `configs/create_your_config.json_here`


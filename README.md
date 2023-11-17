# W3C Discord Bot

![w3c_discord_bot.png](https://github.com/0nlyDev/w3c-discord-bot/blob/main/assets/images/w3c_discord_bot.png)

## Invite the Bot

To invite the bot to your Discord server, use the following link:
[Invite W3C Bot](https://discord.com/api/oauth2/authorize?client_id=1166203153654501406&permissions=826781222912&scope=bot)

## Features
- Slash commands, e.g. `/player_stats_by_game_mode`
- To reduce chat spam, all bot responses are visible only to the user invoking the commands, unless they choose to make it visible with others.
- Search for player stats with a discord @mention, BattleTag or just simply by "any name".
- Makes use of the context menu in Discord. e.g. you can right-click on any Username > Apps > /player_stats_by_game_mode to invoke the command instead of typing it in chat.
- Link your BattleTag to your Discord identity (so that other users can find your stats from W3Champions by @mentioning_you)
- Use optional arguments to refine your search.
- Discover all available battle modes from W3Champions.
- Access a helpful list of commands.
- Easy access to player stats using dropdown menus and embeds.

![image](https://github.com/0nlyDev/w3c-discord-bot/assets/89726447/1e9e81ad-d17a-4a00-9494-61a2f659556b)

## Usage

To use the bot, simply type in one of the following commands:

- `/player_stats_by_game_mode <@UserMention>, <PlayerName>, or <BattleNetTag>` - Search player stats by game mode.
  - Example: `/player_stats_by_game_mode @SageNoob`, `/player_stats_by_game_mode happy#2384`, or `/player_stats_by_game_mode Moon`
  - Optional arguments: [GateWay]
  - If you get multiple results in a search, it loads up to 20 results at a time, you can load additional results by selecting the `🌀 Summon more champions from the depths...` option in the dropdown menu.
  - You can change the season or game mode from the dropdown menus to see the stats you're interested in.
  - Click the `👀 Reveal Me!` button if you want to share the message with others in the same channel.
- `/my_battle_tag`: to link, update, or reveal your BattleTag. 
  - e.g. `/my_battle_tag happy#2384` to link or update your existing BattleTag, 
  - or just `/my_battle_tag` to view your currently linked BattleTag.
  - NOTE: Using this command links your BattleTag with your Discord identity so other users can find your W3C stats by simply using your discord name @mention. e.g. `/player_stats_by_game_mode @SageNoob`.
- `/battle_modes`: Discover all available battle modes.
- `/help`: Access a list of all available commands.

**w3c-discord-bot** is an open-source project that's currently in active development. It aims to provide various statistics from [W3Champions](https://www.w3champions.com/) as bot commands for Discord. If you're interested in contributing, you are more than welcome!
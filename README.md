![w3c_discord_bot.png](assets%2Fw3c_discord_bot.png)

w3c-discord-bot Is open source and, it's currently in active development. It aims to add all (almost) statistics\
from https://www.w3champions.com/ as bot commands. If you're interested in contributing, you are more than welcome!

i.e. type in `!w3c stats happy` and search from a list of players, or if you know the BattleNet Tag `!w3c stats happy#2384 ` in chat, and it returns:\
**🛡️ Champion Stats 🛡️**:\
mode: `1vs1` player: `Happy` race: `undead` season: `16`\
mmr: `2689` win rate 83.6% w/l: 225:44 games: 269

Make sure to type in `!w3c` or `!w3c help` to get a list of all the commands.

To invite the bot to your server, you can use the following link: 
https://discord.com/api/oauth2/authorize?client_id=1166203153654501406&permissions=826781222912&scope=bot

**NOTE**: Currently, the bot is hosted on my own PC, so uptime is not ideal, I will update this page once I find a suitable 
and free server where to host the bot on.\
Alternatively, you can clone this repo and run and host the bot yourself if you wish to so.\
If you host the bot yourself, you will have to create a file named config.json inside the configs directory,
with a key/value pair `{"token": "<your_discord_bot_token>"}`.
 
from parse_player_stats import parse_player_stats
from w3c_endpoints.player_stats import get_player_stats
from w3c_endpoints.active_modes import get_active_modes


def handle_response(message):
    bot_command = '!w3c'
    if message.startswith(bot_command):
        if bot_command + ' help' == message or bot_command == message:
            help_message = ('**W3Champions bot commands**:\n'
                            '`Get player stats by game mode`:\n'
                            '\tCommand: `!w3c stats <BattleNetTag> <Region>`\n'
                            '\te.g. `!w3c stats happy#2384 eu`\n'
                            '\tOptional arguments: `<GameMode>`, `<Race>`,  `<Season>`\n'
                            '\tArguments must be in this order: `!w3c stats <BattleNetTag> <Region> <GameMode> '
                            '<Race> <Season>`\n'
                            '\te.g. `!w3c stats happy#2384 eu 1vs1 ud 16`\n'
                            '\te.g. `!w3c stats moon#35134 eu ffa`\n'
                            '`See all available <GameMode> arguments`:\n'
                            '\tCommand: `!w3c modes`\n'
                            '\tPrints all active modes on w3c, e.g: `1vs1`, `2vs2`, `4vs4`, `FFA`, etc.\n'
                            '`Bot usage (help)`:\n'
                            '\tCommand: `!w3c help` or just `!w3c` Prints this message.\n'
                            'Disclaimer: The W3C Bot is in BETA phase and currently being in development, apologies '
                            'if you encounter bugs or the bot is offline. For anything related, feel free to'
                            'reach out to @SageNoob via Discord.'
                            )
            return help_message
        elif bot_command + ' stats ' in message:
            try:
                _argument1, _argument2, *rest = message.split(' ')
                bnet_tag = rest[0] if rest else None
                region = rest[1] if len(rest) > 1 else None
                game_mode = rest[2] if len(rest) > 2 else None
                race = rest[3] if len(rest) > 3 else None
                season = rest[4] if len(rest) > 4 else None

                player_stats = get_player_stats(bnet_tag, region, game_mode, race, season)
                print('player stats:', player_stats)
                return parse_player_stats(player_stats)
            except Exception as e:
                print(e)
                return
        elif bot_command + ' modes' == message:
            active_modes = ', '.join([f'`{k}`' for k in get_active_modes().keys()])
            return f'Available <GameMode> arguments: {active_modes}'
        elif bot_command in message:
            return ('Command not found, please use `!w3c help` or just `!w3c` in chat, to see available bot commands '
                    'and usage examples.')

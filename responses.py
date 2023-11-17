from w3c_endpoints.active_modes import get_active_modes

responses = {
    'help': {
        'help_response':
            '🔥 **W3C Bot Slash Commands to reveal the World of W3Champions** 🔥:\n\n'

            '🔎 **Discover Champions\' Stats by @mention, Name, or BattleTag** 🔎:\n'
            'Invoke `/player_stats_by_game_mode` with a Discord `@mention`, `BattleTag`, or just a `name`.\n'
            'Examples: `/player_stats_by_game_mode @SageNoob`, `/player_stats_by_game_mode happy#2384`, '
            '`/player_stats_by_game_mode Moon`.\n'
            'If you know the Champion\'s GateWay, you can add an additional argument in the search.\n'
            'e.g. `/player_stats_by_game_mode Grubby Europe`\n'
            'If multiple champions are found, you can load additional results by selecting the '
            '`🌀 Summon more champions from the depths...` option from the dropdown menu.\n'
            'tip: Instead of invoking a slash command from chat, you can leverage the context menu in Discord. To do '
            'that, right click on any Username > Apps > `/player_stats_by_g...` and this will summon the stats for '
            'that user.\n\n'
            
            '🏷️ **Enchant your Discord Presence by linking your BattleTag to your Discord identity** 🏷️️:\n'
            'Invoke `/my_battle_tag` to link, update, or reveal your BattleTag.\n'
            'e.g. `/my_battle_tag happy#2384` to link or update your BattleTag, or just `/my_battle_tag` to view '
            'your currently linked BattleTag. This mystical link allows fellow champions to effortlessly conjure your '
            'W3C stats by simply invoking your Discord @name. e.g. /player_stats_by_game_mode {@USERNAME}\n\n'

            '⚔️ **Discover all the battle modes in the World of W3Champions** ⚔️:\n'
            'Invoke the `/battle_modes` command to reveal all available battle modes.\n\n'

            '🌙 **Seeking guidance, young adventurer?** 🌙:\n'
            'To access this help message again, simply use the `/help` command.\n\n'

            # '📜 **Guardian\'s Scroll**: The W3C Bot, safeguarded by Medivh, stands in its **BETA** phase. '
            # 'Winds of magic can be unpredictable... Should you encounter misplaced enchantments or if the bot '
            # 'drifts into the void, seek **@SageNoob** in the ethereal chambers of Discord. Remember, '
            # 'this spellwork is an open grimoire, a testament to the open-source magic of our world. Brave '
            # 'souls wishing to enrich its pages are welcome to journey to the arcane library 📚 of Github: '
            # 'https://github.com/0nlyDev/w3c-discord-bot. Your wisdom and contributions illuminate our path.'
    },
    'player_stats_by_game_mode': {
        'select_player': '🌌 From the depths of the Dark Portal, select your champion below:',
        'no_players_found': '🌌 In the vastness beyond the Dark Portal, this champion remains a mystery.',
        'load_more_search_results': '🌀 Summon more champions from the depths...',
        'loaded_more_search_results': '🌌 Through the Dark Portal, more champions emerge!',
        'end_of_search': '🌌 By the Light! It seems like we\'ve reached the end of our journey! No more champions '
                         'emerge from the Dark Portal. Try with a different Champion name...',
        'hide_season_zero': 'W3C: This noble person was part of our beta, therefore we hide their buggy stats and thank'
                            ' them for all eternity ;)',
        'message_made_visible_by': 'has summoned this message.',
        'discord_user_is_none': '{PLAYER_NAME} remains elusive in the scrolls of my Ancient Archives. Please ask {'
                                'PLAYER_NAME} to remedy this by linking their BattleTag with their Discord identity, '
                                'using the `/my_battle_tag <BattleTag>` command.'
    },
    'embeds': {
        'footer': 'W3C Bot: I\'m currently in BETA phase, and my code is still being sharpened.\n'
                  'Encounter a bug? Scribe an Issue on GitHub or whisper @SageNoob!',
        'no_stats_found': '🌌 The Dark Portal\'s manifest is void for this Champion.'
    },
    'my_battle_tag': {
        'show_user_battle_tag': '🔮 Champion, behold your BattleTag: {BATTLE_TAG}',
        'user_w/o_battle_tag': '📜 Noble Champion, your Discord identity is yet unlinked to a BattleTag. To link your '
                               'BattleTag, use the same command followed by your BattleTag.\n'
                               'e.g. `/my_battle_tag happy#2384`',
        'battle_tag_saved': '🔗 Success! A link has been forged in my ancient archives, between your Discord identity '
                            'and your BattleTag {BATTLE_TAG}. Now fellow champions can summon your tales from the '
                            'World Of W3Champions by simply calling upon your Discord name.\ne.g. '
                            '/player_stats_by_game_mode {@MENTION}',
        'player_not_found': '🔍 Alas! The champion `{BATTLE_TAG}` eludes our search in the World Of W3Champions. Verify'
                            ' that your BattleTag was spelled correctly and ensure you have an account registered in '
                            'the halls of https://www.w3champions.com/ with at least one ranked game played.',
        'invalid_battle_tag': '⚠️ Beware, brave champion! Your BattleTag must bear the mark of a hashtag `#`, akin to '
                              '`happy#2384`, to be deemed worthy.'
    },
    'error_responses': {
        'connection_error': '⚠️ A troubling ConnectionError, sent by W3Champions, has found its way back to us. '
                            'Please attempt again later.'
    }
}


def active_modes_response():
    return ', '.join([f'`{k}`' for k in get_active_modes().keys()])

from w3c_endpoints.active_modes import get_active_modes

responses = {
    'help': {
        'help_response':
            '🔥 **W3C Bot Slash Commands to reveal the World of W3Champions** 🔥:\n\n'

            '🔎 **Seek champions by Name or Battle Tag to reveal their legendary stats** 🔎:\n'
            'To initiate a search, use the `/player_stats_by_game_mode` command followed by the '
            'player\'s name or Battle Tag.\n'
            'e.g., `/player_stats_by_game_mode Moon` or `/player_stats_by_game_mode happy#2384`\n'
            'If you know the Champion\'s GateWay, you can add an additional argument in the search.\n'
            'e.g. `/player_stats_by_game_mode Grubby Europe`\n'
            'Select from the available options or type the player\'s name or Battle Tag to initiate a search.\n'
            'You can load additional results by selecting the "🌀 Summon more champions from the depths..." option '
            'from the dropdown menu.\n\n'

            '⚔️ **Discover all the battle modes in the World of W3Champions** ⚔️:\n'
            'Use the `/battle_modes` command to reveal all available battle modes.\n\n'

            '🌙 **Seeking guidance, young adventurer?** 🌙:\n'
            'To access this help message again, simply use the `/help` command.\n\n'

            '📜 **Guardian\'s Scroll**: The W3C Bot, safeguarded by Medivh, stands in its **BETA** phase. '
            'Winds of magic can be unpredictable... Should you encounter misplaced enchantments or if the bot '
            'drifts into the void, seek **@SageNoob** in the ethereal chambers of Discord. Remember, '
            'this spellwork is an open grimoire, a testament to the open-source magic of our world. Brave '
            'souls wishing to enrich its pages are welcome to journey to the arcane library 📚 of Github: '
            'https://github.com/0nlyDev/w3c-discord-bot. Your wisdom and contributions illuminate our path.'
    },
    'player_stats_by_game_mode': {
        'select_player': '🌌 From the depths of the Dark Portal, select your champion below:',
        'no_players_found': '🌌 In the vastness beyond the Dark Portal, this champion remains a mystery.',
        'load_more_search_results': '🌀 Summon more champions from the depths...',
        'loaded_more_search_results': '🌌 Through the Dark Portal, more champions emerge!',
        'end_of_search': '🌌 By the Light! It seems like we\'ve reached the end of our journey! No more champions '
                         'emerge from the Dark Portal. Try with a different Champion name...'
    }
}


def active_modes_response():
    return ', '.join([f'`{k}`' for k in get_active_modes().keys()])

import re
import json

import requests


def active_modes_request():
    try:
        url = "https://website-backend.w3champions.com/api/ladder/active-modes"

        payload = ""
        headers = {"User-Agent": "insomnia/8.3.0"}

        response = requests.request("GET", url, data=payload, headers=headers)
        if response:
            return json.loads(response.text)
    except Exception as e:
        raise e


def get_active_modes():
    # active_modes = active_modes_request()
    # if active_modes:
    #     active_game_modes = {}
    #     for mode in active_modes:
    #         mode_name = re.sub(r'\s+', '', mode['name'])
    #         active_game_modes.update({mode_name: mode['id']})
    #     return active_game_modes
    return {'1vs1': 1, '2vs2': 2, '4vs4': 4, 'FFA': 5, 'LegionTD1v1': 203, 'LegionTD4v4': 202, 'RoC1vs1': 301,
            'AllTheRandoms1vs1': 601, 'SurvivalChaos': 1001, 'LineTowerWarsFFA': 402, 'PTR1vs1': 801}
    # TODO invert the dict so that the ID is the key


def get_game_mode_id(mode_name):
    active_game_modes = get_active_modes()
    active_game_modes_lowercase = {k.lower(): v for k, v in active_game_modes.items()}
    if mode_name.lower() in active_game_modes_lowercase.keys():
        return active_game_modes_lowercase[mode_name.lower()]


def get_game_mode_from_id(game_mode_id):
    active_game_modes = get_active_modes()
    for k, v in active_game_modes.items():
        if game_mode_id == v:
            return k
    return f'gameModeID: {str(game_mode_id)}'

# print(get_game_mode_from_id(1))

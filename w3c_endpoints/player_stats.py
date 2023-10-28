import json
import requests

from w3c_endpoints.active_modes import get_game_mode_id
from w3c_endpoints.seasons import get_current_season

RACES = {
    0: ['rnd', 'random', 'rn'],
    1: ['hu', 'human'],
    2: ['oc', 'orc'],
    4: ['ne', 'night elf', 'night_elf', 'nightelf' 'elf', 'nelf'],
    8: ['ud', 'undead'],
    16: ['total']
}


def get_region_id(region):
    region = region.lower()
    if region in ['eu', 'europe']:
        return 20
    elif region in ['us', 'usa', 'america']:
        return 10
    else:
        return 0


def get_race_id(race):
    for race_id, race_names in RACES.items():
        if race in race_names:
            return race_id


def parse_bnet_tag(bnet_tag):
    return bnet_tag.replace('#', '%23').lower()


def get_player_stats(bnet_tag, region, game_mode=None, race=None, season=None):
    if season is None:
        season = get_current_season()
    try:
        url = f'https://website-backend.w3champions.com/api/players/{parse_bnet_tag(bnet_tag)}/game-mode-stats'

        querystring = {"gateWay": get_region_id(region), "season": season}

        payload = ""
        headers = {"User-Agent": "insomnia/8.3.0"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        player_stats = json.loads(response.text)

        selected_stats = []
        for stats in player_stats:
            if game_mode:
                if stats['gameMode'] == get_game_mode_id(game_mode):
                    if race:
                        if stats['race'] == get_race_id(race):
                            selected_stats.append(stats)
                    else:
                        selected_stats.append(stats)
            else:
                if race:
                    if stats['race'] == get_race_id(race):
                        selected_stats.append(stats)
                else:
                    selected_stats.append(stats)
        if selected_stats:
            return selected_stats
    except Exception as e:
        raise e


# for i in get_player_stats('COLORADO16#11383', 'eu', '2vs2'):
#     for k, v in i.items():
#         print(f'{k}: {v}')

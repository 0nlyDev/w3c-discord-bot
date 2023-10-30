import json
import requests

from w3c_endpoints.active_modes import get_game_mode_id
from w3c_endpoints.player_search import player_search_endpoint

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
    return bnet_tag.replace('#', '%23')


# def find_player_region(bnet_tag):


def get_player_stats(bnet_tag, region=None, game_mode=None, race=None, season=None):
    recursion = False
    if region is None:
        region = 'eu'
        print('Guessing region, 1st time.')

    if season is None:
        players = player_search_endpoint(bnet_tag)
        if players and players[0]['seasons']:
            season = players[0]['seasons'][0]['id']  # get last played season
        else:
            return
    try:
        url = f'https://website-backend.w3champions.com/api/players/{parse_bnet_tag(bnet_tag)}/game-mode-stats'

        querystring = {"gateWay": get_region_id(region), "season": season}

        payload = ""
        headers = {"User-Agent": "insomnia/8.3.0"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        player_stats = json.loads(response.text)
        if not player_stats and region != 'us':
            recursion = True
            print('trying to guess region, 2nd time.', bnet_tag)
            player_stats = get_player_stats(bnet_tag, 'us', game_mode, race, season)
        if recursion:
            return player_stats
        else:
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


# print(get_player_stats('happy#2384'))
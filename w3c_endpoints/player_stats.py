import json
import requests

from w3c_endpoints.player_search import player_search_endpoint
from responses import responses

RACES = {
    0: ['rnd', 'random', 'rn'],
    1: ['hu', 'human'],
    2: ['oc', 'orc'],
    4: ['ne', 'night elf', 'night_elf', 'nightelf' 'elf', 'nelf'],
    8: ['ud', 'undead'],
    16: ['total']
}


def get_gate_way_id(gate_way):
    gate_way = gate_way.lower()
    if gate_way in ['eu', 'europe']:
        return 20
    elif gate_way in ['us', 'usa', 'america']:
        return 10
    else:  # china?
        return 0


def get_race_id(race):
    for race_id, race_names in RACES.items():
        if race in race_names:
            return race_id


def parse_bnet_tag(bnet_tag):
    return bnet_tag.replace('#', '%23')


def get_player_stats(bnet_tag, gate_way=None, season=None):
    if gate_way is None:
        gate_way = 'europe'
        print('Guessing gate_way, 1st time (europe).')

    if season is None:
        players = player_search_endpoint(bnet_tag)
        if players and isinstance(players, list) and players[0]['seasons']:
            season = players[0]['seasons'][0]['id']  # get last played season
        elif isinstance(players, requests.exceptions.ConnectionError):
            return responses['error_responses']['connection_error']
        else:
            return None, gate_way
    try:
        url = f'https://website-backend.w3champions.com/api/players/{parse_bnet_tag(bnet_tag)}/game-mode-stats'

        querystring = {"gateWay": get_gate_way_id(gate_way), "season": season}

        payload = ""
        headers = {"User-Agent": "insomnia/8.3.0"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        player_stats = json.loads(response.text)
        if not player_stats and gate_way != 'america':
            print('trying to guess gate_way, 2nd time (america).', bnet_tag)
            player_stats, gate_way = get_player_stats(bnet_tag, gate_way='america', season=season)
        return player_stats, gate_way
    except Exception as e:
        raise e

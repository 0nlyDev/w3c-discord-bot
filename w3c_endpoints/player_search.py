import json
import os
import requests

current_directory = os.path.dirname(os.path.abspath(__file__))
emojis_file_path = os.path.join(current_directory, "..", "assets", "emojis.json")

with open(emojis_file_path, 'r', encoding='utf-8') as file:
    EMOJIS = json.load(file)


def emojify_number(number):
    emojified_number = ''.join([EMOJIS[c] for c in str(number)])
    return emojified_number


def player_search_endpoint(player_name, last_object_id=None):
    url = "https://website-backend.w3champions.com/api/players/global-search"
    if last_object_id is None:
        querystring = {"search": player_name, "pageSize": "20"}
    else:
        querystring = {"search": player_name, "pageSize": "20", "lastObjectId": last_object_id.replace('#', '%23')}

    payload = ""
    headers = {"User-Agent": "insomnia/8.3.0"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    player_search_results = json.loads(response.text)

    return player_search_results


def player_search(player_name, last_object_id=None):
    player_search_results = player_search_endpoint(player_name, last_object_id)

    players = []
    for player in player_search_results:
        bnet_tag = player['battleTag']
        if '#' not in bnet_tag:
            continue
        seasons = [i['id'] for i in player['seasons']]
        emojified_seasons = ' '.join([emojify_number(s) for s in seasons])
        player_string = f'{bnet_tag} | seasons: {emojified_seasons}'
        players.append(player_string)
    if players:
        players.append('🌀 Summon more champions from the depths...')
    print(len(players), players)
    return players


# player_search('Moon')

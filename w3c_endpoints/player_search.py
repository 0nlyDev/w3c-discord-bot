import json
import os
import time

import requests

# Get the directory of the currently executing file
current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the path to emojis.json relative to the current directory
emojis_file_path = os.path.join(current_directory, "..", "assets", "emojis.json")

with open(emojis_file_path, 'r', encoding='utf-8') as file:
    EMOJIS = json.load(file)


def emojify_number(number):
    emojified_number = ''.join([EMOJIS[c] for c in str(number)])
    return emojified_number


def player_search_endpoint_recursive(player_name, player_search_results, last_object_id=None):
    url = "https://website-backend.w3champions.com/api/players/global-search"
    if last_object_id == '':
        querystring = {"search": player_name, "pageSize": "20"}
    else:
        querystring = {"search": player_name, "pageSize": "20", "lastObjectId": last_object_id}

    payload = ""
    headers = {"User-Agent": "insomnia/8.3.0"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    current_player_search_results = json.loads(response.text)

    if player_search_results != current_player_search_results:
        time.sleep(1)
        if current_player_search_results:
            player_search_results += current_player_search_results
            last_bnet_tag = current_player_search_results[-1]['battleTag']
            last_object_id = last_bnet_tag.replace('#', '%23')
            player_search_results = player_search_endpoint_recursive(player_name, player_search_results, last_object_id)
    return player_search_results


def player_search(player_name):
    player_search_results = []
    player_search_results = player_search_endpoint_recursive(player_name, player_search_results)

    players = []
    for player in player_search_results:
        bnet_tag = player['battleTag']
        if '#' not in bnet_tag:
            continue
        seasons = [i['id'] for i in player['seasons']]
        emojified_seasons = ' '.join([emojify_number(s) for s in seasons])
        player_string = f'{bnet_tag} | seasons: {emojified_seasons}'
        players.append(player_string)
    # print(len(players), players)
    return players


# player_search('Moon')

import json
import os
import requests

from responses import responses

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
    try:
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        player_search_results = json.loads(response.text)
        return player_search_results
    except requests.exceptions.ConnectionError as e:
        print(f'⚠️ requests.exceptions.ConnectionError: {str(e)}')
        return requests.exceptions.ConnectionError


def player_search(player_name, last_object_id=None, return_players_string=True):
    player_search_results = player_search_endpoint(player_name, last_object_id)
    if isinstance(player_search_results, requests.exceptions.ConnectionError):
        return responses['error_responses']['connection_error']

    players = {}
    emojified_player_strings = []
    # TODO: handle ide warning here
    for player in player_search_results:
        bnet_tag = player['battleTag']
        if '#' not in bnet_tag:
            continue
        seasons = [i['id'] for i in player['seasons']]
        players.update({bnet_tag: seasons})
    players = clean_dictionary(players)
    for bnet_tag, seasons in players.items():
        emojified_seasons = ' '.join([emojify_number(s) for s in seasons])
        player_string = f'{bnet_tag} | seasons: {emojified_seasons}'
        emojified_player_strings.append(player_string)
    if return_players_string:
        return emojified_player_strings
    else:
        return players


def clean_dictionary(d):
    # Convert all keys to lowercase and count occurrences, also keep track of original case keys
    key_counts = {}
    original_keys = {}
    for key in d.keys():
        lower_key = key.lower()
        key_counts[lower_key] = key_counts.get(lower_key, 0) + 1
        original_keys.setdefault(lower_key, []).append(key)

    # Identify and remove keys with duplicates and empty list values
    keys_to_remove = []
    for lower_key, count in key_counts.items():
        if count > 1:
            for orig_key in original_keys[lower_key]:
                if not d[orig_key]:
                    keys_to_remove.append(orig_key)

    for key in keys_to_remove:
        del d[key]

    return d

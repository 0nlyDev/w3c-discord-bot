import json

import requests


def player_endpoint(bnet_tag):
    url = f'https://website-backend.w3champions.com/api/players/{bnet_tag.replace("#", "%23")}'

    payload = ""
    headers = {"User-Agent": "insomnia/8.3.0"}

    response = requests.request("GET", url, data=payload, headers=headers)

    return json.loads(response.text)


def get_player_participated_in_seasons(bnet_tag):
    return [i['id'] for i in player_endpoint(bnet_tag)['participatedInSeasons']]

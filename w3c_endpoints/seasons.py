import json
import requests


def season_request():
    try:
        url = "https://website-backend.w3champions.com/api/ladder/seasons"

        payload = ""
        headers = {"User-Agent": "insomnia/8.3.0"}

        response = requests.request("GET", url, data=payload, headers=headers)
        if response:
            return json.loads(response.text)
    except Exception as e:
        print(e)


def get_current_season():
    seasons_response = season_request()
    if isinstance(seasons_response, list):
        return seasons_response[0]['id']
    else:
        return seasons_response


def get_all_seasons():
    seasons_response = season_request()
    if isinstance(seasons_response, list):
        return seasons_response

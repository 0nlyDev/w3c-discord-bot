import requests
import json

with open('./configs/config.json', 'r') as file:
    data = json.load(file)
BOT_TOKEN = data["token"]

# Your Application ID from Discord's Developer Portal
CLIENT_ID = data['application_id']

# Define the commands
commands = [
    {
        'name': 'help',
        'description': 'Seeking guidance, adventurer? Look no further!'.lower()
    },
    {
        'name': 'player_stats_by_game_mode',
        'description': 'Reveal the legendary stats of players in the World of W3Champions.'.lower()
    },
    {
        'name': 'battle_modes',
        'description': 'Discover all the battle modes available.'.lower()
    }
]

headers = {
    'Authorization': f'Bot {BOT_TOKEN}',
    'Content-Type': 'application/json'
}

response = requests.put(f'https://discord.com/api/v10/applications/{CLIENT_ID}/commands', headers=headers,
                        data=json.dumps(commands))

if response.status_code == 200:
    print('Global commands registered successfully!')
else:
    print(f'Failed to register global commands. Status code: {response.status_code}. Response: {response.text}')

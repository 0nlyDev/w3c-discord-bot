import json
import re
import discord
import responses


async def send_message(message, user_message):
    if user_message.startswith('!w3c'):
        print(f'"{message.content}", from {message.author} via {message.guild}')
        debugging_mode = True
        if debugging_mode:
            if str(message.guild) != 'SageNoobTesting':
                await message.reply('I am sorry, I am out of service right now. I am currently in development, '
                                    'being upgraded with more bells and whistles, please check back later.\nIf '
                                    'you have any questions, reach out to `@SageNoob` via Discord or on '
                                    'github: https://github.com/0nlyDev/w3c-discord-bot', mention_author=False)
                return
        try:
            response, view = responses.handle_response(user_message)
            if response:
                await message.reply(response, view=view, mention_author=False)
            else:
                await message.reply(f'I am sorry, something went wrong... {str(response)}', mention_author=False)
        except Exception as e:
            raise e


def run_discord_bot():
    with open('./configs/config.json', 'r') as file:
        data = json.load(file)

    token = data["token"]

    intents = discord.Intents.default()
    intents.message_content = True  # explicitly enable the message content intents
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user_message = re.sub(r'\s+', ' ', str(message.content))
        await send_message(message, user_message)

    client.run(token)

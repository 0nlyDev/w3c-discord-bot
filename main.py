import json
import os

import discord
from discord.ext import commands
from db_queries.database import get_engine, initialize_database


class W3ChampionsBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',  # must have this for some wired reason...
            intents=discord.Intents.default())

        with open('./configs/config.json', 'r') as file:
            data = json.load(file)
        self.token = data["token"]

        self.initial_extensions = []
        for root, dirs, files in os.walk('./cogs'):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(os.path.normpath(root), file_name.split(os.extsep)[0])
                    cog = '.'.join(file_path.split(os.path.sep))
                    self.initial_extensions.append(cog)

    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        print(f'{self.user} is now running!')
        synced = await self.tree.sync()
        print(f'Slash commands synced: {len(synced)}')

    async def close(self):
        await super().close()
        await self.session.close()


# Create tables in the database (this is safe to run multiple times as it will not recreate tables that already exist)
initialize_database(get_engine())
# Run the bot
client = W3ChampionsBot()
client.run(client.token)

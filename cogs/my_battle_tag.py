from discord import app_commands
from discord.ext import commands

from responses import responses
from w3c_endpoints.player_search import player_search
from db_queries.database import get_engine, create_session
from db_queries.operations import get_user, upsert_user


class MyBattleTag(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='my_battle_tag', description='Save your BattleTag by adding it after the command, '
                                                            'or run the command alone to view your BattleTag.')
    @app_commands.describe(battle_tag='Your BattleTag, e.g. happy#2384')
    async def my_battle_tag(self,
                            interaction,
                            battle_tag: str = None):
        print(f'{interaction.user.display_name} from {interaction.guild.name} used /my_battle_tag')
        user_provided_battle_tag = battle_tag
        # Display user BattleTag
        if battle_tag is None:
            #  If there's an associated BattleTag for this user in the database, display their BattleTag
            engine = get_engine()
            session = create_session(engine)
            user = get_user(session, interaction.user.id)
            if user:
                battle_tag = user.battle_tag
            session.close()
            if battle_tag:
                url = f'https://www.w3champions.com/player/{battle_tag.replace("#", "%23")}'
                this_response = responses['my_battle_tag']['show_user_battle_tag'].replace(
                    '{BATTLE_TAG}', f'[{battle_tag}]({url})')
                await interaction.response.send_message(content=this_response, ephemeral=True)
            else:
                #  Display how-to save your battle tag message
                await interaction.response.send_message(content=responses['my_battle_tag']['user_w/o_battle_tag'],
                                                        ephemeral=True)
        # Upsert BattleTag
        elif '#' in battle_tag:
            search_results = player_search(battle_tag, return_players_string=False)
            # if the search returns a single result, save the battle tag
            if len(search_results) == 1:
                battle_tag = next(iter(search_results))
                engine = get_engine()
                session = create_session(engine)
                result = upsert_user(session, interaction.user.id, interaction.user.name, battle_tag)
                print(result)
                session.close()
                url = f'https://www.w3champions.com/player/{battle_tag.replace("#", "%23")}'
                this_response = responses['my_battle_tag']['battle_tag_saved'].replace(
                    '{BATTLE_TAG}', f'[{battle_tag}]({url})')
                this_response = this_response.replace('{@MENTION}', interaction.user.mention)
                await interaction.response.send_message(content=this_response, ephemeral=True)
                print(f'BattleTag saved: {battle_tag}')
            elif len(search_results) > 1:
                print(f'WARNING: More than 1 BattleTag was found in search_results.\n'
                      f'user_provided_battle_tag: {user_provided_battle_tag}\n'
                      f'search_results: {search_results}')
            else:
                print(f'BattleTag not found on w3champions: "{battle_tag}"')
                await interaction.response.send_message(
                    content=responses['my_battle_tag']['player_not_found'].replace('{BATTLE_TAG}', battle_tag),
                    ephemeral=True)
        # Invalid BattleTag format
        else:
            await interaction.response.send_message(content=responses['my_battle_tag']['invalid_battle_tag'],
                                                    ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(MyBattleTag(client))

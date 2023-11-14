from discord import app_commands
from discord.ext import commands

from responses import responses
from w3c_endpoints.player_search import player_search


def get_battle_tag_from_username(user):
    print(f'Getting BattleTag for {user}')
    return ''


def save_battle_tag_in_database(user, battle_tag):
    print(f'Saving BattleTag for {user}, {battle_tag}')
    return ''


class MyBattleTag(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='my_battle_tag', description='Add or show your BattleTag.')
    @app_commands.describe(battle_tag='Your BattleTag. e.g. happy#2384')
    async def my_battle_tag(self,
                            interaction,
                            battle_tag: str = None):
        print(f'{interaction.user.display_name} from {interaction.guild.name} used /my_battle_tag')

        # Display user BattleTag
        if battle_tag is None:
            #  If there's an associated BattleTag for this user in the database, display their BattleTag
            battle_tag = get_battle_tag_from_username(interaction.user)
            if battle_tag:
                url = f'https://www.w3champions.com/player/{battle_tag.replace("#", "%23")}'
                this_response = responses['my_battle_tag']['show_user_battle_tag'].replace('{USERNAME}',
                                                                                           interaction.user.mention)
                this_response = this_response.replace('{BATTLE_TAG}', f'[{battle_tag}]({url})')
                await interaction.response.send_message(content=this_response, ephemeral=True)
            else:
                #  Display how-to save your battle tag message
                await interaction.response.send_message(content=responses['my_battle_tag']['user_w/o_battle_tag'],
                                                        ephemeral=True)
        # Save user BattleTag
        elif '#' in battle_tag:
            search_results = player_search(battle_tag)
            # if the search returns a single result, save the battle tag
            if len(search_results) == 1:
                battle_tag = search_results[0].split(' ')[0]
                save_battle_tag_in_database(interaction.user, battle_tag)
                await interaction.response.send_message(
                    content=responses['my_battle_tag']['battle_tag_saved'].replace('{BATTLE_TAG}', f'{battle_tag}'),
                    ephemeral=True)
                print(f'BattleTag saved: {battle_tag}')
            else:
                print(f'BattleTag not found on w3champions: "{battle_tag}"')
                await interaction.response.send_message(
                    content=responses['my_battle_tag']['player_not_found'], ephemeral=True)
        # Invalid BattleTag format
        else:
            await interaction.response.send_message(content=responses['my_battle_tag']['invalid_battle_tag'],
                                                    ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(MyBattleTag(client))

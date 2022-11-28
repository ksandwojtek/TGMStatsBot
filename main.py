#!python
import discord
import os
from structs.proxy import ProxyConnectorWrapper
from discord.ext import commands
from discord_slash import SlashCommand
from util.options import parse_arguments
from structs.global_vars import GlobalVariables

if __name__ == "__main__":
    global_variables = GlobalVariables()
    parse_arguments()

    intents = discord.Intents.all()
    connector = ProxyConnectorWrapper().connector
    client = commands.Bot(command_prefix=global_variables.config["bot"]["prefix"], intents=intents, connector=connector)
    global_variables.set_client(client)

    slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

    client.remove_command('help')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded command \"{filename[:-3]}\"')
            except Exception as e:
                print(e)
        else:
            # print(f'Unable to load {filename[:-3]}')
            pass


    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="PvPArca.de"))
        print(f'{client.user} has connected to Discord!')

    @global_variables.client.event
    async def on_reaction_add(reaction, user):

        def correct_message_get_and_check(reaction_message_id, user):
            if not global_variables.messages:
                return None
            for message in global_variables.messages:
                if message['message'].id == reaction_message_id and user == message['author']:
                    return message
            return None

        message_dict = correct_message_get_and_check(reaction.message.id, user)
        if message_dict is None:
            return

        if str(reaction) == '◀':
            if message_dict['page_number'] > 0:
                message_dict['page_number'] -= 1
                await message_dict['message'].edit(embed=message_dict['pages'][message_dict['page_number']])
        elif str(reaction) == '▶':
            if message_dict['page_number'] < len(message_dict['pages']) - 1:
                message_dict['page_number'] += 1
                await message_dict['message'].edit(embed=message_dict['pages'][message_dict['page_number']])
        try:
            # reaction, user = await global_variables.client.wait_for('reaction_add', timeout=45.0)
            await message_dict['message'].remove_reaction(reaction, user)
        except Exception as e:
            print(e)


    client.run(global_variables.config["bot"]["token"], reconnect=True)

#!python

import discord
import os

import json
import argparse
from discord.ext import commands
from GlobalVariables import GlobalVariables


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs an instance of the Cylone Stat Bot")
    parser.add_argument("-t", "--token", nargs="?", type=str, help="Discord bot token")
    parser.add_argument("-c", "--channel", nargs="?", type=int, help="Channel ID where the Discord Bot will respond "
                                                                     "to queries")
    args = parser.parse_args()

    with open("./config.json", mode="r") as fl:
        config = json.loads(fl.read())

    if args.token is not None:
        config["bot"]["token"] = args.token
    if args.channel is not None:
        config["bot"]["channel"] = args.channel

    global_variables = GlobalVariables()
    global_variables.set_config(config)


    intents = discord.Intents.all()
    client = commands.Bot(command_prefix=config["bot"]["prefix"], intents=intents, case_insensitive=True)

    client.remove_command('help')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

        else:
            print(f'Unable to load {filename[:-3]}')

    Cogs = client.cogs
    for NameOfCog, TheClassOfCog in Cogs.items():
        print(NameOfCog)


    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="CyloneMC.net"))
        print(f'{client.user} has connected to Discord!')

    client.run(config["bot"]["token"], reconnect=True)
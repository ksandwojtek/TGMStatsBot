import requests
import discord
import os
import aiohttp
import asyncio
import json
import datetime as dt
import time
from ago import human
from ago import delta2dict
from datetime import datetime
from discord.ext.commands import cooldown, BucketType
import datetime
from discord.ext import commands

intents = discord.Intents.all()

with open("./config.json", mode="r") as fl:
    config = json.loads(fl.read())

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

import requests
import discord
import os
import aiohttp
import asyncio
import json
import datetime as dt
import time
import random
import humanize
from discord.ext.commands import cooldown, BucketType
import timedelta
import datetime
import timeago, datetime
from datetime import date, timedelta
from discord.ext import commands

intents = discord.Intents.all()

with open("./config.json", mode="r") as fl:
    config = json.loads(fl.read()) 

client = commands.Bot(command_prefix=config["bot"]["prefix"], intents=intents, case_insensitive=True)

client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="CyloneMC.net"))
    print(f'{client.user} has connected to Discord!')

colors = [0x9400D3, 0x4B0082, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF0000]

now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

date = datetime.datetime.now()

########################################################################
########################################################################
########################################################################

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stats(ctx: commands.Context, mc_name : str):
    if ctx.channel.id == 852546541830012988:
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://tgmapi.cylonemc.net/mc/player/' + mc_name, ) as r:
                        res = await r.json()
                        skin = res['user']['uuid']
                        ms = res['user']['lastOnlineDate']
                        ms2 = res['user']['initialJoinDate']
                        embedVar = discord.Embed(title="", color=0xbc2a82)
                        embedVar.set_author(name=mc_name + " Stats on The Cylone Network")
                        embedVar.add_field(name="<a:played:853633469014605824> Matches played", value=(res['user']['matches']), inline=True)
                        embedVar.add_field(name="<a:kills:853628582731186177> Kills", value=(res['user']['kills']), inline=True)
                        embedVar.add_field(name="<a:wins:853628581698600961> Wins", value=(res['user']['wins']), inline=True)
                        embedVar.add_field(name="<:loses:853633469070835712> Losses", value=(res['user']['losses']), inline=True)
                        embedVar.add_field(name="<a:level:853628581188337666> Level", value=(res['user']['level']), inline=True)
                        embedVar.add_field(name="<a:wool:853628583535968286> Wool Destroys", value=(res['user']['wool_destroys']), inline=True)
                        embedVar.add_field(name="Last Online:", value=(timeago.format(ms/1000.0, now, 'en')), inline=True)
                        embedVar.add_field(name="Join Date:", value=(timeago.format(ms2/1000.0, now, 'en')), inline=True)
                        embedVar.timestamp = datetime.datetime.utcnow()
                        embedVar.set_footer(text='Bot Created by ksndq#8052', icon_url="https://cdn.discordapp.com/avatars/431703739913732097/013868d08ceb35bf90fb568bfbd1e854.png?size=64")
                        embedVar.set_image(url='https://crafatar.com/renders/head/' + skin)
                        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="You can't use that here!", color=0xFF0000)
        await ctx.send(embed=embedVar, delete_after=5.0)
        await ctx.message.delete()
        pass

@stats.error
async def stats(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embedVar = discord.Embed(title="Play more to unlock stats!", color=0xFF0000)
        await ctx.send(embed=embedVar, delete_after=5.0)
        await ctx.message.delete()
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=f"Command still on cooldown, try again in {error.retry_after:.2f} seconds!", color=0xFF0000)
        await ctx.send(embed=embedVar, delete_after=3.0)
        await ctx.message.delete()
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embedVar = discord.Embed(title=f"Please provide a player!", color=0xFF0000)
        await ctx.send(embed=embedVar, delete_after=3.0)
        await ctx.message.delete()
    else:
        pass

########################################################################

client.run(config["bot"]["token"], reconnect=True)
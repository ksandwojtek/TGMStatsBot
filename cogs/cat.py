import requests
import discord
import os
import aiohttp
import asyncio
import json
import datetime as dt
import time
from ago import human
import random
from ago import delta2dict
from datetime import datetime
from discord.ext.commands import cooldown, BucketType
import datetime
from discord.ext import commands
from globalvariables import GlobalVariables


class Cat(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.global_variables = GlobalVariables()

    @commands.Cog.listener()
    async def on_ready(self):
        pass



    @commands.command()
    async def cat(self, ctx: commands.context):
        if ctx.channel.id in self.global_variables.config['bot']['channels']:
            async with ctx.typing():
                async with aiohttp.ClientSession() as session:
                    catPicture = requests.get('http://thecatapi.com/api/images/get.php')
                    if catPicture.status_code == 200:
                        catPicture = catPicture.url
                    colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x2E2B5F, 0x8B00FF]
                    embed_Var = discord.Embed(title="Here is a cat! 🐈", color=random.choice(colors))
                    embed_Var.set_image(url=catPicture)   
                    await ctx.send(embed=embed_Var)
                    pass

def setup(client):
    client.add_cog(Cat(client))

import requests
import discord
import aiohttp
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from globalvariables import GlobalVariables


async def process_cat_command(self, ctx):
    if ctx.channel.id in self.global_variables.config['bot']['channels']:
        async with aiohttp.ClientSession() as session:
            catPicture = requests.get('http://thecatapi.com/api/images/get.php')
            if catPicture.status_code == 200:
                catPicture = catPicture.url
            colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x2E2B5F, 0x8B00FF]
            embed_Var = discord.Embed(title="Here is a cat! 🐈", color=random.choice(colors))
            embed_Var.set_image(url=catPicture)
            await ctx.send(embed=embed_Var)
            pass


class Cat(commands.Cog):
    global_variables = GlobalVariables()
    guild_ids = global_variables.config['bot']['guilds']

    def __init__(self, client):
        pass

    @commands.command()
    async def cat(self, ctx: commands.context):
        await process_cat_command(self, ctx)

    @cog_ext.cog_slash(name='Cat', description='Shows you an image of a cat', guild_ids=guild_ids)
    async def _cat(self, ctx: SlashContext):
        await process_cat_command(self, ctx)


def setup(client):
    client.add_cog(Cat(client))

import discord
import aiohttp
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from structs.proxy import ProxyConnectorWrapper
from structs.globals import GlobalVariables


async def process_cat_command(self, ctx):
    if ctx.channel.id in self.global_variables.config['bot']['channels']:
        connector = ProxyConnectorWrapper().connector
        async with aiohttp.ClientSession(connector=connector) as cs:
            async with cs.get('https://thecatapi.com/api/images/get.php') as r:
                if r.status == 200:
                    cat_picture = r.url
                colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x2E2B5F, 0x8B00FF]
                embed_var = discord.Embed(title="Here is a cat! 🐈", color=random.choice(colors))
                embed_var.set_image(url=cat_picture)
                await ctx.send(embed=embed_var)
    else:
        embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
        await ctx.send(embed=embed_var, delete_after=5.0)


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

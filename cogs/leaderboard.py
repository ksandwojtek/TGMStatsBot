import discord
import aiohttp

from aiohttp_socks import ProxyConnector
from datetime import datetime
import datetime
from discord.ext import commands

from customobjects import ProxyConnectorWrapper
from globalvariables import GlobalVariables


class Leaderboard(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.global_variables = GlobalVariables()
        self.leaderboard_prefix = {0: ":first_place:", 1: ":second_place:", 2: ":third_place:"}

    def create_embed(self, res, page_number: int, leaderboard_type: str):
        #######
        #######
        if leaderboard_type == "xp":
            leaderboard_type = "level"

        page = discord.Embed(title="", color=0xbc2a82)
        page.set_author(name="Cylone Network " + leaderboard_type.title() + " Leaderboard " + str(page_number) + "/4")

        for i in range(0, 10):
            leaderboard_prefix = self.leaderboard_prefix.get(i, "")
            page.add_field(name=leaderboard_prefix + " " + str(i + 1) + ". " + res[i]['name'],
                            value=res[i][leaderboard_type], inline=False)

        page.timestamp = datetime.datetime.utcnow()
        page.set_footer(text='Bot Created by ksndq and LordofLightning',
                         icon_url="https://cdn.discordapp.com/icons/754890606173487154"
                                  "/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
        ################################################################
        return page

    @commands.command(aliases=["lb", "leaderboards"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, ctx: commands.context):
        if ctx.channel.id in self.global_variables.config['bot']['channels']:
            async with ctx.typing():
                connector = ProxyConnectorWrapper().connector
                async with aiohttp.ClientSession(connector=connector) as cs:
                    stat_types = ['kills', 'wins', 'xp', 'losses']
                    pages = []
                    for i in range(0, len(stat_types)):
                        async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/' + stat_types[i]) as r:
                            res = await r.json()
                            pages.append(self.create_embed(res, i + 1, stat_types[i]))

        else:
            embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
            await ctx.send(embed=embed_var)
            pass

        message = await ctx.send(embed=pages[0])
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        self.global_variables.messages.append({"message": message, "author": ctx.author, "pages": pages, "page_number": 0})


def setup(client):
    client.add_cog(Leaderboard(client))

import discord
import aiohttp

from datetime import datetime
import datetime
from discord.ext import commands
from GlobalVariables import GlobalVariables


class Leaderboard(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.global_variables = GlobalVariables()
        self.leaderboard_prefix = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:"}

    def create_embed(self, res, page_number: int, leaderboard_type: str):
        #######
        #######
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
        if ctx.channel.id == self.global_variables.config['bot']['channel']:
            async with ctx.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/kills') as r:
                        res = await r.json()
                        page1 = self.create_embed(res, 1, 'kills')

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/wins') as r:
                                res = await r.json()
                        page2 = self.create_embed(res, 2, 'wins')

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/xp') as r:
                                res = await r.json()
                        page3 = self.create_embed(res, 3, 'level')

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/losses') as r:
                                res = await r.json()
                        page4 = self.create_embed(res, 4, 'losses')
        else:
            embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
            await ctx.send(embed=embed_var)
            pass

        pages = [page1, page2, page3, page4]
        message = await ctx.send(embed=page1)
        await message.add_reaction('◀')
        await message.add_reaction('▶')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i])
            elif str(reaction) == '▶':
                if i < 3:
                    i += 1
                    await message.edit(embed=pages[i])
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=45.0, check=check)
                await message.remove_reaction(reaction, user)
            except Exception as e:
                print(e)
                break
        await message.clear_reactions()


def setup(client):
    client.add_cog(Leaderboard(client))

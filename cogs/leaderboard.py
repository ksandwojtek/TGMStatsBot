import discord
import aiohttp

from ago import human
from datetime import datetime
import datetime
from discord.ext import commands
from GlobalVariables import GlobalVariables


class Leaderboard(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.global_variables = GlobalVariables()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, ctx: commands.context):
        if ctx.channel.id == self.global_variables.config['bot']['channel']:
            async with ctx.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/kills') as r:
                        res = await r.json()
                        #######
                        #######
                        page1 = discord.Embed(title="", color=0xbc2a82)
                        page1.set_author(name="Cylone Network Kills Leaderboard 1/4")
                        page1.add_field(name=":first_place: 1. " + res[0]['name'], 
                                        value=res[0]['kills'], inline=False)
                        page1.add_field(name=":second_place: 2. "+ res[1]['name'],
                                        value=res[1]['kills'], inline=False)
                        page1.add_field(name=":third_place: 3. "+ res[2]['name'],
                                        value=res[2]['kills'], inline=False)
                        page1.add_field(name="4. "+ res[3]['name'],
                                        value=res[3]['kills'], inline=False)
                        page1.add_field(name="5. "+ res[4]['name'],
                                        value=res[4]['kills'], inline=False)
                        page1.add_field(name="6. "+ res[5]['name'],
                                        value=res[5]['kills'], inline=False)
                        page1.add_field(name="7. "+ res[6]['name'],
                                        value=res[6]['kills'], inline=False)
                        page1.add_field(name="8. "+ res[7]['name'],
                                        value=res[7]['kills'], inline=False)
                        page1.add_field(name="9. "+ res[8]['name'],
                                        value=res[8]['kills'], inline=False)
                        page1.add_field(name="10. "+ res[9]['name'],
                                        value=res[9]['kills'], inline=False)
                        page1.timestamp = datetime.datetime.utcnow()
                        page1.set_footer(text='Bot Created by ksndq and LordofLightning', icon_url="https://cdn.discordapp.com/icons/754890606173487154/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
                    ################################################################
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/wins') as r:
                                res = await r.json()
                        page2 = discord.Embed(title="", color=0xbc2a82)
                        page2.set_author(name="Cylone Network Wins Leaderboard 2/4")
                        page2.add_field(name=":first_place: 1. " + res[0]['name'], 
                                        value=res[0]['wins'], inline=False)
                        page2.add_field(name=":second_place: 2. "+ res[1]['name'],
                                        value=res[1]['wins'], inline=False)
                        page2.add_field(name=":third_place: 3. "+ res[2]['name'],
                                        value=res[2]['wins'], inline=False)
                        page2.add_field(name="4. "+ res[3]['name'],
                                        value=res[3]['wins'], inline=False)
                        page2.add_field(name="5. "+ res[4]['name'],
                                        value=res[4]['wins'], inline=False)
                        page2.add_field(name="6. "+ res[5]['name'],
                                        value=res[5]['wins'], inline=False)
                        page2.add_field(name="7. "+ res[6]['name'],
                                        value=res[6]['wins'], inline=False)
                        page2.add_field(name="8. "+ res[7]['name'],
                                        value=res[7]['wins'], inline=False)
                        page2.add_field(name="9. "+ res[8]['name'],
                                        value=res[8]['wins'], inline=False)
                        page2.add_field(name="10. "+ res[9]['name'],
                                        value=res[9]['wins'], inline=False)
                        page2.timestamp = datetime.datetime.utcnow()
                        page2.set_footer(text='Bot Created by ksndq and LordofLightning', icon_url="https://cdn.discordapp.com/icons/754890606173487154/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
                    ###############################################################
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/xp') as r:
                                res = await r.json()
                        page3 = discord.Embed(title="", color=0xbc2a82)
                        page3.set_author(name="Cylone Network Level Leaderboard 3/4")
                        page3.add_field(name=":first_place: 1. " + res[0]['name'], 
                                        value=res[0]['level'], inline=False)
                        page3.add_field(name=":second_place: 2. "+ res[1]['name'],
                                        value=res[1]['level'], inline=False)
                        page3.add_field(name=":third_place: 3. "+ res[2]['name'],
                                        value=res[2]['level'], inline=False)
                        page3.add_field(name="4. "+ res[3]['name'],
                                        value=res[3]['level'], inline=False)
                        page3.add_field(name="5. "+ res[4]['name'],
                                        value=res[4]['level'], inline=False)
                        page3.add_field(name="6. "+ res[5]['name'],
                                        value=res[5]['level'], inline=False)
                        page3.add_field(name="7. "+ res[6]['name'],
                                        value=res[6]['level'], inline=False)
                        page3.add_field(name="8. "+ res[7]['name'],
                                        value=res[7]['level'], inline=False)
                        page3.add_field(name="9. "+ res[8]['name'],
                                        value=res[8]['level'], inline=False)
                        page3.add_field(name="10. "+ res[9]['name'],
                                        value=res[9]['level'], inline=False)
                        page3.timestamp = datetime.datetime.utcnow()
                        page3.set_footer(text='Bot Created by ksndq and LordofLightning', icon_url="https://cdn.discordapp.com/icons/754890606173487154/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
                    ################################################################
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get('https://tgmapi.cylonemc.net/mc/leaderboard/losses') as r:
                                res = await r.json()
                        page4 = discord.Embed(title="", color=0xbc2a82)
                        page4.set_author(name="Cylone Network Losses Leaderboard 4/4")
                        page4.add_field(name=":first_place: 1. " + res[0]['name'], 
                                        value=res[0]['losses'], inline=False)
                        page4.add_field(name=":second_place: 2. "+ res[1]['name'],
                                        value=res[1]['losses'], inline=False)
                        page4.add_field(name=":third_place: 3. "+ res[2]['name'],
                                        value=res[2]['losses'], inline=False)
                        page4.add_field(name="4. "+ res[3]['name'],
                                        value=res[3]['losses'], inline=False)
                        page4.add_field(name="5. "+ res[4]['name'],
                                        value=res[4]['losses'], inline=False)
                        page4.add_field(name="6. "+ res[5]['name'],
                                        value=res[5]['losses'], inline=False)
                        page4.add_field(name="7. "+ res[6]['name'],
                                        value=res[6]['losses'], inline=False)
                        page4.add_field(name="8. "+ res[7]['name'],
                                        value=res[7]['losses'], inline=False)
                        page4.add_field(name="9. "+ res[8]['name'],
                                        value=res[8]['losses'], inline=False)
                        page4.add_field(name="10. "+ res[9]['name'],
                                        value=res[9]['losses'], inline=False)
                        page4.timestamp = datetime.datetime.utcnow()
                        page4.set_footer(text='Bot Created by ksndq and LordofLightning', icon_url="https://cdn.discordapp.com/icons/754890606173487154/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
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
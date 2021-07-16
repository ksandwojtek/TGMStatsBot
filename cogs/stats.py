import discord
import aiohttp

from ago import human
from datetime import datetime
import datetime

from aiohttp_socks import ProxyConnector
from discord.ext import commands

from customobjects import EmbedField, ProxyConnectorWrapper
from globalvariables import GlobalVariables


class Stats(commands.Cog):
    global_variables = GlobalVariables()

    def __init__(self, client):
        pass

    @commands.command(aliases=['stat'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx: commands.context, requested_user: str):
        if ctx.channel.id in self.global_variables.config['bot']['channels']:
            async with ctx.typing():
                flags = ""
                requested_user_string_length = len(requested_user)
                # If requested_user is in the form of a Cylone playerID
                if (requested_user_string_length == 24):
                    flags += "?byID=true"
                # If requested_user is in the form of a Minecraft UUID without dashes
                elif (requested_user_string_length == 32):
                    requested_user = requested_user[0:8] + "-" \
                                     + requested_user[8:12] + "-" \
                                     + requested_user[12:16] + "-" \
                                     + requested_user[16:20] + "-" \
                                     + requested_user[20:32]
                    flags += "?byUUID=true"
                # If requested_user is in the form of a Minecraft UUID with dashes
                elif (requested_user_string_length == 36):
                    flags += "?byUUID=true"
                connector = ProxyConnectorWrapper().connector
                async with aiohttp.ClientSession(connector=connector) as cs:
                    async with cs.get('https://api.pvparca.de//mc/player/' + requested_user + flags, ) as r:
                        if (r.status == 522 or r.status == 502):
                            error_message = "The Cylone API is currently down, please wait for it to by " \
                                            "restored to get up-to-date statistics."
                            print(error_message)
                            embed_var = discord.Embed(title=error_message, color=0xFF0000)
                            await ctx.send(embed=embed_var)
                            # Add a cache that returns cached values if the API is down with the date of when the data
                            # Was last updated
                            return
                        res = await r.json()
                        # If the specified user, whether by username, UUID, or playerID does not exist
                        # We inform the user
                        if 'notFound' in res and res['notFound']:
                            # In the future, we should add something here to look up a player's name on Mojang's servers
                            # Or on NameMC to check if a username has been changed, if so tell the user that the player
                            # Who's stats they're looking up may have changed their name and deal with it appropiately
                            embed_var = discord.Embed(
                                title="The user you specified is not in Cylone's database, please check your spelling.",
                                color=0xFF0000)
                            await ctx.send(embed=embed_var)
                            return
                        #######
                        mc_name = res['user']['name']
                        skin = res['user']['uuid']
                        ms = res['user']['lastOnlineDate']
                        ms2 = res['user']['initialJoinDate']
                        win = res['user']['wins']
                        lost = res['user']['losses']
                        k = res['user']['kills']
                        d = res['user']['deaths']
                        #######
                        page1 = discord.Embed(title="", color=0xbc2a82)
                        page1.set_author(name=mc_name + " Stats on The Cylone Network 1/2")
                        page1_embed_fields = [
                            EmbedField(name="<a:played:853633469014605824> Matches played",
                                       value=res['user']['matches']),
                            EmbedField(name="<a:kills:853628582731186177> Kills", value=res['user']['kills']),
                            EmbedField(name="<a:deaths:855109742288437250> Deaths", value=res['user']['deaths']),
                            EmbedField(name="<a:kd:855110404735893515> K/D", value="{:.2f}".format(k / d)),
                            EmbedField(name="<a:level:853628581188337666> Level", value=res['user']['level']),
                            EmbedField(name="<a:wins:853628581698600961> Wins", value=res['user']['wins']),
                            EmbedField(name="<:loses:853633469070835712> Losses", value=res['user']['losses']),
                            EmbedField(name="<a:wl:855110803082313728> W/L", value="{:.2f}".format(win / lost)),
                            EmbedField(name="<a:wool:853628583535968286> Wool Destroys",
                                       value=res['user']['wool_destroys']),
                            EmbedField(name="Last Online", value=human(ms / 1000.0)),
                            EmbedField(name="Join Date", value=human(ms2 / 1000.0))]

                        for field in page1_embed_fields:
                            try:
                                page1.add_field(name=field.name, value=field.value, inline=True)
                            except KeyError:
                                page1.add_field(name=field.name, value="N/A", inline=True)

                        page1.timestamp = datetime.datetime.utcnow()
                        page1.set_footer(text='Bot Created by ksndq and LordofLightning',
                                         icon_url="https://cdn.discordapp.com/icons/754890606173487154"
                                                  "/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
                        page1.set_image(url='https://crafatar.com/renders/head/' + skin)
                    ################################################################
                    async with cs.get('https://api.pvparca.de//mc/match/latest/' + mc_name, ) as r:
                        res = await r.json()
                        ms3 = res[0]['match']['startedDate']
                        i = 0
                        page2 = discord.Embed(title="", color=0xbc2a82)
                        page2.set_author(name=mc_name + " Latest Match Stats 2/2")
                        page2_embed_fields = [
                            EmbedField(name="<a:redblue:853636359108558898> Winning Team",
                                       value=res[0]["match"]["winningTeam"].capitalize()),
                            EmbedField(name="<a:match:854808917024309328> Match Size", value=res[0]["matchSize"]),
                            EmbedField(name="<:maps:853637839064924170> Map", value=res[0]["loadedMap"]["name"]),
                            EmbedField(name="<a:clock:854800563857784872> Time elapsed", value=res[0]["timeElapsed"]),
                            EmbedField(name="Started",
                                       value=datetime.datetime.fromtimestamp(ms3 / 1000.0).strftime('%m-%d • %H:%M:%S'))
                        ]

                        for field in page2_embed_fields:
                            try:
                                page2.add_field(name=field.name, value=field.value, inline=True)
                            except KeyError:
                                page2.add_field(name=field.name, value="N/A", inline=True)

                        page2.timestamp = datetime.datetime.utcnow()
                        page2.set_footer(text='Bot Created by ksndq and LordofLightning',
                                         icon_url="https://cdn.discordapp.com/icons/754890606173487154"
                                                  "/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
                        page2.set_image(url='https://crafatar.com/renders/head/' + skin)
        else:
            embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
            await ctx.send(embed=embed_var)
            pass

        pages = [page1, page2]
        message = await ctx.send(embed=page1)
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        self.global_variables.messages.append({"message": message, "author": ctx.author, "pages": pages, "page_number": 0})


def setup(client):
    client.add_cog(Stats(client))

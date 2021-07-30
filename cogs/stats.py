import discord
import aiohttp

from ago import human
from datetime import datetime
import datetime

from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from structs.proxy import ProxyConnectorWrapper
from structs.embed import EmbedField
from structs.globals import GlobalVariables


async def process_stats_command(self, ctx, requested_user):
    if ctx.channel.id in self.global_variables.config['bot']['channels']:
        flags = ""
        requested_user_string_length = len(requested_user)
        # If requested_user is in the form of a Warzone/TGM playerID
        if requested_user_string_length == 24:
            flags += "?byID=true"
        # If requested_user is in the form of a Minecraft UUID without dashes
        elif requested_user_string_length == 32:
            requested_user = requested_user[0:8] + "-" \
                             + requested_user[8:12] + "-" \
                             + requested_user[12:16] + "-" \
                             + requested_user[16:20] + "-" \
                             + requested_user[20:32]
            flags += "?byUUID=true"
        # If requested_user is in the form of a Minecraft UUID with dashes
        elif requested_user_string_length == 36:
            flags += "?byUUID=true"
        connector = ProxyConnectorWrapper().connector
        async with aiohttp.ClientSession(connector=connector) as cs:
            async with cs.get('https://api.pvparca.de/mc/player/' + requested_user + flags, ) as r:
                if r.status == 522 or r.status == 502:
                    error_message = "The PVP Arcade Team Games API is currently down, please wait for it to by " \
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
                        title="The user you specified is not in PVP Arcade's Team Games database, "
                              "please check your spelling.",
                        color=0xFF0000)
                    await ctx.send(embed=embed_var)
                    return
                #######
                # Since the API returns nothing when a players stat has not been set, such as when a player has not yet
                # lost a game or died, we need to do a bit of inefficient processing on our data to make sure everything
                # still works
                user_stat_types = ['name', 'uuid', 'lastOnlineDate', 'initialJoinDate', 'wins', 'losses', 'kills',
                                   'deaths', 'level', 'wool_destroys']
                for stat_type in user_stat_types:
                    if stat_type is None:
                        if stat_type == "losses" or stat_type == "deaths":
                            res['user'][stat_type] = 0
                        else:
                            res['user'][stat_type] = "N\A"

                mc_name = res['user']['name']
                skin = res['user']['uuid']
                ms = res['user']['lastOnlineDate']
                ms2 = res['user']['initialJoinDate']
                win = res['user']['wins']
                lost = res['user']['losses']
                wl = win / lost if lost != 0 else win
                k = res['user']['kills']
                d = res['user']['deaths']
                kd = k / d if d != 0 else k
                level = res['user']['level']
                wool_destroys = res['user']['wool_destroys']
                matches = res['user']['matches']

                #######
                page1 = discord.Embed(title="", color=0xbc2a82)
                page1.set_author(name=mc_name + " Stats on the Team Games Mode of The PVP Arcade Network 1/2")
                page1_embed_fields = [
                    EmbedField(name="<a:played:853633469014605824> Matches played",
                               value=matches),
                    EmbedField(name="<a:kills:853628582731186177> Kills", value=k),
                    EmbedField(name="<a:deaths:855109742288437250> Deaths", value=d),
                    EmbedField(name="<a:kd:855110404735893515> K/D", value="{:.2f}".format(kd)),
                    EmbedField(name="<a:level:853628581188337666> Level", value=level),
                    EmbedField(name="<a:wins:853628581698600961> Wins", value=win),
                    EmbedField(name="<:loses:853633469070835712> Losses", value=lost),
                    EmbedField(name="<a:wl:855110803082313728> W/L", value="{:.2f}".format(wl)),
                    EmbedField(name="<a:wool:853628583535968286> Wool Destroys",
                               value=wool_destroys),
                    EmbedField(name="Last Online", value=human(ms / 1000.0)),
                    EmbedField(name="Join Date", value=human(ms2 / 1000.0))]

                for field in page1_embed_fields:
                    try:
                        page1.add_field(name=field.name, value=field.value, inline=True)
                    except KeyError:
                        page1.add_field(name=field.name, value="N/A", inline=True)

                page1.timestamp = datetime.datetime.utcnow()
                page1.set_footer(text='Bot Created by ksndq and LordofLightning',
                                 icon_url="https://cdn.discordapp.com/icons/865108378153517096"
                                          "/aa6a471fa500a396a3e0f419b3acad14.png?size=64")
                page1.set_image(url='https://crafatar.com/renders/head/' + skin)
            ################################################################
            async with cs.get('https://api.pvparca.de/mc/match/latest/' + mc_name, ) as r:
                res = await r.json()
                ms3 = res[0]['match']['startedDate']
                i = 0
                page2 = discord.Embed(title="", color=0xbc2a82)
                page2.set_author(name=mc_name + " Latest Match Stats 2/2")
                page2_embed_fields = [
                    EmbedField(name="<a:redblue:853636359108558898> Winning Team",
                               value=res[0]["match"]["winningTeam"]),
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
                                 icon_url="https://cdn.discordapp.com/icons/865108378153517096"
                                          "/aa6a471fa500a396a3e0f419b3acad14.png?size=64")
                page2.set_image(url='https://crafatar.com/renders/head/' + skin)

                pages = [page1, page2]
                message = await ctx.send(embed=page1)
                await message.add_reaction('◀')
                await message.add_reaction('▶')
                self.global_variables.messages.append(
                    {"message": message, "author": ctx.author, "pages": pages, "page_number": 0})
    else:
        embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
        await ctx.send(embed=embed_var, delete_after=5.0)


class Stats(commands.Cog):
    global_variables = GlobalVariables()
    guild_ids = global_variables.config['bot']['guilds']

    def __init__(self, client):
        pass

    @commands.command(aliases=['stat'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx: commands.context, requested_user: str = None):
        async with ctx.typing():
            if requested_user is None:
                embed_var = discord.Embed(title="You must specify a user to check the stats of.", color=0xFF0000)
                await ctx.send(embed=embed_var)
                return
            await process_stats_command(self, ctx, requested_user)

    ########################################################
    options = [
        {
            "name": "requested_user",
            "description": "Your Minecraft name",
            "required": True,
            "type": 3
        }
    ]

    @cog_ext.cog_slash(name='Stats', description='Displays player stats on team games',
                       guild_ids=guild_ids, options=options)
    async def _stats(self, ctx: SlashContext, requested_user: str):
        await ctx.defer()
        await process_stats_command(self, ctx, requested_user)


def setup(client):
    client.add_cog(Stats(client))

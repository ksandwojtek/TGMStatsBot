#!python
import discord
import os
import aiohttp
import json
import argparse
from ago import human
from datetime import datetime
import datetime
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, context

from customobjects import EmbedField
from globalvariables import GlobalVariables

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs an instance of the Cylone Stat Bot")
    parser.add_argument("-t", "--token", nargs="?", type=str, help="Discord bot token")
    parser.add_argument("-c", "--channel", nargs="?", type=int, help="Channel ID where the Discord Bot will respond "
                                                                     "to queries")
    parser.add_argument("-g", "--guild", nargs="?", type=int, help="ID of the Guild/Server that the bot is in.")
    args = parser.parse_args()

    with open("./config.json", mode="r") as fl:

        config = json.loads(fl.read())

    if args.token is not None:
        config["bot"]["token"] = args.token
    if args.channel is not None:
        config["bot"]["channel"] = args.channel
    if args.guild is not None:
        config['bot']['guild'] = [args.guild]

    global_variables = GlobalVariables()
    global_variables.set_config(config)

    intents = discord.Intents.all()
    client = commands.Bot(command_prefix=config["bot"]["prefix"], intents=intents, case_insensitive=True)

    slash = SlashCommand(client, sync_commands=True)

    client.remove_command('help')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')
        else:
            print(f'Unable to load {filename[:-3]}')

        @client.event
        async def on_ready():
            await client.change_presence(activity=discord.Game(name="CyloneMC.net"))
            print(f'{client.user} has connected to Discord!')


        guild_ids = global_variables.config['bot']['guild']
        ########################################################
        options = [
            {
                "name": "requested_user",
                "description": "Your Minecraft name",
                "required": True,
                "type": 3
            }
        ]


    @slash.slash(name='Stats', description='Displays player stats on team games', guild_ids=guild_ids,
                 options=options)
    async def stats(ctx: SlashContext, requested_user: str, name=' '):
        if ctx.channel.id == global_variables.config['bot']['channel']:
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
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://tgmapi.cylonemc.net/mc/player/' + requested_user + flags, ) as r:
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
                        EmbedField(name="<a:played:853633469014605824> Matches played", value=res['user']['matches']),
                        EmbedField(name="<a:kills:853628582731186177> Kills", value=res['user']['kills']),
                        EmbedField(name="<a:deaths:855109742288437250> Deaths", value=res['user']['deaths']),
                        EmbedField(name="<a:kd:855110404735893515> K/D", value="{:.2f}".format(k / d)),
                        EmbedField(name="<a:level:853628581188337666> Level", value=res['user']['level']),
                        EmbedField(name="<a:wins:853628581698600961> Wins", value=res['user']['wins']),
                        EmbedField(name="<:loses:853633469070835712> Losses", value=res['user']['losses']),
                        EmbedField(name="<a:wl:855110803082313728> W/L", value="{:.2f}".format(win / lost)),
                        EmbedField(name="<a:wool:853628583535968286> Wool Destroys", value=res['user']['wool_destroys']),
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
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://tgmapi.cylonemc.net/mc/match/latest/' + mc_name, ) as r:
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
                if i < 1:
                    i += 1
                    await message.edit(embed=pages[i])
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=45.0, check=check)
                await message.remove_reaction(reaction, user)
            except Exception as e:
                print(e)
                break
        await message.clear_reactions()


    ##############################################
    @slash.slash(name='Help', description='Displays the help menu and credits', guild_ids=guild_ids)
    async def help(ctx: SlashContext):
        if ctx.channel.id == global_variables.config['bot']['channel']:
            page1 = discord.Embed(title="", color=0xbc2a82)
            page1.set_author(name="Cylone Stats Bot Help Menu 1/2")
            page1.add_field(name="Stats", value="Displays latest game and player stats on team games", 
                            inline=False)
            page1.add_field(name="Lb/Leaderboard", value="Displays various team games leaderboards.",
                            inline=False)

            page1.timestamp = datetime.datetime.utcnow()
            page1.set_footer(text='Bot Created by ksndq and LordofLightning',
                             icon_url="https://cdn.discordapp.com/icons/754890606173487154/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
            ################################################################
            page2 = discord.Embed(title="", color=0xbc2a82)
            page2.set_author(name="Credit List 2/2")
            page2.add_field(name="Main Developer", value="<@431703739913732097> <:ksndq:856587427283337236>",
                            inline=False)
            page2.add_field(name="Co-Developer",
                            value="<@336363923542376449> <:LordofLightning:856587426985934910>",
                            inline=False)
            page2.add_field(name="Tester", value="<@491621008856449044> <:THAWERZ:856589646909669427>",
                            inline=False)
            page2.set_footer(text='Bot Created by ksndq and LordofLightning',
                             icon_url="https://cdn.discordapp.com/icons/754890606173487154"
                                      "/a_d0357357c6115502b46b996be1fb32d6.webp?size=64")
        else:
            embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
            await ctx.send(embed=embed_var)
            pass

        pages = [page1, page2]
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
                if i < 1:
                    i += 1
                    await message.edit(embed=pages[i])
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=45.0, check=check)
                await message.remove_reaction(reaction, user)
            except Exception as e:
                print(e)
                break
        await message.clear_reactions()                  

    ##############################################
    @slash.slash(name='Leaderboard', description='Displays team games leaderboards', guild_ids=guild_ids)
    async def help(ctx: SlashContext):
        if ctx.channel.id == global_variables.config['bot']['channel']:
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
                reaction, user = await client.wait_for('reaction_add', timeout=45.0, check=check)
                await message.remove_reaction(reaction, user)
            except Exception as e:
                print(e)
                break
        await message.clear_reactions()                                                                                   

    client.run(config["bot"]["token"], reconnect=True)

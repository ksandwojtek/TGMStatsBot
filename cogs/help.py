import discord

from datetime import datetime
import datetime
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from globalvariables import GlobalVariables


async def process_help_command(self, ctx):
    if ctx.channel.id in self.global_variables.config['bot']['channels']:
        page1 = discord.Embed(title="", color=0xbc2a82)
        page1.set_author(name="Bot Help Menu 1/2")
        page1.add_field(name="Stats", value="Displays latest game and player stats on team games.",
                        inline=False)
        page1.add_field(name="Lb/Leaderboard", value="Displays various team games leaderboards.", inline=False)

        page1.timestamp = datetime.datetime.utcnow()
        page1.set_footer(text='Bot Created by ksndq and LordofLightning',
                         icon_url="https://cdn.discordapp.com/icons/865108378153517096"
                                  "/aa6a471fa500a396a3e0f419b3acad14.png?size=64")

        ################################################################

        page2 = discord.Embed(title="", color=0xbc2a82)
        page2.set_author(name="Credit List 2/2")
        page2.add_field(name="Developers", value="<@431703739913732097> <:ksndq:856587427283337236> and "
                                                 "<@336363923542376449> <:LordofLightning:856587426985934910>",
                        inline=False)
        page2.add_field(name="Tester", value="<@491621008856449044> <:THAWERZ:856589646909669427>",
                        inline=False)
        page2.set_footer(text='Bot Created by ksndq and LordofLightning',
                         icon_url="https://cdn.discordapp.com/icons/865108378153517096"
                                  "/aa6a471fa500a396a3e0f419b3acad14.png?size=64")
    else:
        embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
        await ctx.send(embed=embed_var)
        pass

    pages = [page1, page2]
    message = await ctx.send(embed=page1)
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    self.global_variables.messages.append({"message": message, "author": ctx.author, "pages": pages, "page_number": 0})


class Help(commands.Cog):
    global_variables = GlobalVariables()
    guild_ids = global_variables.config['bot']['guilds']

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['halp'])
    async def help(self, ctx: commands.context):
        await process_help_command(self, ctx)

    @cog_ext.cog_slash(name='Help', description='Displays the help menu and credits', guild_ids=guild_ids)
    async def _help(self, ctx: SlashContext):
        await process_help_command(self, ctx)

def setup(client):
    client.add_cog(Help(client))

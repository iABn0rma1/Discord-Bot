import discord
import discordlists
import datetime
import asyncio
import btime
import humanize
import default
import aiohttp
from paginator import Pages
from discord import Webhook, AsyncWebhookAdapter
from discord.utils import escape_markdown, find
from discord.ext import commands, tasks

class owner(commands.Cog, name="owner"):

    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "<:owner:784461000463089714>"
        self.big_icon = "https://cdn.discordapp.com/emojis/784461000463089714.png?v=1"
        self._last_result = None
        self.api = discordlists.Client(self.bot)  # Create a Client instance
        self.api.start_loop()
        self.color = discord.Colour.from_rgb(250,0,0)

    async def cog_check(self, ctx: commands.Context):
        """> Local check, makes all commands in this cog owner-only"""
        if not await ctx.bot.is_owner(ctx.author):

            if ctx.guild.id == 707176269321732146:
                try:
                    pass
                except:
                    pass
            return False
        return True

    @commands.command(hidden=True)
    @commands.is_owner()
    async def o_dm(self, ctx, user: discord.User, *, msg=None):
        """> DM a user"""
        if user != None and msg != None:
            try:
                msg = msg or "This Message is sent via DM"
                await user.send(msg)
                await ctx.send(f"`{msg}` sent to {user.name}: {ctx.author.name}")
            except:
                await ctx.channel.send("Couldn't dm the given user.")
        else:
            await ctx.channel.send("You didn't provide a user's id and/or a message.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def userlist(self, ctx):
        """> Whole list of users that bot can see"""
        try:
            await ctx.message.delete()
        except:
            pass
        async with ctx.channel.typing():
            await asyncio.sleep(2)
        user_list = []
        for user in self.bot.users:
            user_list.append(user)

        user_lists = []  # Let's list the users
        for num, user in enumerate(user_list, start=0):
            user_lists.append(
                f'`[{num + 1}]` **{user.name}** ({user.id})\
                \n**Created at:** {btime.human_timedelta(user.created_at)}\n**────────────────────────**\n')

        paginator = Pages(ctx,
                          title=f"__Users:__ `[{len(user_lists)}]`",
                          entries=user_lists,
                          per_page=10,
                          embed_color=discord.Colour.from_rgb(250,0,0),
                          show_entry_count=False,
                          author=ctx.author)

        await paginator.paginate()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def getguild(self, ctx):
        """> Returning error: list has no attribute channel"""
        lst_guild = list(self.bot.guilds)
        lst_chnnl = self.bot.guilds.TextChannel[0]
        id = ctx.message.guild.id
        await ctx.send(lst_guild, lst_chnnl)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def announce(self, ctx, *, message: str):
        """> Announce something in support server announcement channel
        > (from user as a bot)"""

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discordapp.com/api/webhooks/784485842772557844/qsku3xQN5voiTes-tyeHoQNgR_cttOj1gnhKUcrrwtbYX_-Ko2gGKeXkrNd7i31uZklq'
                                       , adapter=AsyncWebhookAdapter(session))
            await webhook.send(message, username=ctx.author.name, avatar_url=ctx.author.avatar_url)

        await ctx.message.add_reaction(f'<:check:784187150660665384>')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def join(self, ctx):
        """> Summons the bot to your voice channel"""
        await ctx.author.voice.channel.connect() #Joins author's voice channel

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx):
        """> Disconnect the bot from the voice channel"""
        await ctx.voice_client.disconnect()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invite(self, ctx):
        """> Invite bot to your server"""
        embed = discord.Embed(colour=discord.Colour.from_rgb(250, 0, 0),
                              description=f"<:DarkNemesis:770563343974400010> You can invite me by clicking \
                              [here](https://discord.com/api/oauth2/authorize?client_id=785775388286517249&permissions=8&scope=bot)")
        await ctx.send(embed=embed)

    @commands.group(hidden=True)
    @commands.is_owner()
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @change.command(name="username", hidden=True)
    @commands.is_owner()
    async def change_username(self, ctx, *, name: str):
        """> Change username. """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)

    @change.command(name="nickname", hidden=True)
    @commands.is_owner()
    async def change_nickname(self, ctx, *, name: str = None):
        """> Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"Successfully changed nickname to **{name}**")
            else:
                await ctx.send("Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)

def setup(bot):
    bot.add_cog(owner(bot))

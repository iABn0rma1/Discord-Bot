import discord
import datetime
import asyncio
import default
from publicflags import UserFlags
from paginator import Pages
from discord.utils import escape_markdown
from collections import Counter
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = commands.when_mentioned_or('?'), intents=discord.Intents.all(),
                      description="A very nice general bot for memes, music and moderation and also for other stuffs, coded in python3.7 with ❤ by AB01®#2951",
                      pm_help=True,
                      case_insensitive=True, activity=discord.Game(name="Starting the bot...."),
                      status=discord.Status("dnd")
                      )

client._uptime = None

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.command(aliases=["botinfo"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def about(self, ctx):
        """> Displays basic information about the bot """

        version = '01.10'

        channel_types = Counter(type(c) for c in self.bot.get_all_channels())
        voice = channel_types[discord.channel.VoiceChannel]
        text = channel_types[discord.channel.TextChannel]

        te = len([c for c in set(self.bot.walk_commands()) if c.cog_name == "Owner"])
        se = len([c for c in set(self.bot.walk_commands()) if c.cog_name == "Staff"])
        xd = len([c for c in set(self.bot.walk_commands())])
        ts = se + te
        totcmd = xd - ts

        mems = len(self.bot.users)

        AB01 = self.bot.get_user(684644222615158834)

        embed = discord.Embed(colour = discord.Colour.from_rgb(250, 0, 0))
        embed.description = f"""
    __**General Information:**__
    **Developer:** [{escape_markdown(str(AB01), as_needed=True)}](https://www.instagram.com/__i.ab01__/?hl=en)\
    \n**Bot version:** {version}\n**Created on:** {default.date(self.bot.user.created_at)}\
     ({default.timeago(datetime.datetime.now() - self.bot.user.created_at)})
    
    __**Other Information:**__
    **Total:**\nCommands: **{totcmd:,}**\nMembers: **{mems:,}**\
    \nChannels: <:TextChannel:783009153076559903> **{text:,}** | <:VoiceChannel:783009153215496242> **{voice:,}**\n
    """
        embed.set_thumbnail(url=f"{AB01.avatar_url}")
        embed.set_footer(text= f'Made with Discord.py {discord.__version__}',
                         icon_url='https://images-ext-1.discordapp.net/external/h2NyqrWmotzW-h7JoyZqQ7dEGoXIQeZ4eqlHimj1pLk/https/i.imgur.com/6pg6Xv4.png')
        await ctx.send(embed=embed)

    @client.command(aliases=["si", 'server'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """> Overview about the information of a server"""
        description = ctx.guild.description
        icon = ctx.guild.icon_url

        if ctx.guild.mfa_level == 0:
            mfa = "Disabled"
        else:
            mfa = "Enabled"

        embed = discord.Embed(
            title=f"Server Information",
            description=description,
            colour=discord.Colour.from_rgb(250, 0, 0)
        )
        embed.set_thumbnail(url=icon)

        unique_members = set(ctx.guild.members)
        unique_online = sum(1 for m in unique_members if
                            m.status is discord.Status.online and not type(m.activity) == discord.Streaming)
        unique_offline = sum(1 for m in unique_members if
                             m.status is discord.Status.offline and not type(m.activity) == discord.Streaming)
        unique_idle = sum(
            1 for m in unique_members if m.status is discord.Status.idle and not type(m.activity) == discord.Streaming)
        unique_dnd = sum(
            1 for m in unique_members if m.status is discord.Status.dnd and not type(m.activity) == discord.Streaming)
        unique_streaming = sum(1 for m in unique_members if type(m.activity) == discord.Streaming)
        humann = sum(1 for member in ctx.guild.members if not member.bot)
        botts = sum(1 for member in ctx.guild.members if member.bot)

        tot_mem = 0
        for member in ctx.guild.members:
            tot_mem += 1

        nitromsg = f"This server has **{ctx.guild.premium_subscription_count}** boosts"
        nitromsg += "\n{0}".format(default.next_level(ctx))

        embed.add_field(name="__**General Information**__",
                        value=f"**Guild name:** {ctx.guild.name}\n**Guild ID:** {ctx.guild.id}\
                        \n**Guild Owner:** {ctx.guild.owner}\n**Guild Owner ID:** {ctx.guild.owner.id}\
                        \n**Created at:** {ctx.guild.created_at.__format__('%A %d %B %Y, %H:%M')}\
                        \n**Region:** {str(ctx.guild.region).title()}\n**MFA:** {mfa}\
                        \n**Verification level:** {str(ctx.guild.verification_level).capitalize()}",
                        inline=True)
        embed.add_field(name="__**Other**__",
                        value=f"**Members:**\n<:online:783012763638824992> **{unique_online:,}**\
                        \n<:idle:783012763861516339> **{unique_idle:,}**\
                        \n<:dnd:783012763932819496> **{unique_dnd:,}**\
                        \n<:stream:783012763617591400> **{unique_streaming:,}**\
                        \n<:offline:783012764180152391> **{unique_offline:,}**\
                        \n**Total:** {tot_mem:,} ({humann:,} Humans/{botts:,} Bots)\
                        \n**Channels:** <:TextChannel:783009153076559903> {len(ctx.guild.text_channels)}/<:VoiceChannel:783009153215496242> \
{len(ctx.guild.voice_channels)}\n**Roles:** {len(ctx.guild.roles)}",
                        inline=True)
        embed.add_field(name='__**Server boost status**__',
                        value=nitromsg, inline=False)
        embed.set_image(url=ctx.guild.banner_url)

        await ctx.send(embed=embed)

    @client.command(name="userinfo", aliases=['ui', 'whois'])
    async def userinfo(self, ctx, user: discord.Member = None):
        """> Overview about the information of an user"""
        user = user or ctx.author

        badges = {
            'hs_brilliance': f'<:brilliance:782237533937336340>',
            'discord_employee': f'<:staff:784160633674793021>',
            'discord_partner': f'<:partner:784160633548963861>',
            'hs_events': f'<:events:784162225446191105>',
            'bug_hunter_lvl1': f'<:bughunter:784160633728925760>',
            'hs_bravery': f'<:bravery:782238095093399563>',
            'hs_balance': f'<:balance:782238156141494282>',
            'early_supporter': f'<:supporter:784160633826181140>',
            'bug_hunter_lvl2': f'<:bughunter:784160633728925760>',
            'verified_dev': f'<:verified:784160633527730186>'
        }

        badge_list = []
        flag_vals = UserFlags((await self.bot.http.get_user(user.id))['public_flags'])
        for i in badges.keys():
            if i in [*flag_vals]:
                badge_list.append(badges[i])

        if user.bot:
            bot = "Yes"
        elif not user.bot:
            bot = "No"

        if badge_list:
            discord_badges = ' '.join(badge_list)
        elif not badge_list:
            discord_badges = ''

        usercheck = ctx.guild.get_member(user.id)
        if usercheck:

            if usercheck.nick is None:
                nick = "N/A"
            else:
                nick = usercheck.nick

            status = {
                "online": f"{f'<:online_mob:784158326333112382>' if usercheck.is_on_mobile() else f'<:online:783012763638824992>'}",
                "idle": f"{f'<:idle_mob:784158326824501338>' if usercheck.is_on_mobile() else f'<:idle:783012763861516339>'}",
                "dnd": f"{f'<:dnd_mob:784158326727639070>' if usercheck.is_on_mobile() else f'<:dnd:783012763932819496>'}",
                "offline": f"<:offline:783012764180152391>"
            }

            if usercheck.activities:
                ustatus = ""
                for activity in usercheck.activities:
                    if activity.type == discord.ActivityType.streaming:
                        ustatus += f"<:stream:783012763617591400>"
            else:
                ustatus = f'{status[str(usercheck.status)]}'

            if not ustatus:
                ustatus = f'{status[str(usercheck.status)]}'

            uroles = []
            for role in usercheck.roles:
                if role.is_default():
                    continue
                uroles.append(role.mention)

            uroles.reverse()

            profile = discord.Profile

            emb = discord.Embed(color=ctx.author.colour)
            emb.set_author(icon_url=user.avatar_url, name=f"{user.name}'s information")
            emb.add_field(name="__**Personal Info:**__",
                          value=f"**Full name:** {user} {discord_badges}\n**User ID:** {user.id}\
                          \n**Account created:** {user.created_at.__format__('%A %d %B %Y, %H:%M')}\
                          \n**Bot:** {bot}\n**Avatar URL:** [Click here]({user.avatar_url})",
                          inline=False)
            emb.add_field(name="__**Activity Status:**__",
                          value=f"**Status:** {ustatus}\n**Activity status:** {default.member_activity(usercheck)}",
                          inline=False)
            emb.add_field(name="__**Server Info:**__",
                          value=f"**Nickname:** {user.nick}\n**Joined at:** {default.date(usercheck.joined_at)}\
                          \n**Roles: ({len(usercheck.roles) - 1}) **" + ", ".join(
                              uroles), inline=True)
            if user.is_avatar_animated() == False:
                emb.set_thumbnail(url=user.avatar_url_as(format='png'))
            elif user.is_avatar_animated() == True:
                emb.set_thumbnail(url=user.avatar_url_as(format='gif'))
            else:
                emb.set_thumbnail(url=user.avatar_url)

            await ctx.send(embed=emb)

    @commands.command(name="Tinfo", hidden=True)
    @commands.guild_only()
    async def tinfo(self, ctx):
        """> Overview about the information of an ticket"""
        embed = discord.Embed(title="Info",
                              description=f"I heard you needed some info! React with <:RS_bin:781641561867812905> to remove this embed.",
                              color=discord.Colour.from_rgb(250,0,0))
        embed.add_field(name=f"Data stored:", value="None!", inline=False)
        embed.add_field(name=f"Fact:", value="All embeds I send are removeable via a reaction!", inline=False)
        embed.add_field(name=f"Required permissions:",
                        value="Send messages, Manage channels, Read messages, Add reactions\nIf I am missing one of these permissions, I will throw a 503 error",
                        inline=False)
        embed.add_field(name=f"Other causes of 503 error:",
                        value="503 is quite a common error, if you wish to report one, head over to my support server!",
                        inline=False)
        message1 = await ctx.send(embed=embed)
        await message1.add_reaction('<:RS_bin:781641561867812905')

        def check1(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "<:RS_bin:781641561867812905>"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check1)
        except asyncio.TimeoutError:
            return
        else:
            await message1.delete()

    @commands.command(aliases=['guildstaff'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def serverstaff(self, ctx):
        """> Check which server staff are online in the server"""
        message = ""
        online, idle, dnd, offline = [], [], [], []

        for user in ctx.guild.members:
            if ctx.channel.permissions_for(user).kick_members or \
                    ctx.channel.permissions_for(user).ban_members:
                if not user.bot and user.status is discord.Status.online:
                    online.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.idle:
                    idle.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.dnd:
                    dnd.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.offline:
                    offline.append(f"**{user}**")

        if online:
            message += f"<:online:783012763638824992> {', '.join(online)}\n"
        if idle:
            message += f"<:idle:783012763861516339> {', '.join(idle)}\n"
        if dnd:
            message += f"<:dnd:783012763932819496> {', '.join(dnd)}\n"
        if offline:
            message += f"<:offline:783012764180152391> {', '.join(offline)}\n"

        e = discord.Embed(color=discord.Colour.from_rgb(250,0,0), title=f"{ctx.guild.name} mods",
                          description="This lists everyone who can ban and/or kick.")
        e.add_field(name="Server Staff List:", value=message)

        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def roles(self, ctx):
        """> List of all the roles in the server """
        allroles = []

        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            if role.is_default():
                continue
            allroles.append(
                f"`[{str(num).zfill(2)}]` {role.mention} | {role.id} | **[ Users : {len(role.members)} ]**\n")

        if len(allroles) == 0:
            return await ctx.send(f"<:xmark:784187150542569503> Server has no roles")

        # data = BytesIO(allroles.encode('utf-8'))
        paginator = Pages(ctx,
                          title=f"{ctx.guild.name} roles list",
                          entries=allroles,
                          thumbnail=None,
                          per_page=15,
                          embed_color=discord.Colour.from_rgb(250,0,0),
                          show_entry_count=True,
                          author=ctx.author)
        await paginator.paginate()

    @commands.command(aliases=['se', 'emotes'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def serveremotes(self, ctx):
        """> Get a list of all the emotes in the server"""

        _all = []
        for num, e in enumerate(ctx.guild.emojis, start=0):
            _all.append(f"`[{num + 1}]` {e} **{e.name}** | {e.id}\n")

        if len(_all) == 0:
            return await ctx.send(f"<:xmark:784187150542569503> Server has no emotes!")

        paginator = Pages(ctx,
                          title=f"{ctx.guild.name} emotes list",
                          entries=_all,
                          thumbnail=None,
                          per_page=15,
                          embed_color=discord.Colour.from_rgb(250,0,0),
                          show_entry_count=True,
                          author=ctx.author)
        await paginator.paginate()

    @commands.command(aliases=['perms'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def permissions(self, ctx, member: discord.Member = None):
        """> See what permissions member has in the server"""

        member = member or ctx.author

        sperms = dict(member.guild_permissions)

        perm = []
        for p in sperms.keys():
            if sperms[p] == True and member.guild_permissions.administrator == False:
                perm.append(f"<:check:784187150660665384> {p}\n")
            if sperms[p] == False and member.guild_permissions.administrator == False:
                perm.append(f"<:xmark:784187150542569503> {p}\n")

        if member.guild_permissions.administrator == True:
            perm = [f'<:check:784187150660665384> Administrator']

        paginator = Pages(ctx,
                          title=f"{member.name} guild permissions",
                          entries=perm,
                          thumbnail=None,
                          per_page=20,
                          embed_color=discord.Colour.from_rgb(250, 0, 0),
                          show_entry_count=False,
                          author=ctx.author)
        await paginator.paginate()

def setup(bot):
    bot.add_cog(Information(bot))
import discord
import os
import json
import traceback
import asyncio
import random
from discord.ext import commands, tasks
from discord.utils import escape_markdown, sleep_until
import default, btime
from default import timeago
from datetime import datetime
from default import color_picker
from caches import CacheManager as cm


class Events(commands.Cog, name="Events", command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.color = color_picker('colors')

    async def bot_check(self, ctx):
        moks = self.bot.get_user(345457928972533773)
        if ctx.author == moks:
            return True

        data = cm.get_cache(self.bot, ctx.author.id, 'blacklisted_users')
        if data:
            return False
        return True

    async def gain_early(self, member):
        with open('db/badges.json', 'r') as f:
            data = json.load(f)
        try:
            if f'<:supporter:784160633826181140>' not in data['Users'][f'{member.id}']['Badges']:
                data['Users'][f"{member.id}"]['Badges'] += f'<:supporter:784160633826181140>'
                self.bot.user_badges[f"{member.id}"]["Badges"] += f'<:supporter:784160633826181140>'
            else:
                return
        except KeyError:
            data['Users'][f"{member.id}"] = {"Badges": f'<:supporter:784160633826181140>'}
            self.bot.user_badges[f"{member.id}"] = {"Badges": f'<:supporter:784160633826181140>'}

        await member.add_roles(discord.Object(679642623107137549))

        with open('db/badges.json', 'w') as f:
            data = json.dump(data, f, indent=4)

    '''@commands.Cog.listener()
    async def on_ready(self):
        m = "Logged in as:"
        m += "\nName: {0} ({0.id})".format(self.bot.user)
        m += f"\nTime taken to boot: {btime.human_timedelta(self.bot.uptime, suffix=None)}"
        print(m)
        # await self.temp_mutes()
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name="-help")
        )
        for g in self.bot.blacklisted_guilds:
            d = self.bot.get_guild(g)
            try:
                await d.leave()
                print(f"[BLACKLIST ACTION] Left blacklisted guild ({d.id})")
            except:
                pass
        # await self.bot.change_presence(status='idle', activity=discord.Activity(type=discord.ActivityType.playing, name=f"Dredd's rewrite"))'''

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        # Check if guild is blacklisted before continuing
        reason = await self.bot.db.fetchval("SELECT reason FROM blockedguilds WHERE guild_id = $1", guild.id)
        support = self.bot.support

        # If it is blacklisted, log it.
        data = cm.get_cache(self.bot, guild.id, 'blacklisted_guilds')
        if data:
            try:
                to_send = sorted([chan for chan in guild.channels if chan.permissions_for(
                    guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
            except IndexError:
                pass
            else:
                reason = ''.join(data)
                e = discord.Embed(color=self.color['deny_color'],
                                  description=f"Hello!\nThis server has been blacklisted for: **{reason}**\n\nThus why I'll be leaving this server.\nIf you wish to appeal feel free to join the [support server]({self.bot.support})\nOnly server owner can appeal, unless their account is terminated.",
                                  timestamp=datetime.utcnow())
                e.set_author(name=f"Blacklist issue occured!", icon_url=self.bot.user.avatar_url)
                e.set_thumbnail(
                    url='https://media.discordapp.net/attachments/756847192945459201/783075230922702848/Comp_1.gif?width=461&height=461')
                try:
                    await to_send.send(embed=e)
                except:
                    pass
                await guild.leave()

            # Send it to the log channel
            chan = self.bot.get_channel(783793077918629939)
            modid = await self.bot.db.fetchval("SELECT dev FROM blockedguilds WHERE guild_id = $1", guild.id)
            mod = 684644222615158834
            e = discord.Embed(color=discord.Colour.from_rgb(250,0,0), title=f":black_circle: Attempted Invite",
                              timestamp=datetime.utcnow(),
                              description=f"A blacklisted guild attempted to invite me.\
                              \n**Guild name:** {guild.name}\n**Guild ID:** {guild.id}\
                              \n**Guild Owner:** {guild.owner}\n**Guild size:** {len(guild.members) - 1}\
                              \n**Blacklisted by:** {mod}\n**Blacklist reason:** {reason}")
            e.set_thumbnail(url=guild.icon_url)
            return await chan.send(embed=e)

        # Guild is not blacklisted!
        # Insert guild's data to the database and cache
        prefix = '?'
        await self.bot.db.execute("INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2)", guild.id, prefix)
        await self.bot.db.execute("INSERT INTO raidmode(guild_id, raidmode, dm) VALUES ($1, $2, $3)", guild.id, False,
                                  True)
        self.bot.prefixes[guild.id] = prefix
        self.bot.raidmode[guild.id] = {'raidmode': False, 'dm': True}

        Zenpa = self.bot.get_user(684644222615158834)
        Moksej = self.bot.get_user(684644222615158834)
        support = self.bot.support
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(
                guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            if to_send.permissions_for(guild.me).embed_links:  # We can embed!
                e = discord.Embed(
                    color=discord.Colour.from_rgb(250,0,0), title="A cool bot has spawned in!")
                e.description = f"Thank you for adding me to this server! If you'll have any questions you can contact `{Moksej}` or `{Zenpa}`. You can also [join support server]({support})\nTo get started, you can use my commands with my prefix: `{prefix}`, and you can also change the prefix by typing `{prefix}prefix [new prefix]`"
                e.set_thumbnail(
                    url='https://media.discordapp.net/attachments/756847192945459201/783075230922702848/Comp_1.gif?width=461&height=461')
                try:
                    await to_send.send(embed=e)
                except:
                    pass
            else:  # We were invited without embed perms...
                msg = f"Thank you for adding me to this server! If you'll have any questions you can contact `{Moksej}` or `{Zenpa}`. You can also join support server: {support}\nTo get started, you can use my commands with my prefix: `{prefix}`, and you can also change the prefix by typing `{prefix}prefix [new prefix]`"
                try:
                    await to_send.send(msg)
                except:
                    pass

        # Log the join
        logchannel = self.bot.get_channel(783793077918629939)

        members = len(guild.members)
        bots = len([x for x in guild.members if x.bot])
        tch = len(guild.text_channels)
        vch = len(guild.voice_channels)
        if len(self.bot.guilds) == 100:
            g100 = f'\n\n<:star_vip:784450777091407923> **This is 100th server!**'
        else:
            g100 = ''

        ratio = f'{int(100 / members * bots)}'

        embed = discord.Embed(color=discord.Colour.from_rgb(250,0,0), title="I've joined a guild",
                              description=f"I've joined a new guild. Informing you for safety reasons{g100}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="__**General Info**__",
                        value=f"**Guild name:** {guild.name}\n**Guild ID:** {guild.id}\n**Guild owner:** {guild.owner}\n**Guild owner ID:** {guild.owner.id}\n**Guild created:** {default.date(guild.created_at)} ({default.timeago(datetime.utcnow() - guild.created_at)})\n**Member count:** {members - 1} (Bots / Users ratio: {ratio}%)\n**Text channels:** {tch}\n**Voice channels:** {vch}",
                        inline=False)
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        # Delete guild data from the database
        # await self.bot.db.execute("DELETE FROM automods WHERE guild_id = $1", guild.id)
        await self.bot.db.execute("DELETE FROM guilds WHERE guild_id = $1", guild.id)
        cm.delete_cache(self.bot, guild.id)

        # Log the leave
        members = len(guild.members)
        logchannel = self.bot.get_channel(783793077918629939)

        e = discord.Embed(color=discord.Colour.from_rgb(250,0,0), title='I\'ve left the guild...',
                          description=f"**Guild name:** {guild.name}\n**Member count:** {members}")
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        # We don't want to listen to bots
        if message.author.bot:
            return

        # We dont want to listen to commands
        try:
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                return
        except:
            return

        if message.guild and message.guild.id == 667065302260908032:
            if message.author.id == 393793344263815180:
                num = random.randint(1, 10)
                if num == 5:
                    await message.channel.send(f"{message.author.mention} simp",
                                               allowed_mentions=discord.AllowedMentions(users=True))

        # Something happened in DM's
        if message.guild is None:
            blacklist = await self.bot.db.fetchval("SELECT * FROM blacklist WHERE user_id = $1", message.author.id)
            dm_blacklist = await self.bot.db.fetchval("SELECT * FROM dm_black WHERE user_id = $1", message.author.id)
            if blacklist:
                return

            if dm_blacklist:
                return

            if message.content.lower().startswith("-"):
                return await message.author.send("You can use my commands in DM with prefix `!`.")

            # They DM'ed the bot
            logchannel = self.bot.get_channel(783793077918629939)
            dmid = ''
            for num in self.bot.dm:
                if self.bot.dm[num] == message.author.id:
                    dmid += f"{num}"

            total_dms = len(self.bot.dm)
            if not dmid:
                self.bot.dm[total_dms + 1] = message.author.id
                dmid = total_dms + 1

            msgembed = discord.Embed(
                description=escape_markdown(message.content, as_needed=False), color=discord.Color.blurple(),
                timestamp=datetime.utcnow())
            msgembed.set_author(name=f"New DM from: {message.author} | #{dmid}", icon_url=message.author.avatar_url)
            # They've sent a image/gif/file
            if message.attachments:
                attachment_url = message.attachments[0].url
                msgembed.set_image(url=attachment_url)
            msgembed.set_footer(text=f"User ID: {message.author.id}")
            await logchannel.send(embed=msgembed)

    @commands.Cog.listener('on_message')
    async def afk_check(self, message):
        if message.guild is None:
            return

        if message.author.bot:
            return

        for user, guild, msg, time in self.bot.afk_users:
            afkmsg = ""
            if message.author.id == user and message.guild.id == guild:
                ctx = await self.bot.get_context(message)
                if ctx.valid:
                    return
                await message.channel.send(
                    f"Welcome back {message.author.mention}! Removing your AFK state. You were AFK for {btime.human_timedelta(time, suffix=None)}.",
                    delete_after=20, allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True))
                self.bot.afk_users.remove((user, guild, msg, time))
                return await self.bot.db.execute("DELETE FROM userafk WHERE user_id = $1 AND guild_id = $2",
                                                 message.author.id, message.guild.id)

            for userids in message.mentions:
                if userids.id == user:
                    usere = message.guild.get_member(userids)
                    afkmsg += f"{usere} is afk:"

            if afkmsg and message.guild.id == guild:
                afkmsg = afkmsg.strip()
                if '\n' in afkmsg:
                    afkmsg = "\n" + afkmsg
                note = msg
                time = time
                afkuser = message.guild.get_member(user)
                try:
                    await message.channel.send(
                        f'{message.author.mention}, **{escape_markdown(afkuser.display_name, as_needed=True)}** went AFK **{btime.human_timedelta(time)}**, but he left you a note: **{escape_markdown(note, as_needed=True)}**',
                        delete_after=30,
                        allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True))
                except discord.HTTPException:
                    try:
                        await message.author.send(
                            f"Yo, **{escape_markdown(afkuser.display_name, as_needed=True)}** went AFK **{btime.human_timedelta(time)}**, but he left you a note: **{escape_markdown(note, as_needed=True)}**")
                    except discord.Forbidden:
                        return

    @commands.Cog.listener('on_message')
    async def lmao_count(self, message):

        ice = self.bot.get_user(302604426781261824)
        if "lmao" in message.content.lower():
            if not message.author == ice:
                return
            await self.bot.db.execute('UPDATE lmaocount SET count = count + 1 WHERE user_id = $1', message.author.id)

        if "lmfao" in message.content.lower():
            if not message.author == ice:
                return
            await self.bot.db.execute('UPDATE lmaocount SET lf = lf + 1 WHERE user_id = $1', message.author.id)

    @commands.Cog.listener('on_message')
    async def del_staff_ping(self, message):
        moksej = self.bot.get_user(684644222615158834)
        if message.channel.id == 783793077918629939 and message.author.id == 709050474627596340:
            if "added bot" in message.content.lower():
                await moksej.send(f"New bot added {message.jump_url}")
            if "resubmitted bot" in message.content.lower():
                await moksej.send(f"Bot resubmitted {message.jump_url}")

    @commands.Cog.listener('on_member_update')
    async def nicknames_logging(self, before, after):
        if before.bot:
            return
        nicks_opout = await self.bot.db.fetchval("SELECT user_id FROM nicks_op_out WHERE user_id = $1", before.id)

        if before.nick != after.nick and nicks_opout is None:
            if before.nick is None:
                nick = before.name
            elif before.nick:
                nick = before.nick
            await self.bot.db.execute(
                "INSERT INTO nicknames(user_id, guild_id, nickname, time) VALUES ($1, $2, $3, $4)", before.id,
                before.guild.id, nick, datetime.utcnow())

    @commands.Cog.listener('on_member_join')
    async def raid_check(self, member):

        data = cm.get_cache(self.bot, member.guild.id, 'raidmode')
        if data:
            if member.guild.me.guild_permissions.kick_members:
                if data['raidmode'] == True:
                    if data['dm'] == True:
                        try:
                            await member.send(
                                f":warning: I'm sorry but **{member.guild.name}**\
                                 is currently experiencing a raid and have raid-mode enabled. Try joining back later!")
                        except:
                            pass
                        await member.guild.kick(member, reason='Anti-raid protection')
                    elif data['dm'] == False:
                        await member.guild.kick(member, reason='Anti-raid protection')
                elif data['raidmode'] == False:
                    return
        else:
            return

    @commands.Cog.listener('on_member_update')
    async def nitro_booster(self, before, after):
        guild = self.bot.get_guild(719754177940684881)
        nitro_role = guild.get_role(766360938399006752)
        if guild:
            if nitro_role in after.roles:
                check = await self.bot.db.fetchval("SELECT * FROM vip WHERE user_id = $1", after.id)
                if check:
                    return
                with open('db/badges.json', 'r') as f:
                    data = json.load(f)
                badge = f"<:booster:784451508870578226>"
                try:
                    if badge not in data['Users'][f'{after.id}']["Badges"]:
                        data['Users'][f'{after.id}']["Badges"] += [badge]
                except KeyError:
                    data['Users'][f"{after.id}"] = {"Badges": [badge]}

                with open('db/badges.json', 'w') as f:
                    data = json.dump(data, f, indent=4)
                await self.bot.db.execute("INSERT INTO vip(user_id, prefix) VALUES($1, $2)", after.id, '-')
                self.bot.boosters[after.id] = {'custom_prefix': '?'}
            else:
                return
        else:
            return

    @commands.Cog.listener('on_member_join')
    async def badges_sync(self, member):
        if member.guild.id == 783791239903969362:
            if member.bot:
                return
            await self.gain_early(member=member)
        else:
            return


def setup(bot):
    bot.add_cog(Events(bot))

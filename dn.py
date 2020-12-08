import discord
import DiscordUtils
import asyncio
import time
import datetime
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import BucketType

TOKEN = 'Nzg1Nzc1Mzg4Mjg2NTE3MjQ5.X88wWw._HlLTJR2G0B9JSok3lUx6Pbqeu0'

client = commands.Bot(command_prefix=commands.when_mentioned_or('%'), intents=discord.Intents.all(),
                      description="刀ARK么れEMESIS BOT", pm_help=True, owner_id=684644222615158834, case_insensitive=True
                      )
tracker = DiscordUtils.InviteTracker(client)

client._uptime = None

client.remove_command("help")

extensions = [
    "Admin",
    "Fun",
    "Giveaway",
    "Help",
    "Information",
    "Invites",
    "Management",
    "Moderation",
    "Owner",
    "tickets",
]


@client.event
async def on_connect():
    if client._uptime is None:
        print(f"Connected to Discord. Getting ready...")
        print(f'-----------------------------')

@client.event
async def on_ready():
    change_status.start()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------------------------------------')
    client.starttime = time.time()
    print(client.starttime)
    print(f'--------------------------------------')
    print(f'Bot ready!')
    print(f"Successfully logged in as: {client.user.name}")
    print(f"ID: {client.user.id}")
    print(f"Total servers: {len(client.guilds)}")
    print(f"Total Members: {len(client.users)}")
    print(f"Discord.py version: {discord.__version__}")
    print(f'--------------------------------------')
    await tracker.cache_invites()
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(e)

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(name="DM to Contact Staff"), status=discord.Status.idle)
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="%help"),
                                 status=discord.Status.idle)
    await asyncio.sleep(10)

@client.event
async def on_member_join(member):
    inviter = await tracker.fetch_inviter(member)  # inviter is the member who invited
    embed = discord.Embed(color=discord.Color.from_rgb(250, 0, 0),
                          description=f"Welcome to Dark nemesis, where nemesis thrives and the weak die.\
                          \nbe sure to read <#720114750977212476>\nand claim your roles from <#719954850749743157>")
    embed.set_image(
        url='https://media.discordapp.net/attachments/702075277672448021/754948152767021147/20200914_114409.jpg?width=1201&height=586')
    embed.set_author(name=f"Namaste {member.name} ",
                     icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"Inivted by: {inviter} | Total Members: {len(list(member.guild.members))}",
                     icon_url=inviter.avatar_url)

    channel = client.get_channel(id=707239457203552287)

    await channel.send(embed=embed)

@client.event
async def on_message(message):
    """if message.channel.id == 729559048977907803:    #instagram
        await message.add_reaction(f"<:DN_Ok:782953423824879647>")
        await message.add_reaction(f"<:DN_NotOk:782953423824879647>")
        await message.add_reaction(f"<:DN_GetRekt:782953423824879647>")
        await message.add_reaction(f"<:DN_GG:785807194708115478>")
        await message.add_reaction(f"<:DN_Clap:782969142302867496>")
    if message.channel.id == 729558913468334201:    #youtube
        await message.add_reaction(f"<:DN_Ok:782953423824879647>")
        await message.add_reaction(f"<:DN_NotOk:782953423824879647>")
        await message.add_reaction(f"<:DN_GetRekt:782953423824879647>")
        await message.add_reaction(f"<:DN_GG:785807194708115478>")
        await message.add_reaction(f"<:DN_Clap:782969142302867496>")
    if message.channel.id == 720161972703854603:    #images
        await message.add_reaction(f"<:DN_Ok:782953423824879647>")
        await message.add_reaction(f"<:DN_NotOk:782953423824879647>")
        await message.add_reaction(f"<:DN_GetRekt:782953423824879647>")
        await message.add_reaction(f"<:DN_RIP:782953423824879647>")
        await message.add_reaction(f"<:DN_GG:785807194708115478>")
        await message.add_reaction(f"<:DN_WTF:782953423824879647>")
    if message.channel.id == 720161864214118461:    #videos
        await message.add_reaction(f"<:DN_Ok:782953423824879647>")
        await message.add_reaction(f"<:DN_NotOk:782953423824879647>")
        await message.add_reaction(f"<:DN_GG:785807194708115478>")
        await message.add_reaction(f"<:DN_LOL:780000388572250155>")
        await message.add_reaction(f"<:DN_Clap:782969142302867496>")
    if message.channel.id == 720688119254483124:    #memes
        await message.add_reaction(f"<:DN_Ok:780000388572250155>")
        await message.add_reaction(f"<:DN_NotOk:780000388572250155>")
        await message.add_reaction(f"<:DN_LOL:780000388572250155>")
        await message.add_reaction(f"<:DN_LaughingWithGun:780000388572250155>")
        await message.add_reaction(f"<:DN_PepeRevenge:780000388572250155>")"""
    client.channel = client.get_channel(739304042223632408)
    if not client.channel:
        print(f'Channel with ID 739304042223632408 not found.')
        await client.close()
    author = message.author
    if author == client.user:
        return
    if type(message.channel) is discord.DMChannel:
        # for the purpose of nicknames, if anys
        for server in client.guilds:
            member = server.get_member(author.id)
            if member:
                author = member
            break
        embed = discord.Embed(title="Received a DM", description=message.content,
                              colour=discord.Colour.from_rgb(250,0,0))
        if isinstance(author, discord.Member) and author.nick:
            author_name = f'{author.nick} ({author})'
        else:
            author_name = str(author)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=author_name, icon_url=author.avatar_url if author.avatar else author.default_avatar_url)
        to_send = f'{author.mention}'
        if message.attachments:
            attachment_urls = []
            for attachment in message.attachments:
                attachment_urls.append(f'[{attachment.filename}]({attachment.url}) '
                                       f'({attachment.size} bytes)')
            attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} '.join(attachment_urls)
            embed.add_field(name='Attachments', value=attachment_msg, inline=False)
        await client.channel.send(to_send, embed=embed)
        client.last_id = author.id
    await client.process_commands(message)

@client.command(aliases=["latency"])
async def ping(ctx):
    """> See bot's latency to discord"""
    ping = round(client.latency * 1000)
    await ctx.send(f":ping_pong: Pong   |   {ping}ms")

q_list = [
    "What\'s your IGN (In-Game-Name)?",
    "What\'s your UID?",
    "What\'s your age?",
    "Where are you from (Which country)",
    "What device are you playing on?",
    "Have you played for other clan before? If yes, please give a list.",
    "Are you still playing for a clan?",
    "Briefly tell us why would you like to join",
    "How much time do you spend on playing CODM?",
    "Are you available for VC (Voice Chat)",
    "Send your stats (in-link)"
]

a_list = []

@client.command()
@commands.guild_only()
async def apply(ctx, member: discord.Member = None):
    """> Start a new application"""

    member = ctx.author if not member else member

    def checkmsg(m):
        return m.author == member

    def checkreact(reaction, user):
        return user.id == member.id and str(reaction.emoji) in ['✅', '❌']

    try:
        embed_start = discord.Embed(title=f"Application started in dm by {member}",
                               description="The Questions will be sent shortly...",
                               colour=discord.Colour.from_rgb(250,0,0))
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Send your stats")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        if msg.attachments:
            attachment_urls = []
            for attachment in msg.attachments:
                attachment_urls.append(f'[{attachment.filename}]({attachment.url}) '
                                       f'({attachment.size} bytes)')
            msg = '\N{BULLET} ' + '\n\N{BULLET} '.join(attachment_urls)
        try:
            zeroth = msg.content
        except:
            zeroth = msg
        await ctx.send(embed=embed_start)
        async with member.typing():
            await asyncio.sleep(3)
        await member.send("What's your IGN (In-Game-Name)?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        first = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send(
            "What's your UID?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        second = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send(
            "What's your age?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        third = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Where are you from (Which country)")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        fourth = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("What device are you playing on?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        fifth = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Have you played for other clan before? If yes, please give a list.")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        sixth = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Are you still playing for a clan?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        seventh = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Briefly tell us why would you like to join")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        eighth = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("How much time do you spend on playing CODM?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        nineth = msg.content
        async with member.typing():
            await asyncio.sleep(1)
        await member.send("Are you available for VC (Voice Chat)")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        tenth = msg.content


    except asyncio.TimeoutError:
        await member.send("You took too long to write in a response :(")
    else:
        channel = client.get_channel(739304042223632408)
        submit = await member.send("Are you sure you want to submit this application?")
        await submit.add_reaction('✅')
        await submit.add_reaction('❌')
        reaction, user = await client.wait_for("reaction_add", timeout=600.0, check=checkreact)
        if str(reaction.emoji) == '✅':
            async with member.typing():
                await asyncio.sleep(2)
            await member.send('Thank you for applying! Your application will be sent to the Owner soon')
            await asyncio.sleep(2)
            embed = discord.Embed(colour=discord.Colour.from_rgb(250,0,0))

            fields = [(q_list[0], first, False), (q_list[1], second, False), (q_list[2], third, False),
                      (q_list[3], fourth, False), (q_list[4], fifth, False), (q_list[5], sixth, False),
                      (q_list[6], seventh, False), (q_list[7], eighth, False), (q_list[8], nineth, False),
                      (q_list[9], tenth, False), (q_list[10], zeroth, False)]

            embed.add_field(name="User", value=f"{msg.author.mention} | {msg.author.id}", inline=False)

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_author(name=f"Application taken by: {member}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{ctx.guild.name}")
            embed.timestamp = datetime.datetime.utcnow()
            embed_finished = await channel.send(embed=embed)
            await embed_finished.add_reaction('✅')
            await embed_finished.add_reaction('❌')
        else:
            if str(reaction.emoji) == '❌':
                await member.send('Application won\'t be sent')

@client.command(aliases=['idea', 'suggestion'])
@commands.guild_only()
@commands.cooldown(5, 30, type=BucketType.user)
async def suggest(ctx, *, sug):
    """> Leave a suggestion!"""
    await ctx.message.delete()
    try:
        embed = discord.Embed(description=f"Suggestion provided by {ctx.author.mention}\n`{sug}`\
        \n\nReact down below to leave your opinion! ⬇️", colour=discord.Colour.from_rgb(250,0,0))
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        channel = ctx.guild.get_channel(739304042223632408)
        poo = await channel.send(embed=embed)
        await poo.add_reaction("☑")
        await poo.add_reaction("🚫")
    except Exception as error:
        raise(error)

@suggest.error
async def suggestn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        embed = discord.Embed(description='⚠️ You\'re supposed to include the suggestion dummy ⚠️\n```!suggest <suggestion>```',
                              color=ctx.author.colour)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.channel.send(embed=embed, delete_after=5)

client.run(TOKEN)
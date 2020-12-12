import discord
import DiscordUtils
import asyncio
import time
import datetime
from io import BytesIO
from PIL import Image, ImageDraw
from discord.ext import commands, tasks

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
    "Games",
    "Giveaway",
    "Help",
    "Invites",
    "Miscellaneous",
    "Moderation",
    "Owner",
    "tickets",
    "Utility"
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
    welcome = Image.open("welcome.png")
    AVATAR_SIZE = 256

    avatar_asset = member.avatar_url_as(format='png', size=AVATAR_SIZE)

    buffer_avatar = BytesIO(await avatar_asset.read())

    avatar_image = Image.open(buffer_avatar)

    avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))

    circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), outline="green", width=5, fill=255)

    welcome.paste(avatar_image, (460, 45), circle_image)

    welcome.save("wlcm.png")

    inviter = await tracker.fetch_inviter(member)
    embed = discord.Embed(color=discord.Color.from_rgb(250, 0, 0),
                          description=f"<a:DN_Wlcm:720229315723132950> Welcome to Dark nemesis,\
                           where nemesis thrives and the weak die.\
                          \n<a:DN_ThisR:719866047930302464> be sure to read <#720114750977212476>\
                          \n<a:DN_ThisR:719866047930302464> and claim your roles from <#719954850749743157>")
    embed.set_author(name=f"Namaste {member.name} ",
                     icon_url=f"{member.avatar_url}")
    ava = "https://w7.pngwing.com/pngs/609/846/png-transparent-discord-logo-discord-computer-icons-logo-computer-software-avatar-miscellaneous-blue-angle.png"
    embed.set_footer(text=f"Inivted by: {inviter} | Total Members: {len(list(member.guild.members))}")

    channel = client.get_channel(id=719953710192656484)

    file = discord.File("wlcm.png")
    embed.set_image(url="attachment://wlcm.png")
    await channel.send(file=file, embed=embed)

@client.event
async def on_message(message):
    if message.content.startswith(f"<@!{client.user.id}>") or message.content == f"<@!{client.user.id}>":
        await message.channel.send(f"My prefix is `%`")

    if message.channel.id == 729559048977907803:    #instagram
        await message.add_reaction(f"<:DN_Ok:766392304390373386>")
        await message.add_reaction(f"<:DN_NotOk:766392304138715138>")
        await message.add_reaction(f"<:DN_GG:786903401128001596>")
        await message.add_reaction(f"<:DN_Clap:766392302884749363>")
    if message.channel.id == 729558913468334201:    #youtube
        await message.add_reaction(f"<:DN_Ok:766392304390373386>")
        await message.add_reaction(f"<:DN_NotOk:766392304138715138>")
        await message.add_reaction(f"<:DN_GG:786903401128001596>")
        await message.add_reaction(f"<:DN_Clap:766392302884749363>")
    if message.channel.id == 720161972703854603:    #images
        await message.add_reaction(f"<:DN_Ok:766392304390373386>")
        await message.add_reaction(f"<:DN_NotOk:766392304138715138>")
        await message.add_reaction(f"<:DN_GetRekt:766549673556836384>")
        await message.add_reaction(f"<:DN_RIP:766549674076143636>")
        await message.add_reaction(f"<:DN_GG:786903401128001596>")
        await message.add_reaction(f"<:DN_WTF:766549673665495071>")
    if message.channel.id == 720161864214118461:    #videos
        await message.add_reaction(f"<:DN_Ok:766392304390373386>")
        await message.add_reaction(f"<:DN_NotOk:766392304138715138>")
        await message.add_reaction(f"<:DN_GG:786903401128001596>")
        await message.add_reaction(f"<:DN_LOL:780000388572250155>")
        await message.add_reaction(f"<:DN_Clap:766392302884749363>")
    if message.channel.id == 720688119254483124:    #memes
        await message.add_reaction(f"<:DN_Ok:766392304390373386>")
        await message.add_reaction(f"<:DN_NotOk:766392304138715138>")
        await message.add_reaction(f"<:DN_LOL:766549673955033088>")
        await message.add_reaction(f"<:DN_LaughingWithGun:721551289670172672>")
        await message.add_reaction(f"<:DN_PepeRevenge:719868161083834451>")

    client.channel = client.get_channel(720169568965754932)
    if not client.channel:
        print(f'Channel with ID 720169568965754932 not found.')
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
        embed = discord.Embed(title="Mod Mail 📬", description=message.content,
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

client.run(TOKEN)
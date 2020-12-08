import discord
import asyncio
import random
import requests
import pendulum
import aiohttp
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import BadArgument
from discord import Spotify
from lists import *

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.members = True

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """> Share a beer with someone"""
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: fieeeeestaaa!🎉🍺")
        if user.bot == True:
            return await ctx.send(
                f"I would love to give a beer to {user.mention}. But i am unsure they will respond to you!")

        beer_offer = f"**{user.mention}**, You have a 🍺 offered from **{ctx.author.mention}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.mention}** and **{ctx.author.mention}** Are enjoying a lovely 🍻")
            await msg.clear_reactions()
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well it seems **{user.name}** didnt want a beer with **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            beer_offer = f"**{user.name}**, you have a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command()
    async def retard(self, ctx, user: discord.Member = None):
        """> See how retard user is, 100% official score"""
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=ctx.author.colour
        )
        embed.add_field(name='**retard r8 machine**', value=f'{user.display_name} is {random.randint(1,100)}% retarded')
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes'])
    async def joke(self, ctx):
        """> Sends a random joke"""
        embed = discord.Embed(
            title='',
            color=discord.Color.from_rgb(250,0,0)
        )
        embed.add_field(name='**Joke**', value=f'{random.choice(joke)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['murder'])
    async def kill(self, ctx, *, user: discord.Member = None):
        """> Sick of someone? Easy! Just kill them! (we do not endorse murder yet BUT we do in **CODM**)"""
        if user == None or user == 'me':
            user = ctx.author
        else:
            pass
        e = discord.Embed(title="", description="", colour=ctx.author.colour)
        e.add_field(name=f'**How did they die**', value=(f'{user.display_name} was killed by {random.choice(died)}'))
        await ctx.send(embed=e)

    @commands.command()
    async def hack(self, ctx, member: discord.Member = None):
        """> Hack your friends! Or your enemies...
        BTW if you think this is a real hack get your brain checked for smoothness"""
        if not member:
            await ctx.send("Please specify a member")
            return

        fakeips = random.choice(IP_addresses)

        embed = discord.Embed(title=f"**Hacking: {member} now** 0%", color=0x2f3136)
        m = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"19% **Finding IP address**")
        await m.edit(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"34% **IP address: {fakeips}**")
        await m.edit(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"55% **Selling data in Dark Web**")
        await m.edit(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"67% **Reporting account to discord for breaking TOS**")
        await m.edit(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"84% **Hacking login credentials**")
        await m.edit(embed=embed)
        await m.edit(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"**Hacking: {member}**", color=0x2f3136,
                              description=f"100% **The hack is complete!**")
        await m.edit(embed=embed)
        await asyncio.sleep(4)
        embed = discord.Embed(title=f"{member} info ",
                              description=f"*Email `{member}@hacked.com` Password `{random.choice(passwords)}`  IP `{fakeips}`*",
                              color=0x2f3136)
        embed.set_footer(text=f"Hacked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await asyncio.sleep(1)
        await m.edit(embed=embed)

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        """> Get info of spotify song [user] is listening to"""
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                em = discord.Embed(color=activity.color)
                em.title = f'{user.name} is listening to {activity.title}'
                em.set_thumbnail(url=activity.album_cover_url)
                em.description = f"Song Name: {activity.title}\nSong Artist: {activity.artist}\nSong Album: {activity.album}\
                \nSong Lenght: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def slot(self, ctx):
        """> Play slot machine game"""
        emojis = [":apple:", ":tangerine:", ":pear:", ":lemon:", ":watermelon:", ":grapes:", ":strawberry:", ":cherries:"]
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        owner = self.bot.get_user(684644222615158834)
        if ctx.author == owner:
            a = random.choice(emojis)
            b = a
            c = a

        slotmachine = f"{a} {b} {c}"

        if (a == b == c):
            name=":tada: Congrats you won! :tada:"
            value=f"{slotmachine}"
        else:
            name="You lost"
            value=f"{slotmachine}"

        embed = discord.Embed(title="Slotmachine", colour=ctx.author.colour)
        embed.add_field(name=name, value=f"> {value}")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name)
        #embed.set_footer()
        await ctx.send(embed=embed)

    @commands.command(aliases=["rolldice"])
    @commands.guild_only()
    async def roll(self, ctx, dice: str):
        """> Rolls a dice in NdN format (e.g. 2d6)"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        embed = discord.Embed(colour=ctx.author.colour,
                              title='Outcomes:',
                              description=f'{result}')
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author} rolled")
        await ctx.send(embed=embed)

    @commands.command(aliases=["coinflip", "flip"])
    @commands.guild_only()
    async def toss(self, ctx):
        """> Coin flip!"""
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(['Heads','Tails'])}**!")

    @commands.command(aliases=['predict'])
    @commands.guild_only()
    async def guess(self, ctx):
        """> Number guessing game"""
        await ctx.send('Guess a number between 1 and 10.')
        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()
        answer = random.randint(1, 10)
        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long it was {}.'.format(answer))
        if int(guess.content) == answer:
            await ctx.send('You are right!')
        else:
            await ctx.send('Oops. You are wrong. It is actually {}.'.format(answer))

    @commands.command(aliases=['penis', 'howbig', 'pickle'])
    @commands.guild_only()
    async def pp(self, ctx, *, user: discord.Member = None):
        """> how big pp"""
        if user is None:
            user = ctx.author
        owner = self.bot.get_user(684644222615158834)
        if user == owner:
            return await ctx.send(embed=discord.Embed(title='PP size machine',
                              description=f"{user.name}'s penis\n8===============D",
                              colour=ctx.author.colour))
        bot = self.bot.get_user(780851858096390204)
        if user == bot:
            return await ctx.send("I'm a bot stupid")
        size = random.randint(1,15)
        pp = size*"="
        embed = discord.Embed(title='PP size machine',
                              description=f"{user.name}'s penis\n8{pp}D",
                              colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', 'fortune'])
    @commands.guild_only()
    async def _8ball(self, ctx, *, question):
        """> Ask the magic 8ball about your future!"""
        await ctx.send("{}: {}".format(ctx.author.name, random.choice(magic_conch_shell)))

    @commands.command(aliases=["wiferank"])
    async def waifu(self, ctx, user: discord.Member = None):
        """> See how good of a waifu you are"""
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=ctx.author.colour
        )
        embed.add_field(name='**Waifu r8 machine**', value=f'{user.display_name} is {random.choice(Number1)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=["rekt"])
    @commands.guild_only()
    async def roast(self, ctx, member: discord.Member = None):
            """>  Sick of someone? Easy! Just roast them!"""
            await ctx.trigger_typing()
            if member is None:
                member = ctx.author
            bot = self.bot.get_user(780851858096390204)
            if member == bot:
                return await ctx.send("Don't you dare doing that!")
            owner = self.bot.get_user(684644222615158834)
            if member == owner:
                return await ctx.send("I'm not going to do that.")
            await ctx.send("{random.choice(roasts)}")

    @commands.command(aliases=["drunk"])
    @commands.guild_only()
    async def actdrunk(self, ctx):
        """> Act like you are drunk"""
        await ctx.send(random.choice(drunkaf))

    @commands.command(aliases=["quote", "repeat"])
    async def sayings(self, ctx, *, quote: str = None):
        """> Make the bot say whatever you want!"""
        if quote == None:
            await ctx.send('What are u saying!')
            return
        await ctx.send('{}\n\n**- {}**'.format(quote, ctx.author))

    @commands.command(aliases=["rn", "number"])
    @commands.guild_only()
    async def randomnumber(self, ctx, *, digits: int = 1):
        """> Generates a random number with the specified length of digits"""
        number = ""
        for i in range(digits):
            number += str(random.randint(0, 9))
        await ctx.send(number)

    @commands.command(aliases=['pfp', 'av'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.User = None):
        """> Displays what avatar user is using"""
        user = user or ctx.author
        AB01 = self.bot.get_user(684644222615158834)
        if user is self.bot.user:
            embed = discord.Embed(colour=discord.Colour.from_rgb(250, 0, 0),
                                  title=f'{self.bot.user.name}\'s Profile Picture!')
            embed.set_image(url=self.bot.user.avatar_url_as(static_format='png'))
            embed.set_footer(text=f'Huge thanks to {AB01} for this avatar')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.from_rgb(250, 0, 0),
                                  title=f'{user}\'s Profile Picture!')
            embed.set_image(url = user.avatar_url_as(static_format='png'))
            await ctx.send(embed=embed)

    @commands.command(aliases=['howhot'])
    @commands.guild_only()
    async def hot(self, ctx, *, user: discord.Member = None):
        """> Check someones hotness"""
        user = user or ctx.author
        owner = self.bot.get_user(684644222615158834)
        if user == owner:
            return await ctx.send("My hot calculator has melted down, because of him.")

        bot = self.bot.get_user(780851858096390204)
        if user == bot:
            return await ctx.send("I'm too hot for you 😏")

        if user is None:
            user = ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "\U0001f494"
        if hot > 25:
            emoji = "\U0001f494"
        if hot > 50:
            emoji = "\U00002764"
        if hot > 75:
            emoji = "\U0001f49e"
        await ctx.send(embed=discord.Embed(title="hot r8 machine", colour=ctx.author.colour,
                                           description=f"**{user}** is **{hot:.2f}%** hot. {emoji}"))

    @commands.command(aliases=["slap_member", "hit"])
    @commands.guild_only()
    async def slap(self, ctx, member: discord.Member = None, *, reason: commands.clean_content = None):
        """> Slap someone shitless with this"""
        if reason is None:
            reason = 'for no reason'
        if member is None:
            return await ctx.send(f"{ctx.author.name} slapped himself. He's so dumb!")
        bot = self.bot.get_user(780851858096390204)
        if member == bot:
            return await ctx.send("Don't you dare doing that!")
        owner = self.bot.get_user(684644222615158834)
        if member == owner:
            return await ctx.send("You can't do that.")
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

    @slap.error
    async def slap_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member.")

    @commands.command()
    async def fact(self, ctx):
        """> It is just a fact bro"""
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                fact = r['text']
                embed = discord.Embed(title=f'Random Fact', colour=ctx.author.colour, timestamp=ctx.message.created_at)

                embed.add_field(name='***Fun Fact***', value=fact, inline=False)
                await ctx.send(embed=embed)

    @commands.command(aliases=["select", "pick"])
    @commands.guild_only()
    async def choose(self, ctx, *choices: str):
        """> Choose between multiple choices"""
        try:
            choice = "`" + '`, `'.join(choices) + "`"
            embed = discord.Embed(colour=ctx.author.colour,
                                  description=f"**Choices:** {choice}\n**I'd choose:** `{random.choice(choices)}`")
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(f"❌ Can't choose from empty choices")

    @commands.command(aliases=["overturn"])
    @commands.guild_only()
    async def reverse(self, ctx, *, text: str):
        """> Reverse something"""
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")

        embed = discord.Embed(colour=ctx.author.colour, title='Text was reversed!',
                              description=f"**Input:** {text}\n**Output:** {t_rev}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["gayrate"])
    @commands.guild_only()
    async def howgay(self, ctx, *, user: discord.User = None):
        """> See how gay someone is (100% real)"""
        bot = self.bot.get_user(780851858096390204)
        owner = self.bot.get_user(684644222615158834)
        if user == bot or user == bot:
            return await ctx.send("Bot's can't be gay. You are so dumb!")
        if user == owner or user == owner:
            return await ctx.send(embed=discord.Embed(title="gay r8 machine", colour=discord.Colour.from_rgb(250,0,0),
                                                      description=f"{ctx.author.name} is 100% gay"))
        if user is None:
            user = ctx.author.name
        num = random.randint(0, 100)
        deci = random.randint(0, 9)
        if num == 100:
            deci = 0
        rating = f"{num}.{deci}"
        embed = discord.Embed(title='gay r8 machine',
                              description = f"{user.name} is {rating}% gay :rainbow_flag:",
                              colour=ctx.author.colour)
        await ctx.send(embed = embed)

    @commands.command(aliases=['simpr8', 'howsimp'])
    @commands.guild_only()
    async def simp(self, ctx, user: discord.Member = None):
        """> See how simp someone is, 100% official score"""
        if user is None:
            user = ctx.author
        owner = self.bot.get_user(684644222615158834)
        if user == owner:
            return await ctx.send(embed = discord.Embed(title='simp r8 machine',
                                description=f"{user.name} is 100% simp",
                                colour=discord.Colour.from_rgb(250, 0, 0)))
        bot = self.bot.get_user(780851858096390204)
        if user == bot:
            return await ctx.send("I'm a bot not a simp.")
        num = random.randint(0, 100)
        deci = random.randint(0, 9)
        if num == 100:
            deci = 0
        rating = f"{num}.{deci}"
        embed = discord.Embed(title='simp r8 machine',
                                description=f"{user.name} is {rating}% simp",
                                colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def fight(self, ctx, user1: discord.Member, user2: discord.Member = None):
        """> Fight someone! Wanna fight with yourself? Leave [user2] empty"""
        if user2 == None:
            user2 = ctx.author
        bot = self.bot.get_user(780851858096390204)
        owner = self.bot.get_user(684644222615158834)
        if user1 == bot or user2 == bot:
            return await ctx.send("I'm not fighting with anyone.")
        if user1 == owner or user2 == owner:
            return await ctx.send("AB01 fucked you up so hard that you died immediately.")
        win = random.choice([user1, user2])
        if win == user1:
            lose = user2
        else:
            lose = user1
        responses = [
            f'That was intense battle, but unfortunatelly {win.mention} has beaten up {lose.mention} to death',
            f'That was a shitty battle, they both fight themselves to death',
            f'Is that a battle? You both suck',
            f'Yo {lose.mention} you lose! Ha',
            f'I\'m not sure how, but {win.mention} has won the battle']
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    @commands.guild_only()
    async def urban(self, ctx, *, urban: str):
        """> Search for a term in the urban dictionary """
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'http://api.urbandictionary.com/v0/define?term={urban}') as r:
                url = await r.json()
        if url is None:
            return await ctx.send("No URL found")
        count = len(url['list'])
        if count == 0:
            return await ctx.send("No results were found.")
        result = url['list'][random.randint(0, count - 1)]
        definition = result['definition']
        example = result['example']
        if len(definition) >= 1000:
            definition = definition[:1000]
            definition = definition.rsplit(' ', 1)[0]
            definition += '...'
        embed = discord.Embed(color=ctx.author.colour,
                              description=f"**Search:** {result['word']} | **by:** {result['author']}")
        embed.add_field(
            name="Votes:", value=f"\U0001f44d **{result['thumbs_up']}** | \U0001f44e **{result['thumbs_down']}**",
            inline=False)
        embed.add_field(name="Definition", value=definition, inline=True)
        embed.add_field(name="Example", value=example, inline=True)
        embed.set_footer(text=f"© {self.bot.user.name}")
        async with ctx.channel.typing():
            await asyncio.sleep(5)
            return await ctx.send(embed=embed)

    @commands.command()
    async def rps(self, ctx, choice=None):
        """> Play the famous "Rock, Paper, Scissors" game against me!"""
        if choice == None:
            embed = discord.Embed(
                title='You gotta give a choice!',
                color=discord.Color.red(),
                description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. \
                The valid options are:\n`rock` `paper` `scissor`'
            )
            await ctx.send(embed=embed)
        else:
            x = choice.lower()
            option = ['rock', 'paper', 'scissor']
            op = random.choice(option)
            if x == 'rock' or x == 'r' or x == '✊' or x == ':fist:':
                if op == 'rock':
                    await ctx.send(embed=discord.Embed(title=f"It's a tie!", colour=ctx.author.colour,
                         description=f'{ctx.author.name} **picked:** ✊ `rock`\
                         \n{self.bot.user.name} **picked:** ✊ `rock`\n> {random.choice(rps_d)}'))
                elif op == 'paper':
                    await ctx.send(embed=discord.Embed(title=f"I win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** ✊ `rock`\
                                             \n{self.bot.user.name} **picked:** :back_of_hand: `paper`\n> {random.choice(rps_l)}'))
                elif op == 'scissor':
                    await ctx.send(embed=discord.Embed(title=f"You Win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** ✊ `rock`\
                                             \n{self.bot.user.name} **picked:** :v: `scissor`\n> {random.choice(rps_w)}'))
            elif x == 'scissor' or x == 's' or x == ':scissors:' or x == ':v:':
                if op == 'rock':
                    await ctx.send(embed=discord.Embed(title=f"I win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :v: `scissor`\
                                             \n{self.bot.user.name} **picked:** ✊ `rock`\n> {random.choice(rps_l)}'))
                elif op == 'paper':
                    await ctx.send(embed=discord.Embed(title=f"You Win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :v: `scissor`\
                                             \n{self.bot.user.name} **picked:** :back_of_hand: `paper`\n> {random.choice(rps_w)}'))
                elif op == 'scissor':
                    await ctx.send(embed=discord.Embed(title=f"It's a tie!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :v: `scissor`\
                                             \n{self.bot.user.name} **picked:** :v: `scissors`\n> {random.choice(rps_d)}'))
            elif x == 'paper' or x == 'p' or x == ':back_of_hand:':
                if op == 'rock':
                    await ctx.send(embed=discord.Embed(title=f"You win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :back_of_hand: `paper`\
                                             \n{self.bot.user.name} **picked:** ✊ `rock`\n> {random.choice(rps_w)}'))
                elif op == 'paper':
                    await ctx.send(embed=discord.Embed(title=f"It's a tie!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :back_of_hand: `paper`\
                                             \n{self.bot.user.name} **picked:** :back_of_hand: `paper`\n> {random.choice(rps_d)}'))
                elif op == 'scissor':
                    await ctx.send(embed=discord.Embed(title=f"I win!", colour=ctx.author.colour,
                                                       description=f'{ctx.author.name} **picked:** :back_of_hand: `paper`\
                                             \n{self.bot.user.name} **picked:** :v: `scissors`\n> {random.choice(rps_l)}'))
            else:
                embed = discord.Embed(
                    title='You gotta give a choice!',
                    color=discord.Color.red(),
                    description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. The valid options are:\n`rock` `paper` `scissor`'
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def decipher(self, ctx): #, opt='Easy'
        """> Decipher a word"""
        """options = ['easy', 'medium', 'hard', 'impossible']
        if not opt.lower() in options:
            await ctx.send('Give a valid difficulty.\n**Current Difficulties:**\n> `Easy` `Medium` `Hard` `Impossible`')
            return
        choice = opt.lower()
        if choice == 'easy':
            choice = random.choice(easy)
        elif choice == 'medium':
            choice = random.choice(medium)
        elif choice == 'hard':
            choice = random.choice(hard)
        elif choice == 'impossible':
            choice = random.choice(impossible)"""
        x = list(random.choice(easy))
        random.shuffle(x)
        await ctx.send('**⬇ The word you must decipher is ⬇**')
        await ctx.send(' '.join(map(str, x)))

        def check(m):
            user = ctx.author
            if m.author.id == user.id and m.content.lower() == choice.lower():
                return True
            return False

        try:
            await self.bot.wait_for('message', timeout=15.0, check=check)
            await ctx.send(f'**Congratulations {ctx.author}! You got the correct word.**')
        except asyncio.TimeoutError:
            await ctx.send('Your answer is **INCORRECT!**')
            await ctx.send(f'**The correct word was {choice}**')

def setup(bot):
    bot.add_cog(Fun(bot))
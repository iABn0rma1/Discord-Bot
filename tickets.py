import discord, sqlite3, datetime
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["open"])
    @commands.guild_only()
    async def topen(self, ctx):
        """> Open a ticket"""
        arg = f"{ctx.author.name}"
        argplus = arg.replace(" ", "-")
        args = str(ctx.author).replace(' ', '-').replace('#', '_').lower()
        if not discord.utils.get(ctx.guild.text_channels, name=args) == None:
            await ctx.send(f"{ctx.author.mention} You already have a ticket!")
        else:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                          ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                          ctx.author: discord.PermissionOverwrite(send_messages=True, read_messages=True)}
            channel = await ctx.guild.create_text_channel(args, overwrites=overwrites,
                                                          topic=f"Ticket Owner: {ctx.author}\nTicket Owner ID: {ctx.author.id}\n#NemesisAintBorn",
                                                          slowmode_delay=1)
            embed = discord.Embed(title="New ticket!",
                                  description=f"Hey {ctx.author.name}, I've created a ticket just for you!",
                                  color=discord.Colour.from_rgb(250,0,0))
            await ctx.send(f"I created a channel for you! ({channel.mention})")
            await channel.send(f"@everyone", embed=embed)
            conn = sqlite3.connect('mybot.db')
            cur = conn.cursor()
            cur.execute("Select channelID from WelcomeChannel where guildID = ?", (ctx.guild.id,))
            check = cur.fetchone()
            conn.close()
            embed = discord.Embed(title=f"Ticket opened!",
                                  description=f"Ticket opened by {ctx.author} ({ctx.author.mention} **|** {ctx.author.id})",
                                  color=discord.Colour.from_rgb(250,0,0), timestamp=datetime.datetime.utcnow())
            if check is None:
                pass
            else:
                try:
                    channel = self.bot.get_channel(check[0])
                    await channel.send(embed=embed)
                except:
                    pass

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Tshut(self, ctx):
        """> Close an opened ticket"""
        try:
            if not ctx.channel.topic.endswith("#NemesisAintBorn"):
                await ctx.send("Sorry, this isn't a ticket, so I can't close it!")
            else:
                try:
                    await ctx.channel.delete(reason=f"Closed by {ctx.author}")
                    conn = sqlite3.connect('mybot.db')
                    cur = conn.cursor()
                    cur.execute("Select channelID from WelcomeChannel where guildID = ?", (ctx.guild.id,))
                    check = cur.fetchone()
                    conn.close()
                    embed = discord.Embed(title=f"Ticket closed!",
                                          description=f"Ticket closed by {ctx.author} ({ctx.author.mention} **|** {ctx.author.id})",
                                          color=0xff0000, timestamp=datetime.datetime.utcnow())
                    if check is None:
                        pass
                    else:
                        try:
                            channel = self.bot.get_channel(check[0])
                            await channel.send(embed=embed)
                        except:
                            pass
                except:
                    await ctx.send("I couldn't delete this channel, please make sure I have all necessary permissions")
        except Exception as ex:
            await ctx.send(
                f"Sorry, I encountered an error! If this is repetitive report it to my support server!\nError: `{ex}`")

def setup(bot):
    bot.add_cog(Tickets(bot))

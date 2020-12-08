import discord
import asyncio
import random
import os
from discord.ext import commands
from discord.ext.commands import BucketType

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 50000, BucketType.user)
    async def report(self, ctx, *args):
        """> Reports to the developer"""
        if args == []:
            await ctx.send('Please give me a report to send. This has been flagged.')
            return
        counter = random.randint(1, 1000)
        channel = self.bot.get_channel(783793077918629939)
        x = ' '.join(map(str, args))
        if x == None:
            await ctx.send('You going to report nothing?')
        else:
            embed = discord.Embed(
                title=f'Report #{counter}',
                color=discord.Color.from_rgb(250,0,0),
                description=f'The user `{ctx.author}` from the guild `{ctx.guild}` has sent a report!'
            )
            embed.add_field(name='Query?', value=f'{x}')
            embed.set_footer(text=f'User ID: {ctx.author.id}\nGuild ID: {ctx.guild.id}')
            await channel.send(embed=embed)
            await ctx.send(f'Your report has successfully been sent!')

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        msg = await ctx.send('Syncing now!')
        for file in os.listdir('.'):
            if file.endswith('.py'):
                try:
                    self.bot.reload_extension(f"cogs.{file[:-3]}")
                except Exception:
                    pass
        await msg.edit(content='I\'m synced!')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        if ctx.author.id == 684644222615158834:
            await ctx.send('Going offline now!')
            await self.bot.change_presence(status=discord.Status.invisible)
            exit()
        else:
            await ctx.send('You do not own me.')

def setup(bot):
    bot.add_cog(Management(bot))

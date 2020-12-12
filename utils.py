import discord

from discord.ext import commands
from datetime import datetime


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id != 671078170874740756:
            return

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == 772461778470830110:
            if str(payload.emoji) in self.bot.config.ROLES:
                role = guild.get_role(self.bot.config.ROLES[str(payload.emoji)])
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id != 671078170874740756:
            return

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == 772461778470830110:
            if str(payload.emoji) in self.bot.config.ROLES:
                role = guild.get_role(self.bot.config.ROLES[str(payload.emoji)])
                await user.remove_roles(role)

    @commands.command(brief='Privacy policy', aliases=['pp', 'policy', 'privacypolicy'])
    async def privacy(self, ctx):
        e = discord.Embed(color=discord.Color.blurple(), title=f"{self.bot.user} Privacy Policy's")
        e.add_field(name='What data is being stored?', value="No data of you is being stored as of now", inline=False)
        e.add_field(name='What should I do if I have any concerns?', value=f"You can shoot a direct message to **{ctx.guild.owner}** or email us at `dreddhelp@gmail.com`")
        await ctx.send(embed=e)

    @commands.command(name='time', brief='Displays Moksej\'s time')
    async def time(self, ctx):
        time = datetime.now()
        await ctx.send(f"Current <@345457928972533773>'s time is: {time.strftime('%H:%M')} CET (Central European Time)", allowed_mentions=discord.AllowedMentions(users=False))

def setup(bot):
    bot.add_cog(Utils(bot))
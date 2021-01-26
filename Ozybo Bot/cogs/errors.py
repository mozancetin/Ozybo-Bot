import discord
from discord.ext import commands

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                await ctx.send(f"You are on cooldown. Try again in about {round(error.retry_after / 3600)} hour")
            elif 60 < error.retry_after < 3600:
                await ctx.send(f"You are on cooldown. Try again in about {round(error.retry_after / 60)} min")
            elif error.retry_after < 60:
                await ctx.send(f"You are on cooldown. Try again in {int(error.retry_after)} sec")






def setup(bot):
    bot.add_cog(Errors(bot))
import discord
from discord.ext import commands
import random
import asyncio

PARTY_ROLE_ID = None # Give as a int
class Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def party(self, ctx):
        role = ctx.guild.get_role(PARTY_ROLE_ID)
        for i in range(100):
            await role.edit(colour=discord.Colour(random.randint(0, 16777215)))
            await asyncio.sleep(0.1)


def setup(bot):
    bot.add_cog(Role(bot))
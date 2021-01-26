import discord
import sqlite3
from discord.ext import commands

class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)} ms")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix : str):
    
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
    
        cmd = "UPDATE servers SET prefix = ? WHERE guild_id = ?"
        cursor.execute(cmd, (prefix, str(ctx.guild.id)))
        db.commit()
        db.close()

        await ctx.send(f"Prefix has changed: `{prefix}`")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        embed = discord.Embed(color = discord.Colour.red(), description=f"Please wait a moment {ctx.author.mention}!")
        await ctx.send(embed=embed)
        await ctx.channel.purge(limit=amount+1)



def setup(bot):
    bot.add_cog(Server(bot))
import discord
import sqlite3
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.exist = False

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason = reason)
        await ctx.send(f"{member.mention} was kicked from the server!")
    
    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        await member.mute(reason=reason)
        await ctx.send(f"{member} user was silenced!")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason = reason)
        await ctx.send(f"{member.mention} was banned from the server!")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention}'s ban has been removed.")
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user : discord.User, *, args=None):
        user_id = user.id

        if user_id != None and args != None:
            try:
                target = await self.bot.fetch_user(user_id)
                await target.send(args)

                await ctx.send("The message was sent to: " + target.name)
            except:
                await ctx.send("Message could not be sent!")
        else:
            await ctx.send("Please write message and user!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx, *, args=None):

        if args != None:
            members = ctx.guild.members
            for member in members:
                if member == self.bot.user:
                    continue
                try:
                    await member.send(args)
                    await ctx.send("The message was sent to: " + member.mention)
                except:
                    await ctx.send("The message could not be sent to: " + member.mention)
        else:
            await ctx.send("Please write your message!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dmrole(self, ctx, role : discord.Role = None, *, args=None):
        self.exist = False

        if args != None and role != None:
            members = ctx.guild.members
            for member in members:
                if role in member.roles:
                    try:
                        self.exist = True
                        await member.send(args)
                        await ctx.send("The message was sent to: " + member.mention)
                    except:
                        await ctx.send("The message could not be sent to: " + member.mention)
            if not self.exist:
                await ctx.send(f"There is no one using the {role} role on the server")
        else:
            await ctx.send("Please write message and role!")

def setup(bot):
    bot.add_cog(Moderation(bot))
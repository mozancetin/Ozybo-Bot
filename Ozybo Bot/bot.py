import os
import sqlite3
import discord
from itertools import cycle
from discord.ext import commands, tasks

ROLE_CHANNEL_ID = None # Give as a int
GUEST_ROLE_NAME = "" # Give as a string
MESSAGE_CHANNEL_NAME = "" # Give as a string
BOT_TOKEN = "" # Give as a string

def get_prefix(bot, message):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    sorgu = "SELECT prefix FROM servers WHERE guild_id = ?"
    cursor.execute(sorgu, (str(message.guild.id),))
    prefix = cursor.fetchone()
    db.close()
    return prefix


def get_guilds():

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    sorgu = "SELECT guild_name FROM servers"
    cursor.execute(sorgu)

    guilds = cursor.fetchall()
    db.close()
    return len(guilds)


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
status = cycle([f"Şu anda {get_guilds()} sunucuda aktifim!","Robotlar evreni ele geçirecek hahahaha!", "Eğleniyorum", "Hayatımı sorguluyorum", "Hey!", "Ben kimim?", "Burada ne işim var?", "42", "Made by Ozybo"])


@bot.event
async def on_ready():
    
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS servers(guild_name TEXT, guild_id TEXT, prefix TEXT, rolemessageid INT, commandschannelid INT)")
    db.close()

    db2 = sqlite3.connect("users.sqlite")
    cursor = db2.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_name TEXT, user_id TEXT, xp INT, level INT, levelxp INT, cash INT)")
    db2.close()

    print("Logged in as: " + bot.user.name + "\n")
    await change_status.start()

@tasks.loop(minutes = 1)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(status)))

@bot.event
async def on_guild_join(guild):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    sorgu = "INSERT INTO servers VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sorgu, (guild.name, str(guild.id), ".", "Null","Null"))
    db.commit()
    db.close()

@bot.event
async def on_guild_remove(guild):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    sorgu = "DELETE FROM servers WHERE guild_name = ?"
    cursor.execute(sorgu, (guild.name,))
    db.commit()
    db.close()

@bot.event
async def on_member_join(member):
    
    role_channel = bot.get_channel(ROLE_CHANNEL_ID)
    print(f'{member} aramıza katıldı!')
    for role in member.guild.roles:
        if role.name == GUEST_ROLE_NAME:
            await member.add_roles(role)
    for channel in member.guild.channels:
        if channel.name == MESSAGE_CHANNEL_NAME:
            embed = discord.Embed(color=discord.Colour.dark_magenta())
            embed.set_author(name=f"Sunucumuza Hoşgeldin {member.name}!")
            embed.set_thumbnail(url=member.avatar_url)

            embed.add_field(name="Seninle birlikte tam şu kadar kişi olduk:", value=f":sunglasses: {len(list(member.guild.members))} :sunglasses:", inline = False)
            embed.add_field(name="Bu kanaldan istediğin rolü alabilirsin:", value=role_channel.mention, inline = False)
            await channel.send(embed=embed)


    db2 = sqlite3.connect("users.sqlite")
    cursor = db2.cursor()
    sorgu = "SELECT * FROM users WHERE user_id = ?"
    cursor.execute(sorgu, (str(member.id),))
    users = cursor.fetchall()
    if len(users) > 0:
        return
    else:
        sorgu = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)"
        cursor.execute(sorgu, (str(member), str(member.id), 0, 1, 10, 0))
        db2.commit()
    db2.close()

@bot.event
async def on_member_remove(member):
    print(f'{member} aramızdan ayrıldı.')
    
    db2 = sqlite3.connect("users.sqlite")
    cursor = db2.cursor()

    sorgu = "DELETE FROM users WHERE user_id = ?"
    cursor.execute(sorgu, (str(member.id),))
    db2.commit()
    db2.close()

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f"Extension: {extension} is up to date!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
    
bot.run(BOT_TOKEN)

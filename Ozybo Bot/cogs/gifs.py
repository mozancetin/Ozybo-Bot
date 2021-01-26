import discord
import giphy_client
from discord.ext import commands
from giphy_client.rest import ApiException

GIPHY_API_KEY = "" # Give as a string
class Gif(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_instance = giphy_client.DefaultApi()
        self.api_key = GIPHY_API_KEY
        self.fmt = 'json'

    @commands.command()
    async def randomgif(self, ctx, *, tag : str = "rainbow"):

        tag = tag.replace(" ","-")
        api_response = self.api_instance.gifs_random_get(self.api_key, tag=tag, fmt=self.fmt)
        url = api_response.data.image_original_url

        embed = discord.Embed(color = discord.Colour.dark_purple())
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def marvel(self, ctx):

        tag = "marvel"
        api_response = self.api_instance.gifs_random_get(self.api_key, tag=tag, fmt=self.fmt)
        url = api_response.data.image_original_url
        
        embed = discord.Embed(color = discord.Colour.dark_purple())
        embed.set_image(url=url)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Gif(bot))

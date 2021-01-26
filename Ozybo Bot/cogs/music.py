import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import asyncio


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.queue_run = False

    @commands.command(pass_context=True, aliases=['j', 'joi'], help = "Bot bulunduğunuz ses kanalına katılır. Kullanım: .join / .j / .joi")
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            #await voice.move_to(channel)
            await ctx.send("Bot şu anda başka bir kanalda!")
        else:
            voice = await channel.connect()
            print(f"The bot has connected to {channel}\n")
            await ctx.send(f"Bot {channel} kanalına katıldı!")
    
    @commands.command(pass_context=True, aliases=['l', 'lea'],help = "Bot ses kanalından ayrılır. Kullanım: .leave / .l / .lea")
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Bot başarıyla {channel} kanalından çıkartıldı.")
        else:
            print("Bot was told to leave voice channel, but was not in one")
            await ctx.send("Herhangi bir ses kanalında olduğumu sanmıyorum.")
    
    @commands.command(pass_context=True, aliases=['p', 'pla'],help = "Şarkıyı başlatır. Kullanmadan önce join ile katılmanız gerekir. Kullanım: .play [youtube link]")
    async def play(self, ctx, url: str):
        def check_queue():
            try:
                if self.queue != 0:
                    ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}]}
                    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

                    print("Müzik başlatıldı.")
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(self.queue[0], download=False)
                        URL = info['formats'][0]['url']
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: check_queue())
                    self.queue.pop(0)
                else:
                    return False
            except Exception:
                print("Sıra bitti.")
                return False


        self.queue.append(url)
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await ctx.send("Şarkı sıraya eklendi.")
            return False
        else:
            isQueue = check_queue()

    @commands.command(pass_context=True, aliases=['pa', 'pau'],help = "Şarkıyı duraklatır. Kullanım: .pause / .pa / .pau")
    async def pause(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Müzik durduruldu.")
        else:
            print("Music not playing failed pause")
            await ctx.send("Oynayan bir müzik olmadığı için dondurulamadı.")
    
    @commands.command(pass_context=True, aliases=['r', 'res'], help = "Duraklamış şarkıyı devam ettirir. Kullanım: .resume / .r / .res")
    async def resume(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Resumed music")
            voice.resume()
            await ctx.send("Müzik devam ettiriliyor.")
        else:
            print("Music is not paused")
            await ctx.send("Müzik durmuş durumda değil.")

    @commands.command(pass_context=True, aliases=['s', 'sto'], help = "Şarkıyı kapatır. Kullanım: .stop / .s / .sto")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        self.queue.clear()
        self.clear_run = False

        if voice and voice.is_playing():
            print("Music stopped")
            voice.stop()
            await ctx.send("Müzik kapatıldı.")
        else:
            print("No music playing failed to stop")
            await ctx.send("Hali hazırda oynayan bir müzik yok.")
    
    @commands.command(pass_context=True, aliases=['n', 'nex'], help = "Sıradaki şarkıya geçer. Kullanım: .next / .n / .nex")
    async def next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Playing Next Song")
            voice.stop()
            await ctx.send("Sonraki şarkıya geçiliyor.")
        else:
            print("No music playing")
            await ctx.send("Çalınan bir şarkı bulunamadı.")

def setup(bot):
    bot.add_cog(Music(bot))

import asyncio

import discord
import youtube_dl
from discord import VoiceClient, FFmpegPCMAudio
from discord.ext import commands

import env
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def test(e):
    if not e:   print(42)


@bot.command()
async def yt(ctx, *, url):
    """Plays from a url (almost anything youtube_dl supports)"""

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        ctx.voice_client.play(player, after=test)

    await ctx.send(f'Now playing: {player.title}')


@bot.command(pass_context=True)
async def pause(ctx):
    voice: VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("not playing anything")


@bot.command(pass_context=True)
async def resume(ctx):
    voice: VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Not currently paused")


@bot.command(pass_context=True)
async def stop(ctx):
    voice: VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Stopping")


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel. Please join one beforehand")


@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel")


async def main():
    async with bot:
        # await bot.add_cog(Music(bot))
        await bot.start(env.DISCORD_TOKEN)

bot.run(env.DISCORD_TOKEN)

import asyncio

import discord
import youtube_dl
from discord.ext import commands

from DiscordBots.Utils.music_queue import Music
from DiscordBots.commands.music_player import MusicPlayer

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


class YoutubePlayer(MusicPlayer):
    @staticmethod
    def after(e):
        print(f'Player error: {e}') if e else None

    async def load_playlist(self, url) -> int:
        playlist = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        for music in playlist["entries"]:
            self.music_player.add(Music(
                name=f"{music['title'].strip()}",
                track=music.get("webpage_url")
            ))
        return len(playlist["entries"])

    async def start_loop(self, ctx):
        async def play_next():
            player = await YTDLSource.from_url(self.music_player.next(self.cursor).track, loop=self.bot.loop)
            ctx.voice_client.play(player, after=self.music_player.on_track_finish)
            await ctx.send(f'Now playing: {player.title}')

        while self.music_player.size and (self.cursor < self.music_player.size or ctx.voice_client.is_playing()):
            await play_next()
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            self.cursor += 1

    async def start(self, ctx, url=None):
        await super().start(ctx, url)
        self.task = await self.start_loop(ctx)
        await ctx.send("No more music to plays :(")
        self.cursor = 0

    @commands.command()
    async def yt(self, ctx, *, url, stream=True):
        """Plays from an url (almost anything youtube_dl supports)"""
        async with ctx.typing():
            new_elem = await self.load_playlist(url)
        await ctx.send(f"Added {new_elem} tracks to the queue: Total {self.music_player.size}")
        if not self.is_playing(ctx):
            await self.start(ctx)

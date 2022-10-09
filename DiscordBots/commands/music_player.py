from abc import abstractmethod

import discord
from discord import VoiceClient, Enum
from discord.ext import commands

from DiscordBots.Utils.music_queue import Queue


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_player = Queue()
        self.cursor = 0
        self.task = None

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("not playing anything")

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Not currently paused")

    @commands.command(pass_context=True)
    async def stop(self, ctx, silent=False):
        voice: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if not silent:
            await ctx.send("Stopping")

    @commands.command(pass_context=True)
    async def play(self, ctx):
        if self.is_playing(ctx):
            await ctx.send("Already Playing")
        await self.start(ctx)

    @commands.command(pass_context=True)
    async def previous(self, ctx):
        voice: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("Stopping")

    @commands.command(pass_context=True)
    async def volume(self, ctx, arg):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.source.volume = arg / 100

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        msg = ["Music in queue:"]

        if self.music_player.size:
            for index in range(self.music_player.size):
                msg.append(f"{index}: {self.music_player.queue[index].name}")
                if self.cursor == index:
                    msg[-1] = f"> {msg[-1]} <"
        msg = '\n'.join(msg)
        msg = f"```{msg}```"
        await ctx.send(msg)

    @staticmethod
    def is_playing(ctx):
        player: VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if player:
            return player.is_playing()
        return False

    @abstractmethod
    async def start(self, ctx, track=None):
        await self.ensure_voice(ctx)
        if self.is_playing(ctx):
            await self.stop(ctx, silent=True)

    @staticmethod
    async def ensure_voice(ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

import guildData
import asyncio, subprocess
from lib.lib import discord
from musicData import *
from botConst import loopState

class __baseClient:
    guild_id: int                   # Guild/Server ID
    channel_id: int                 # Voice Channel ID
    client: discord.VoiceClient     # Voice Client Handle
    song: Music = None              # Music currently playing
    queue: list[Music]              # Queued List
    loop: loopState                 # Play normally, repeat the queued list or repeat the current song

    is_paused: bool = False         # Song is paused
    is_loading: bool = False        # A song is being loaded

class voiceClient(__baseClient):
    def __init__(self, guild_id : int, channel_id : int, client : discord.VoiceClient, bot : discord.Bot) -> None:
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.client = client
        
        self.queue, self.loop = guildData.loadVoice(guild_id)

        asyncio.run_coroutine_threadsafe(self.worker(), bot.loop)

    async def worker(self) -> None:
        while self.client.is_connected():
            if not self.is_loading:
                # to implement
                pass
            await asyncio.sleep(0.3)
        
        self.cleanup()

    async def play(self, song : Music, musicLogger : lovedMusic) -> bool:
        if self.is_loading:
            return False
        else:
            self.is_loading = True
        
        songPath = os.path.join(GUILDPATH, str(self.guild_id), 'song.mp3')
        
        if os.path.exists(songPath):
            os.remove(songPath)

        if not musicLogger.get(song.id, songPath):
            # Cache Miss...  * Nerd Smug *

            download = subprocess.Popen(f'/usr/local/bin/yt-dlp -f mp3/bestaudio/best -x --audio-format mp3 -o "{songPath[:-4]}" {song.id}', shell = True)
            
            while download.poll() == None:
                if not self.client.is_connected():
                    download.terminate()
                    return True
                await asyncio.sleep(0)

        self.client.play(discord.FFmpegPCMAudio(source=songPath))
        song.play()
        self.is_paused = False
        self.song = song

        musicLogger.log(song.id, songPath)
        
        return True

    def pause(self) -> bool:
        if not self.is_paused:
            self.is_paused = True
            self.client.pause()
            self.song.pause()

            return True
        else:
            return False

    def unpause(self) -> bool:
        if self.is_paused:
            self.is_paused = False
            self.client.resume()
            self.song.play()

            return True
        else:
            return False

    def cleanup(self) -> None:
        self.client.cleanup()
        if self.guild_id in voiceClient.__voiceClients:
            voiceClient.__voiceClients.pop(self.guild_id)


    __voiceClients = {}

    @staticmethod
    def query(guild_id : int):
        if guild_id in voiceClient.__voiceClients:
            return voiceClient.__voiceClients[guild_id]
        return None

    @staticmethod
    def create(guild_id : int, channel_id : int, client : discord.VoiceClient, bot : discord.Bot):
        vc = voiceClient(guild_id, channel_id, client, bot)
        voiceClient.__voiceClients[guild_id] = vc
        return vc


def initializeVoice(client: discord.Bot, musicLogger : lovedMusic) -> None:
    async def userInVoice(ctx: discord.ApplicationContext):
        if not ctx.author.voice:
            await ctx.respond("You are not connected to a voice channel", delete_after=3)
            return False
        return True

    @client.slash_command(description="Connect bot to your voice channel")
    async def connect(ctx: discord.ApplicationContext):
        if not await userInVoice(ctx):
            return

        await ctx.defer()
        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if vClient == None:
            voiceClient.create(ctx.guild_id, vChannel.id, await vChannel.connect(), client)
            await ctx.respond(f"Bot is connected to {vChannel.mention}", delete_after=6)
        elif vClient.channel_id == vChannel.id:
            await ctx.respond("Bot is already connected to your voice channel", delete_after=3)
        else:
            await ctx.respond("Bot is already connected to a voice channel", delete_after=3)

    @client.slash_command(name='disconnect', description="Disconnect bot from a voice channel")
    async def disconnect(ctx: discord.ApplicationContext):
        if not await userInVoice(ctx):
            return
        
        await ctx.defer()
        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if vClient == None:
            await ctx.respond(f"Bot is not connected to a voice channel", delete_after=6)
        elif vClient.channel_id == vChannel.id:
            await vClient.client.disconnect()

            await ctx.respond("Bot successfully disconnected", delete_after=6)
        else:
            await ctx.respond("You are not connected to the Bot's voice channel", delete_after=3)

    @client.slash_command(name='play', description="Plays a song. If paused, resumes the song.")
    async def play(ctx: discord.ApplicationContext, query: discord.Option(str, "Song to search from youtube", required=False)):
        if not await userInVoice(ctx):
            return

        if query:
            await ctx.defer()
            result = youtubeQuery(query)

            if result.length == 0:
                await ctx.respond(f"No results for \"{query}\"", delete_after=3)
                return
            
            song = await result.display()

            if song == None:
                return

        if not ctx.author.voice:
            await ctx.respond("You are not connected to a voice channel", delete_after=3)
            return

        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if vClient == None:
            if not query:
                await ctx.respond("Bot is not connected to a voice channel", delete_after=6)
                return
            vClient = voiceClient.create(ctx.guild_id, vChannel.id, await vChannel.connect(), client)
        elif vClient.channel_id != vChannel.id:
            await ctx.respond("You must be connected with the bot's channel to play music", delete_after=3)
            return
        
        if not query:
            if vClient.unpause():
                await ctx.respond("Bot is paused")
            else:
                await ctx.respond("Bot is already paused", delete_after=6)
        else:
            if await vClient.play(song, musicLogger):
                await ctx.respond(embed = song.embed(client))
            else:
                await ctx.respond("A song is already being loaded. Please wait")

    @client.slash_command(name='pause', description="Pauses the bot")
    async def pause(ctx: discord.ApplicationContext):
        if not await userInVoice(ctx):
            return

        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if vClient == None:
            await ctx.respond("Bot is not connected to a voice channel", delete_after=6)
            return
        elif vClient.channel_id != vChannel.id:
            await ctx.respond("You must be connected with the bot's channel to play music", delete_after=3)
            return

        if vClient.pause():
            await ctx.respond("Bot is paused")
        else:
            await ctx.respond("Bot is already paused", delete_after=6)
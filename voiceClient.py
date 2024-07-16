import guildData
import asyncio, subprocess
import discord
from musicData import *
from botConst import *

class __baseClient:
    guild_id: int                           # Guild/Server ID
    channel_id: int                         # Voice Channel ID
    client: discord.VoiceClient             # Voice Client Handle
    song: Music = None                      # Music currently playing
    queue: list[Music]                      # Queued List
    loop: int                               # Play normally, repeat the queued list or repeat the current song

    is_paused: bool = False                 # Song is paused
    is_loading: bool = False                # A song is being loaded

    ytdlp_Proc: subprocess.Popen = None     # Youtube Downloader Handle

class voiceClient(__baseClient):
    def __init__(self, guild_id : int, channel_id : int, client : discord.VoiceClient, bot : discord.Bot) -> None:
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.client = client
        
        self.queue, self.loop = guildData.loadVoice(guild_id)

        asyncio.run_coroutine_threadsafe(self.worker(), bot.loop)

    async def disconnect(self) -> None:
        self.client.stop()
        await self.client.disconnect()

    async def worker(self) -> None:
        while self.client.is_connected():
            if not self.is_loading:
                # to implement
                pass
            await asyncio.sleep(0.3)
        
        self.cleanup()

    async def play(self, song : Music) -> bool:
        if self.is_loading:
            return False
        else:
            self.is_loading = True

        download = subprocess.Popen(f'/usr/local/bin/yt-dlp -f mp3/bestaudio/best -x --audio-format mp3 -o - {song.id}', shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for i in download.stderr:
            if i.decode().startswith("[download]"):
                break

        self.client.stop()
        if self.ytdlp_Proc != None and not self.ytdlp_Proc.poll():
            self.ytdlp_Proc.terminate()

        self.ytdlp_Proc = download

        self.client.play(discord.FFmpegPCMAudio(source=self.ytdlp_Proc.stdout, pipe=True))
        song.play()
        self.is_paused = False
        self.song = song

        self.is_loading = False
        
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
        self.client.stop()
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

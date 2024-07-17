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
    loop_ind: int = 0                       # current index for REPEAT_QUEUE
    is_paused: bool = False                 # Song is paused

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
            if not self.client.is_playing() and not self.is_paused:
                if self.loop == DEFAULT:
                    self.song = None
                    self.next()
                elif self.loop == REPEAT_QUEUE:
                    self.song = None
                    if len(self.queue) == 0:
                        self.loop_ind = 0
                    else:
                        self.loop_ind += 1
                        try:
                            self.play(self.queue[self.loop_ind])
                        except IndexError:
                            self.loop_ind = 0
                            self.play(self.queue[self.loop_ind])
                elif self.loop == REPEAT_SONG:
                    if self.song != None:
                        self.play(self.song)
                    else:
                        self.next()

            await asyncio.sleep(0.5)
        
        self.cleanup()

    def play(self, song : Music):
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

    def next(self) -> Music:
        try:
            song = self.queue.pop(0)
            self.play(song)
            guildData.updateVoice(self.guild_id, self.loop, self.queue)
            return song
        except IndexError:
            return None

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

    @staticmethod
    def loopState(guild_id : int) -> str:
        vGuild = voiceClient.query(guild_id)
        if vGuild:
            queue = vGuild.queue
            loop = vGuild.loop
        else:
            queue, loop = guildData.loadVoice(guild_id)

        if loop == REPEAT_SONG:
            loop = DEFAULT
        else:
            loop += 1

        if loop == DEFAULT:
            out = "Bot will play normally through the queued songs."
        elif loop == REPEAT_QUEUE:
            if vGuild:
                if vGuild.song != None:
                    queue.insert(0, vGuild.song)
                vGuild.loop_ind = 0
            out = "Bot will repeat songs in queue."
        elif loop == REPEAT_SONG:
            if vGuild:
                queue = queue[vGuild.loop_ind + 1:len(queue)]
            out = "Bot will repeat current song."

        if vGuild:
            vGuild.queue = queue
            vGuild.loop = loop

        guildData.updateVoice(guild_id, loop, queue)

        return out
    
    @staticmethod
    def queueGuild(guild_id : int, add : Music = None, remove = None):
        vGuild = voiceClient.query(guild_id)
        if vGuild:
            queue = vGuild.queue
            loop = vGuild.loop
            loop_ind = vGuild.loop_ind
        else:
            queue, loop = guildData.loadVoice(guild_id)
            loop_ind = 0
        
        if add:
            queue.append(add)
        elif remove != None:
            if remove == "all":
                queue = []
                loop_ind = 0
                removed = True
            else:
                if remove < 0 and remove >= len(queue):
                    return False
                if loop == REPEAT_QUEUE and remove < loop_ind:
                    loop_ind -= 1

                removed = queue.pop(remove)
        else:
            return queue
        
        if vGuild:
            vGuild.queue = queue
            vGuild.loop_ind = loop_ind

        guildData.updateVoice(guild_id, loop, queue)

        return True if add else removed

    def cleanup(self) -> None:
        self.client.stop()
        self.client.cleanup()
        if self.ytdlp_Proc != None and not self.ytdlp_Proc.poll():
            self.ytdlp_Proc.terminate()
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

import guildData
import asyncio, subprocess
import discord, fcntl
from musicData import *
from botConst import *

class __baseClient:
    guild_id: int                           # Guild/Server ID
    channel_id: int                         # Voice Channel ID
    client: discord.VoiceClient             # Voice Client Handle
    song: Music = None                      # Music currently playing
    queue: list[Music]                      # Queued List
    loop: int                               # Play normally, repeat the queued list or repeat the current song
    loop_ind: int = -1                      # current index for REPEAT_QUEUE
    is_paused: bool = False                 # Song is paused
    is_loading = asyncio.Event()            # Song is being loaded. (Async play lock)
    cancel: bool = False                    # Cancel request to a song that is about to play

    ytdlp_Proc: YoutubeStreamer = None     # Youtube Downloader Handle

class voiceClient(__baseClient):
    def __init__(self, guild_id : int, channel_id : int, client : discord.VoiceClient) -> None:
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.client = client

        self.queue, self.loop = guildData.loadVoice(guild_id)

        self.is_loading.set()
        asyncio.create_task(self.worker())

    async def disconnect(self) -> None:
        self.client.stop()
        await self.client.disconnect()
        self.cleanup()

    async def worker(self) -> None:
        try:
            while self.client.is_connected():
                await self.is_loading.wait()
                if not self.client.is_playing() and self.is_loading.is_set() and not self.cancel and not self.is_paused:
                    if self.loop == REPEAT_SONG:
                        if self.song != None:
                            await self.play(self.song)
                        else:
                            await self.next()
                    else:
                        self.song = None
                        if self.ytdlp_Proc:
                            self.ytdlp_Proc.terminate()
                            self.ytdlp_Proc = None

                        if self.loop == DEFAULT:
                            await self.next()
                        elif self.loop == REPEAT_QUEUE:
                            if len(self.queue) == 0:
                                self.loop_ind = 0
                            else:
                                self.loop_ind += 1
                                try:
                                    await self.play(self.queue[self.loop_ind])
                                except IndexError:
                                    self.loop_ind = 0
                                    await self.play(self.queue[self.loop_ind])

                await asyncio.sleep(0.5)

            self.cleanup()
        except:
            from traceback import format_exc
            from botPath import WORKERERRORPATH

            with open(WORKERERRORPATH, "w") as w:
                w.write(format_exc())

    async def play(self, song : Music, force = False):
        if not self.is_loading.is_set():
            if not force:
                return False
            while not self.is_loading.is_set():
                self.cancel = True
                await self.is_loading.wait()
            self.cancel = False

        if not self.client.is_connected():
            self.cancel = True
            return False

        self.is_loading.clear()

        if song == True:
            download = subprocess.Popen(['/usr/local/bin/yt-dlp', '-f', 'bestaudio/best', '-o', '-', '--', str(song.id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            fcntl.fcntl(download.stderr, fcntl.F_SETFL, fcntl.fcntl(download.stderr, fcntl.F_GETFL) | os.O_NONBLOCK)
            while download.poll() == None:
                if download.stderr.readline().startswith(b"[download]"):
                    break
                await asyncio.sleep(0.3)
                if self.cancel == True:
                    download.terminate()
                    self.is_loading.set()
                    return False

            self.client.stop()
            if self.ytdlp_Proc != None:
                self.ytdlp_Proc.terminate()

            self.ytdlp_Proc = YoutubeStreamer(download)

            self.client.play(discord.FFmpegPCMAudio(source=self.ytdlp_Proc, pipe=True))
            self.song = song
        else:
            self.client.stop()
            self.ytdlp_Proc.reset()
            self.song.seek(0)
            self.client.play(discord.FFmpegPCMAudio(source=self.ytdlp_Proc, pipe=True))

        self.song.play()
        self.is_paused = False
        guildData.updateRecent(self.guild_id, self.song)

        self.is_loading.set()
        return True

    async def next(self, index = 1, force = False) -> Music:
        try:
            if self.loop == REPEAT_QUEUE:
                try:
                    self.loop_ind += index
                    song = self.queue[self.loop_ind]
                except IndexError:
                    if len(self.queue) == 0:
                        self.loop_ind = -1
                        raise IndexError
                    while self.loop_ind >= len(self.queue):
                        self.loop_ind -= len(self.queue)
                    song = self.queue[self.loop_ind]
            else:
                song = self.queue[index - 1]
                self.queue = self.queue[index:]
            guildData.updateVoice(self.guild_id, self.loop, self.queue)
            if force:
                return (asyncio.create_task(self.play(song, force)), song)
            await self.play(song)
        except IndexError:
            return (None, None)

    def pause(self) -> bool:
        if not self.is_paused:
            self.is_paused = True
            self.client.pause()
            self.song.pause()

            return True
        else:
            return False

    def seek(self, seek) -> bool:
        if self.ytdlp_Proc:
            if self.ytdlp_Proc.seekable(seek):
                self.client.stop()
                self.ytdlp_Proc.reset()
                self.song.seek(seek)
                self.client.play(discord.FFmpegPCMAudio(source=self.ytdlp_Proc, pipe=True, options=f"-ss {seek}"))
                self.song.play()
                self.is_paused = False

                return True
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
            try:
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
            except IndexError:
                return None
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
        self.cancel = True
        if self.ytdlp_Proc != None:
            self.ytdlp_Proc.terminate()
            self.ytdlp_Proc = None
        if self.guild_id in voiceClient.__voiceClients:
            voiceClient.__voiceClients.pop(self.guild_id)


    __voiceClients = {}

    @staticmethod
    def query(guild_id : int):
        if guild_id in voiceClient.__voiceClients:
            return voiceClient.__voiceClients[guild_id]
        return None

    @staticmethod
    def create(guild_id : int, channel_id : int, client : discord.VoiceClient):
        vc = voiceClient(guild_id, channel_id, client)
        voiceClient.__voiceClients[guild_id] = vc
        return vc

import asyncio, subprocess
import discord
from threading import Thread
from botPath import *
from time import perf_counter

from youtube_search import youtube_search

class Music:
    def __init__(self, start = False, **kwargs) -> None:
        self.name = kwargs['name']
        self.channel = kwargs['channel']
        self.thumb = kwargs['thumb']
        self.id = kwargs['id']
        self.length = kwargs['length']
        
        self.time = perf_counter() if start else None
        self.offset = 0
        self.is_paused = False

    def play(self):
        self.time = perf_counter()
        self.is_paused = False

    def pause(self):
        self.offset += perf_counter() - self.time
        self.is_paused = True

    def seek(self, time):
        if isinstance(time, str):
            timed = time.split(":")
            try:
                time = float(timed[-1])
                time += int(timed[-2]) * 60
                time += int(timed[-3]) * 3600
            except IndexError:
                pass

        self.offset = time

    def toDict(self, plays = None) -> dict:
        if plays:
            return {"name": self.name, "channel": self.channel, "thumb": self.thumb, "id": self.id, "length": self.length, "plays": plays}
        return {"name": self.name, "channel": self.channel, "thumb": self.thumb, "id": self.id, "length": self.length}

    def embed(self, bot : discord.Bot, title = "Now Playing", color = discord.Colour.blue(), timed = False) -> discord.Embed:
        embed = discord.Embed(title=self.name, color=color, url="https://www.youtube.com/watch?v=" + self.id)
        embed.set_thumbnail(url=self.thumb)
        embed.set_author(name=title)
        embed.add_field(name="Channel", value=self.channel)
        if timed:
            cur_length = (perf_counter() - self.time if self.is_paused == False else 0) + self.offset
            embed.add_field(name="Duration", value=self.__humanLength(cur_length) + " / " + self.__humanLength())
        else:
            embed.add_field(name="Duration", value=self.__humanLength())
        embed.set_footer(text="Little Hirishima", icon_url=bot.user.avatar.url)

        return embed
    
    def __humanLength(self, timed = None):
        if timed == None:
            timed = self.length
        else:
            timed = int(timed)

        seconds = timed % 60
        minutes = (timed // 60) % 60
        hours = timed // 3600

        seconds = "0" + str(seconds) if seconds < 10 else str(seconds)

        minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
        minutes += ":"

        hours = str(hours) + ":" if hours > 0 else ""

        return f"{hours}{minutes}{seconds}"


class YoutubeStreamer:
    def __init__(self, ytdlp_proc : subprocess.Popen) -> None:
        self.ytdlp_proc = ytdlp_proc
        self.cursor = 0
        self.size = 0
        self.is_complete = False
        self.buffer = bytearray()
        self.seeked = 0

        Thread(target=self._worker, daemon=True).start()

    def _worker(self) -> None:
        while not self.is_complete:
            data = self.ytdlp_proc.stdout.read(8192)

            if not data:
                break

            self.buffer.extend(data)
            self.size += len(data)

        self.is_complete = True

    def seekable(self, seek) -> bool:
        if seek <= self.seeked:
            return True
        ffm_proc = subprocess.Popen(
            ["ffmpeg", "-ss", str(seek), "-i", "-", "-f", "s16le", "-ar", "48000", "-ac", "2", "-t", "0.001", "-loglevel", "warning", "pipe:1"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        if ffm_proc.communicate(bytes(self.buffer[:self.size]))[0]:
            self.seeked = seek
            return True
        return False 

    def read(self, length) -> bytes:
        while not self.is_complete and self.cursor + length > self.size:
            pass

        data = bytes(self.buffer[self.cursor:self.cursor + length])
        self.cursor += length

        return data

    def reset(self) -> None:
        self.cursor = 0

    def poll(self):
        return self.ytdlp_proc.poll()

    def terminate(self) -> None:
        self.is_complete = True
        self.size = 0
        self.buffer = bytearray()
        return self.ytdlp_proc.terminate()
        
    def __del__(self) -> None:
        self.terminate()


class youtubeQuery:
    result: list[Music]
    length: int
    
    def __init__(self, result : list) -> None:
        self.result = result
        self.length = len(self.result)

    @staticmethod
    async def search(query : str):
        return youtubeQuery([Music(name = i[0], channel = i[1], id = i[2], thumb = i[3], length = i[4]) for i in await youtube_search(query, 25)])

    async def display(self, ctx: discord.ApplicationContext, bot: discord.Bot) -> Music:
        select = discord.ui.Select(select_type=discord.ComponentType.string_select, placeholder="Choose a song")

        for i in range(0, self.length):
            select.add_option(label=self.result[i].name, value=str(i), description=self.result[i].channel)

        message = await ctx.respond(view=discord.ui.View(select, timeout=20), delete_after=20)

        display_lock = asyncio.Event()
        async def sel_respond(interaction : discord.Interaction):
            if interaction.user != ctx.user:
                await ctx.channel.send(f"{interaction.user.mention} Please make your own request using `/play` or `/queue`.", delete_after=6)
            else:
                display_lock.set()

        select.callback = sel_respond

        try:
            await asyncio.wait_for(display_lock.wait(), timeout=20)
            await message.delete()
            output = int(select.values[0])
        except TimeoutError:
            return None
        except ValueError:
            return None

        return self.result[output]

    def get(self, index: int):
        return self.result[index - 1]

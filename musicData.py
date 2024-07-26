import asyncio, io, threading
import discord
from discord.opus import Encoder as OpusEncoder
from botPath import *
from time import time

from youtube_search import youtube_search

class Music:
    def __init__(self, start = False, **kwargs) -> None:
        self.name = kwargs['name']
        self.channel = kwargs['channel']
        self.thumb = kwargs['thumb']
        self.id = kwargs['id']
        self.length = kwargs['length']
        
        self.time = time() if start else None
        self.offset = 0

    def play(self):
        self.time = time()

    def pause(self):
        self.offset += time() - self.time

    def reset(self):
        self.offset = 0

    def embed(self, bot : discord.Bot, title = "Now Playing", color = discord.Colour.blue()) -> discord.Embed:
        embed = discord.Embed(title=self.name, color=color, url="https://www.youtube.com/watch?v=" + self.id)
        embed.set_thumbnail(url=self.thumb)
        embed.set_author(name=title)
        embed.add_field(name="Channel", value=self.channel)
        embed.add_field(name="Duration", value=self.__humanLength())
        embed.set_footer(text="Little Hirishima", icon_url=bot.user.avatar.url)

        return embed
    
    def __humanLength(self):
        seconds = self.length % 60
        minutes = (self.length // 60) % 60
        hours = self.length // 3600

        seconds = "0" + str(seconds) if seconds < 10 else str(seconds)

        minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
        minutes += ":"

        hours = str(hours) + ":" if hours > 0 else ""

        return f"{hours}{minutes}{seconds}"

class musicBuffer(io.BytesIO):
    def __init__(self, stdout : io.BufferedIOBase):
        super().__init__()
        self.stdout = stdout
        self.size = 0
        self.is_complete = False

        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while True:
            data = self.stdout.read(OpusEncoder.FRAME_SIZE)

            if not data:
                break

            self.write(data)
            self.size += len(data)

        self.is_complete = True

    def close(self):
        self.stdout.close()
        super().close()

    def __del__(self) -> None:
        self.stdout.close()
        return super().__del__()

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

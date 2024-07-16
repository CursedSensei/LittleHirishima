import guildData, asyncio, os
import discord
from botPath import *
from time import time

import shutil
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

    def embed(self, bot : discord.Bot, title = "Now Playing") -> discord.Embed:
        embed = discord.Embed(title=self.name, color=discord.Colour.blue(), url="https://www.youtube.com/watch?v=" + self.id)
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


class youtubeQuery:
    result: list[Music]
    length: int
    
    def __init__(self, query : str) -> None:
        self.result = [Music(name = i[0], channel = i[1], id = i[2], thumb = i[3], length = i[4]) for i in youtube_search(query)]
        self.length = len(self.result)

    async def display(self, ctx: discord.ApplicationContext, bot: discord.Bot) -> Music:
        response = "**Choose a song:**\n\n"
        for i in range(0, self.length):
            response += '**' +str(i + 1) + ":** " + self.result[i].name + " *- " + self.result[i].channel + "*" + "\n"

        response = await ctx.respond(response)

        def checker(message: discord.Message):
            try:
                if ctx.author != message.author or ctx.channel != message.channel:
                    raise ValueError
                self.result[int(message.content) - 1]
            except ValueError:
                return False
            except IndexError:
                return False
            return True

        try:
            message = await bot.wait_for('message', check=checker, timeout=20)
        except asyncio.TimeoutError:
            await response.delete()
            return None
        
        await response.delete()
        await message.delete()

        return self.result[int(message.content) - 1]

    def get(self, index: int):
        return self.result[index - 1]

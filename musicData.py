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
    
    def __init__(self, result : list) -> None:
        self.result = result
        self.length = len(self.result)

    @staticmethod
    async def search(query : str):
        return youtubeQuery([Music(name = i[0], channel = i[1], id = i[2], thumb = i[3], length = i[4]) for i in await youtube_search(query)])

    async def display(self, ctx: discord.ApplicationContext, bot: discord.Bot) -> Music:
        response = []

        embed = discord.Embed(title="", color=discord.Colour.blue())
        embed.set_author(name="Choose a song")
        embed.add_field(name="#", value="")
        embed.add_field(name="Name", value="")
        embed.add_field(name="Channel", value="")
        embed.add_field(name="", value="", inline=False)

        for i in range(0, self.length):
            if i != 0 and i % 5 == 0:
                response.append(await ctx.respond(embed=embed))
                embed.clear_fields()
                embed.set_author(name="")
            embed.add_field(name="", value=str(i + 1))
            embed.add_field(name="", value=f"[{self.result[i].name}](https://www.youtube.com/watch?v={self.result[i].id})")
            embed.add_field(name="", value=self.result[i].channel)
            embed.add_field(name="", value="", inline=False)

        embed.set_footer(text=f"Requested by: {ctx.author.nick}", icon_url=ctx.author.avatar.url)
        response.append(await ctx.respond(embed=embed))

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
            for i in response:
                asyncio.create_task(i.delete())
            return None
        
        for i in response:
            asyncio.create_task(i.delete())
        asyncio.create_task(message.delete())

        return self.result[int(message.content) - 1]

    def get(self, index: int):
        return self.result[index - 1]

import botPath
from voiceClient import *
import musicData
import botControl
from guildData import updateVoice, loadGuilds, updateGuilds
from botConst import *

import json, asyncio
import discord
from re import match
from discord.ext import commands
from discord import VoiceChannel
from aiohttp.client_exceptions import ClientConnectorError

#import logging
#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S'
#)
#
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#
#handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

try:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = commands.Bot(intents=intents)

    botControl.initializeAdmin(client)

    @client.event
    async def on_ready():
        print("Little Hirishima is now connected!")

        await loadGuilds(client)

    @client.event
    async def on_guild_join(guild : discord.Guild):
        updateGuilds(add=guild)

    @client.event
    async def on_guild_remove(guild : discord.Guild):
        updateGuilds(remove=guild)



    @client.event
    async def on_voice_state_update(author : discord.Member, before_vcstate : discord.VoiceState, after_vcstate : discord.VoiceState):
        if before_vcstate.channel == None:
            return
        elif author == client.user:
            if after_vcstate.channel == None:
                return
            elif before_vcstate.channel != after_vcstate.channel:
                vClient = voiceClient.query(before_vcstate.channel.guild.id)
                if vClient != None and vClient.is_initialized:
                    await vClient.disconnect()
        elif len(before_vcstate.channel.members) == 1 and before_vcstate.channel.members[0] == client.user:
            vClient = voiceClient.query(before_vcstate.channel.guild.id)
            if vClient != None and vClient.is_initialized:
                await vClient.disconnect()


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
        vChannel: VoiceChannel = ctx.author.voice.channel

        if vClient == None:
            try:
                await voiceClient.create(ctx.guild_id, vChannel.id, vChannel)
            except:
                await ctx.respond("Bot failed to connect", delete_after=6)
                return
            await ctx.respond(f"Bot is connected to {vChannel.mention}")
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
            if vClient.is_initialized == False:
                await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
                return

            await vClient.disconnect()

            await ctx.respond(f"Bot successfully disconnected from {vChannel.mention}")
        else:
            await ctx.respond("You are not connected to the Bot's voice channel", delete_after=3)

    @client.slash_command(name='play', description="Plays a song. If paused, resumes the song.")
    async def play(ctx: discord.ApplicationContext, query: discord.Option(str, "Song to search from youtube", required=False)):
        if not await userInVoice(ctx):
            return

        if query:
            await ctx.defer()
            result = await musicData.youtubeQuery.search(query)

            if result.length == 0:
                await ctx.respond(f"No results for \"{query}\"", delete_after=3)
                return
            
            if match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', query):
                song = result.get(1)
            else:
                song = await result.display(ctx, client)

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
            try:
                vClient = await voiceClient.create(ctx.guild_id, vChannel.id, vChannel)
            except:
                await ctx.respond("Bot failed to connect", delete_after=6)
                return
        elif vClient.channel_id != vChannel.id:
            await ctx.respond("You must be connected with the bot's channel to play music", delete_after=3)
            return
        elif vClient.is_initialized == False:
            await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
            return
        
        if not query:
            if vClient.unpause():
                await ctx.respond("Bot is unpaused")
            else:
                await ctx.respond("Bot is already unpaused", delete_after=6)
        else:
            song_mes = asyncio.create_task(ctx.respond(embed = song.embed(client, title = "Song to play", color=discord.Colour.orange())))
            
            if await vClient.play(song, force = True):
                song_mes = await song_mes
                if vClient.loop == REPEAT_QUEUE:
                    await song_mes.edit(embed = song.embed(client, title = f"Now Playing (#{vClient.loop_ind + 2} in Queue)"))
                    vClient.loop_ind += 1
                    vClient.queue.insert(vClient.loop_ind, song)
                    updateVoice(vClient.guild_id, vClient.loop, vClient.queue)
                else:
                    await song_mes.edit(embed = song.embed(client))
            else:
                await (await song_mes).edit(embed = song.embed(client, title = "Song Cancelled", color=discord.Colour.red()))

    @client.slash_command(name='queue', description="Add, remove, or list songs in queue")
    async def queue(ctx: discord.ApplicationContext, query: discord.Option(str, "Add song from youtube to queue", required=False),
            remove: discord.Option(str, 'Remove a song from queue. type "all" to remove all songs in queue', required=False,)):
        await ctx.defer()
        if query:
            result = await musicData.youtubeQuery.search(query)

            if result.length == 0:
                await ctx.respond(f"No results for \"{query}\"", delete_after=3)
                return
            
            if match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', query):
                song = result.get(1)
            else:
                song = await result.display(ctx, client)

            if song == None:
                return
            
            position = voiceClient.queueGuild(ctx.guild_id, add=song)

            if position:
                await ctx.respond(embed = song.embed(client, f"Song added to queue (#{position})"))
        elif remove:
            try:
                if remove == "all":
                    voiceClient.queueGuild(ctx.guild_id, remove=remove)
                    await ctx.respond("Removed all queued songs")
                else:
                    song = voiceClient.queueGuild(ctx.guild_id, remove=int(remove) - 1)
                    if song:
                        await ctx.respond(embed = song.embed(client, "Song removed from queue"))
                    else:
                        await ctx.respond('Song not found. To remove queued song, input the index of the song ("2" for the second song) or "all" to remove all queued songs', delete_after=10)
            except ValueError:
                await ctx.respond('Invalid. To remove queued song, input the index of the song ("2" for the second song) or "all" to remove all queued songs', delete_after=10)
        else:
            songs = voiceClient.queueGuild(ctx.guild_id)
            if len(songs) == 0:
                await ctx.respond("No songs in queue", delete_after=10)
            else:
                embed = discord.Embed(title="", color=discord.Colour.blue())
                embed.set_author(name="Songs in queue")
                embed.add_field(name="#", value="")
                embed.add_field(name="Name", value="")
                embed.add_field(name="Channel", value="")
                embed.add_field(name="", value="", inline=False)

                for i in range(0, len(songs)):
                    if i != 0 and i % 5 == 0:
                        await ctx.respond(embed=embed)
                        embed.clear_fields()
                        embed.set_author(name="")
                    embed.add_field(name="", value=str(i + 1))
                    embed.add_field(name="", value=f"[{songs[i].name}](https://www.youtube.com/watch?v={songs[i].id})")
                    embed.add_field(name="", value=songs[i].channel)
                    embed.add_field(name="", value="", inline=False)

                embed.set_footer(text="Little Hirishima", icon_url=client.user.avatar.url)
                await ctx.respond(embed=embed)


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
        elif vClient.is_initialized == False:
            await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
            return

        if vClient.pause():
            await ctx.respond("Bot is paused")
        else:
            await ctx.respond("Bot is already paused", delete_after=6)

    @client.slash_command(name='loop', description="Switch between three loop modes")
    async def loop(ctx: discord.ApplicationContext):
        await ctx.respond(voiceClient.loopState(ctx.guild_id))

    @client.slash_command(name='next', description="Plays next in queue")
    async def next(ctx: discord.ApplicationContext, index: discord.Option(int, "Index of song in queue to play next", required=False)):
        if index and index <= 0:
            await ctx.respond("Incorrect index format", delete_after=3)
            return

        vClient = voiceClient.query(ctx.guild_id)
        if vClient:
            if vClient.is_initialized == False:
                await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
                return

            await ctx.defer()

            if index:
                taskPlay, song = await vClient.next(index, force = True)
            else:
                taskPlay, song = await vClient.next(vClient.loop_ind + 2 if vClient.loop == REPEAT_QUEUE and len(vClient.queue) >= vClient.loop_ind + 2 else 1, force = True)

            if song:
                song_mes = asyncio.create_task(ctx.respond(embed = song.embed(client, title = "Next song in queue", color=discord.Colour.orange())))
                if await taskPlay:
                    song_mes = await song_mes
                    if vClient.loop == REPEAT_QUEUE:
                        await song_mes.edit(embed = song.embed(client, title = f"Now Playing (#{vClient.loop_ind + 2} in Queue)"))
                    else:
                        await song_mes.edit(embed = song.embed(client))
                else:
                    await (await song_mes).edit(embed = song.embed(client, title = "Song Cancelled", color=discord.Colour.red()))
            else:
                await ctx.respond("No song found in queue", delete_after=6)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='playing', description="Show what song is being played")
    async def playing(ctx: discord.ApplicationContext):
        vClient = voiceClient.query(ctx.guild_id)
        if vClient:
            if vClient.is_initialized == False:
                await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
                return

            if vClient.song == None:
                await ctx.respond("No song is currently played", delete_after=6)
            else:
                if vClient.loop == REPEAT_QUEUE:
                    await ctx.respond(embed = vClient.song.embed(client, title = f"Now Playing (#{vClient.loop_ind + 1} in Queue)", timed = True))
                else:
                    await ctx.respond(embed = vClient.song.embed(client, timed = True))
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='seek', description="Seek to specified timestamp of song")
    async def seek(ctx: discord.ApplicationContext, timestamp: discord.Option(str, "Timestamp to seek", required=True)):
        timed = timestamp.split(":")
        try:
            timestamp = float(timed[-1])
            timestamp += int(timed[-2]) * 60
            timestamp += int(timed[-3]) * 3600

            if timestamp < 0:
                raise ValueError
        except IndexError:
            pass
        except ValueError:
            await ctx.respond("The inputted timestamp is invalid", delete_after=6)
            return

        vClient = voiceClient.query(ctx.guild_id)
        if vClient:
            if vClient.is_initialized == False:
                await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
                return

            await ctx.defer()
            if vClient.song == None:
                await ctx.respond("No song is currently played", delete_after=6)
            else:
                if vClient.seek(timestamp):
                    await ctx.respond(embed = vClient.song.embed(client, timed = True))
                else:
                    await ctx.respond("The inputted timestamp is not in range or currently not yet available.", delete_after=6)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='shuffle', description="Shuffle the current queue")
    async def shuffle(ctx: discord.ApplicationContext):
        await ctx.defer()
        if voiceClient.queueGuild(ctx.guild_id, shuffle=True):
            await ctx.respond("Current queue successfully shuffled")
        else:
            await ctx.respond("There is no queue to shuffle", delete_after=6)

    @client.slash_command(name='replay', description="Replay the song currently played")
    async def replay(ctx: discord.ApplicationContext):
        vClient = voiceClient.query(ctx.guild_id)
        if vClient:
            if vClient.is_initialized == False:
                await ctx.respond("Bot is still connecting. Try again later", delete_after=6)
                return

            if vClient.song == None:
                await ctx.respond("No song is currently played", delete_after=6)
            else:
                await vClient.play(True)
                await ctx.respond(embed = vClient.song.embed(client, timed = True))
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    with open(botPath.TOKENPATH, "r") as f:
        TOKEN = json.load(f)['TOKEN']

    client.run(TOKEN)
except RuntimeError:
    pass
except ClientConnectorError:
    import time, os

    time.sleep(10)
    #subprocess.Popen([sys.executable, os.path.abspath(__file__)], start_new_session = True)
    os.system(f'tmux send-keys -t "little_hirishima:0" C-m "{sys.executable} {botPath.MAINFILEPATH}" C-m')
except:
    import traceback
    with open(botPath.ERRORPATH,"w") as f:
        f.write(traceback.format_exc())
    print("[ERROR] " + traceback.format_exc())

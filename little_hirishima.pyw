import botPath
from voiceClient import *
import musicData
import botControl

import json
import discord
from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError

try:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = commands.Bot(intents=intents)

    botControl.initializeAdmin(client)

    @client.event
    async def on_voice_state_update(author : discord.Member, before_vcstate : discord.VoiceState, after_vcstate : discord.VoiceState):
        if before_vcstate.channel == None:
            return
        elif author == client.user:
            if after_vcstate.channel == None:
                return
            elif before_vcstate.channel != after_vcstate.channel:
                vClient = voiceClient.query(before_vcstate.channel.guild.id)
                if vClient != None:
                    await vClient.disconnect()
        elif len(before_vcstate.channel.members) == 1 and before_vcstate.channel.members[0] == client.user:
            vClient = voiceClient.query(before_vcstate.channel.guild.id)
            if vClient != None:
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
            await vClient.disconnect()

            await ctx.respond("Bot successfully disconnected", delete_after=6)
        else:
            await ctx.respond("You are not connected to the Bot's voice channel", delete_after=3)

    @client.slash_command(name='play', description="Plays a song. If paused, resumes the song.")
    async def play(ctx: discord.ApplicationContext, query: discord.Option(str, "Song to search from youtube", required=False)):
        if not await userInVoice(ctx):
            return

        if query:
            await ctx.defer()
            result = musicData.youtubeQuery(query)

            if result.length == 0:
                await ctx.respond(f"No results for \"{query}\"", delete_after=3)
                return
            
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
            vClient = voiceClient.create(ctx.guild_id, vChannel.id, await vChannel.connect(), client)
        elif vClient.channel_id != vChannel.id:
            await ctx.respond("You must be connected with the bot's channel to play music", delete_after=3)
            return
        
        if not query:
            if vClient.unpause():
                await ctx.respond("Bot is unpaused")
            else:
                await ctx.respond("Bot is already unpaused", delete_after=6)
        else:
            if await vClient.play(song):
                await ctx.respond(embed = song.embed(client))
            else:
                await ctx.respond("A song is already being loaded. Please wait", delete_after=6)

    @client.slash_command(name='queue', description="Add, remove, or list songs in queue")
    async def queue(ctx: discord.ApplicationContext, query: discord.Option(str, "Add song from youtube to queue", required=False),
            remove: discord.Option(str, 'Remove a song from queue. type "all" to remove all songs in queue', required=False,)):
        await ctx.defer()
        if query:
            result = musicData.youtubeQuery(query)

            if result.length == 0:
                await ctx.respond(f"No results for \"{query}\"", delete_after=3)
                return
            
            song = await result.display(ctx, client)
            if song == None:
                return
            
            if voiceClient.queueGuild(ctx.guild_id, add=song):
                await ctx.respond(embed = song.embed(client, "Song added to queue"))
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

        if vClient.pause():
            await ctx.respond("Bot is paused")
        else:
            await ctx.respond("Bot is already paused", delete_after=6)

    @client.slash_command(name='loop', description="Change mode for loop")
    async def loop(ctx: discord.ApplicationContext):
        await ctx.respond(voiceClient.loopState(ctx.guild_id))

    @client.slash_command(name='next', description="Plays next in queue")
    async def next(ctx: discord.ApplicationContext, number: discord.Option(int, "Number of songs to skip in queue", required=False)):
        if number and number <= 0:
            await ctx.respond("Incorrect number format", delete_after=3)
            return

        vClient = voiceClient.query(ctx.guild_id)
        if vClient:
            await ctx.defer()
            song = await vClient.next(1 if not number else number)
            if song:
                await ctx.respond(embed = song.embed(client))
            elif song == False:
                await ctx.respond("A song is already being loaded. Please wait", delete_after=6)
            else:
                await ctx.respond("No song found in queue", delete_after=6)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    with open(botPath.TOKENPATH, "r") as f:
        TOKEN = json.load(f)['TOKEN']

    client.run(TOKEN)
except RuntimeError:
    pass
except ClientConnectorError:
    import subprocess, time, os

    time.sleep(10)
    subprocess.Popen(f"python3 {os.path.abspath(__file__)}", start_new_session = True, shell = True)
except:
    import traceback
    with open(botPath.ERRORPATH,"w") as f:
        f.write(traceback.format_exc())
    print("[ERROR] " + traceback.format_exc())

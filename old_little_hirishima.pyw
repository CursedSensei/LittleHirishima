import os,random,time,threading,subprocess,asyncio,sys,json,shutil
 
# ADDITIONAL FEATURE
# add database for each member's playlist, add view buttons

class variables:
    class weapons:
        vstar = ["Lost Prayer of the Sacred Winds","Freedom Sworn",
        "Primorial Jade Spear","Primorial Jade Cutter","Wolf's Gravestone",
        "Aquila Favonia","Skyward Pride","Skyward Harp","Skyward Sword",
        "Skyward Atlas","Amos' Bow","Aqua Simulacra","Calamity Queller",
        "Elegy of the End","Engulfing Lightning","Everlasting Moonglow",
        "Haran Geppaku Futsu","Kagura's Verity","Memory of Dust",
        "Mistplitter Reforged","Polar Star","Skyward Spine",
        "Song of Broken Pines","Staff of Homa","Summit Shaper",
        "The Unforged","Thundering Pusle","Vortex Vanquisher",
        "Redhorn Stonethresher"]

        ivstar = ["Favonius Sword","Iron Sting","Kagostsurube Isshin",
        "Lion's Roar","Sacrificial Sword",
        "The Alley Flash","The Flute",
        "Akuomaru","Favonius Greatsword",
        "Lithic Blade","Rainslasher",
        "Sacrificial Greatsword",
        "The Bell","Whiteblind",
        "Eye of Perception","Favonius Codex",
        "Sacrificial Fragments","The Widsith",
        "Wine and Song",
        "Favonius Lance","Lithic Spear",
        "Wavebreaker's Fin",
        "Fading Twighlight","Alley Hunter",
        "Favonius Warbow","Miiternachts Waltz","Mouun's Moon",
        "Rust","Sacrificial Bow","The Stringless",
        "The Viridescent Hunt"]

        iiistar = ["Cool Steel","Dark Iron Sword","Fillet Blade","Harbinger or Dawn",
        "Travler's Handy Sword","Bloodtainted Greatsword","Debate Club","Ferrous Shadow",
        "Skyrider Greatsword","White Iron Greatsword","Emerald Orb","Magic Guide",
        "Otherworldly Story","Thrilling Tales of Dragon Slayers","Twin Nephrite",
        "Black Tassle","Halberd","White Tassle","Messenger","Raven Bow","Recurve Bow",
        "Sharpshooter's Oath","Slingshot"]

    class characters:
        vstar = ["Diluc","Qiqi","Jean","Mona","Keqing","Venti","Kazuha",
        "Xiao","Zhongli","Klee","Ayaka","Hu Tao","Ayato","Yoimiya","Shenhe",
        "Childe","Raiden Shogun","Albedo","Aloy","Eula","Itto","Kokomi","Yelan","Yae Miko"]

        ivstar = ["Heizou","Bennett","Amber","Lisa","Fischl","Kuki Shinobu","Kaeya",
        "Barbara","Razor","Noelle","Sucrose","Beidou","Xiangling","Xingqiu","Chongyun",
        "Diona","Xinyan","Rosaria","Sayu","Kujo Sara","Gorou","Thoma","Yun Jin"]

    class non_obtainables:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        gachadata = os.path.join(ROOT_DIR, 'lib/gachadata.cfg')
        bufferdirectory = "/var/www/html/Anime"
        downloadbuffer = os.path.join(ROOT_DIR, 'lib/urldown.py')

sys.path.append(os.path.join(variables.non_obtainables.ROOT_DIR,'lib/lib'))
import discord, mutagen
from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError
from youtube_search import youtube_search

class gacha:
    def __init__(self):
        if not os.path.exists(variables.non_obtainables.gachadata):
            with open(variables.non_obtainables.gachadata, "w+") as data_create:
                data_create.write("Deleting this file will reset the probability for 5-star (using arknight's probability).\n\n0.005\n0")

    def get_rarity(self):
        all_rarity = ["3-star","4-star","5-star"]
        with open(variables.non_obtainables.gachadata, "r") as rawfive_rarity:
            five_rarity = float(rawfive_rarity.readlines()[2])
        with open(variables.non_obtainables.gachadata, "r") as raw_all_rolls:
            all_rolls = int("".join([str(item) for item in raw_all_rolls.readlines()[3:]]))
        rawrarity = random.choices(all_rarity, [0.38, 0.089, five_rarity])
        rarity =''.join([str(item) for item in rawrarity])
        if rarity != "5-star":
            if all_rolls >= 50:
                five_rarity += 0.05
                writefive_rarity = str(five_rarity)
                with open(variables.non_obtainables.gachadata, "w") as writefive_rarity_raw:
                    writefive_rarity_raw.write(f"Deleting this file will reset the probability for 5-star (using arknight's probability).\n\n{writefive_rarity}\n1")
            else:
                all_rolls += 1
                with open(variables.non_obtainables.gachadata, "w") as writeall_rolls_raw:
                    writefive_rarity = str(five_rarity)
                    writeall_rolls = str(all_rolls)
                    writeall_rolls_raw.write(f"Deleting this file will reset the probability for 5-star (using arknight's probability).\n\n{five_rarity}\n{writeall_rolls}")
        else:
            with open(variables.non_obtainables.gachadata, "w") as writefive_rarity_raw:
                writefive_rarity_raw.write(f"Deleting this file will reset the probability for 5-star (using arknight's probability).\n\n0.005\n0")
        return rarity

    def roll(self):
        class randomizer:
            randomized_weapons_vstar = random.choice(variables.weapons.vstar)
            randomized_characters_vstar = random.choice(variables.characters.vstar)
            randomized_weapons_ivstar = random.choice(variables.weapons.ivstar)
            randomized_characters_ivstar = random.choice(variables.characters.ivstar)
            randomized_weapons_iiistar = random.choice(variables.weapons.iiistar)
            types = random.randint(1,2)
            rarity = self.get_rarity()
        if randomizer.rarity == "5-star":
            if randomizer.types == 1:
                rollgot = f"```css\n[You received a 5-star weapon {randomizer.randomized_weapons_vstar}]\n```\n"
            else:
                rollgot = f"```css\n[You received a 5-star character {randomizer.randomized_characters_vstar}]\n```\n"
        elif randomizer.rarity == "4-star":
            if randomizer.types == 1:
                rollgot = f"```fix\n[You received a 4-star weapon {randomizer.randomized_weapons_ivstar}]\n```\n"
            else:
                rollgot = f"```fix\n[You received a 4-star character {randomizer.randomized_characters_ivstar}]\n```\n"
        else:
            rollgot = f"```ini\n[You received a 3-star weapon {randomizer.randomized_weapons_iiistar}]\n```\n"
        return rollgot

    def ten_roll(self):
        response = self.roll()
        for i in range(0, 9):
            response = f"{response}{self.roll()}"
        return response

class GuildMessages:
    def __init__(self, GuildId):
        self.queue = [None]
        self.list = [None]

    async def move(self, message, nextPage = False):
        if self.queue[0] and self.queue[0].id == message.id:
            if (not nextPage and self.queue[2] == 1) or (nextPage and len(self.queue[1]) <= 20 * self.queue[2]):
                return

            if nextPage:
                self.queue[2] += 1
            else:
                self.queue[2] -= 1
            start = self.queue[2]

            songs = self.queue[1][20 * (start - 1):20 * start]

            init = "queue"

        else:
            if (not nextPage and self.list[2] == 1) or (nextPage and len(self.list[1]) <= 20 * self.list[2]):
                return
            
            if nextPage:
                self.list[2] += 1
            else:
                self.list[2] -= 1
            start = self.list[2]

            songs = self.list[1][20 * (start - 1):20 * start]

            init = "library"

        await message.edit(embed=self.embed(init, songs, start))

    async def setList(self, channel):
        if self.list[0]:
            try:
                await self.list[0].delete()
            except:
                pass

        songs = Music.getMusicLib()
        self.list = [await channel.respond(embed=self.embed("library", songs if len(songs) <= 20 else songs[0:20])),
            songs, 1]

        if len(songs) > 20:
            await self.list[0].add_reaction("⬅️")
            await self.list[0].add_reaction("➡️")

    async def setQueue(self, channel, songs):
        if self.queue[0]:
            try:
                await self.queue[0].delete()
            except:
                pass

        self.queue = [await channel.respond(embed=self.embed("queue", songs if len(songs) <= 20 else songs[0:20])),
            songs, 1]

        if len(songs) > 20:
            await self.queue[0].add_reaction("⬅️")
            await self.queue[0].add_reaction("➡️")

    async def removeQueue(self):
        if self.queue[0]:
            try:
                await self.queue[0].delete()
            except:
                pass
            self.queue = [None]

    def embed(self, init, songs, start = 1):
        start = 20 * start - 19

        embed = discord.Embed(title=f"**List of songs in {init}:**", description="\u200B")
        embed.colour = discord.Colour.dark_purple()
        for i in range(0, len(songs)):
            embed.add_field(name="", value=f"**{i + start}:** {songs[i] if type(songs[i]) != tuple else songs[i][1]}", inline=False)
        return embed

    @staticmethod
    async def purge():
        for i in guild_message:
            await guild_message[i].removeQueue()
            if guild_message[i].list[0]:
                await guild_message[i].list[0].delete()

    @staticmethod
    def getGuildMessages(GuildId, message = None):
        if not GuildId in guild_message:
            if message != None:
                raise TypeError("Message not found!")
            guild_message[GuildId] = GuildMessages(GuildId)
        if message != None:
            if not ((guild_message[GuildId].queue[0] and guild_message[GuildId].queue[0].id == message.id) or (guild_message[GuildId].list[0] and guild_message[GuildId].list[0].id == message.id)):
                raise TypeError("Message not found!")
        return guild_message[GuildId]

class GuildClient:
    def __init__(self, GuildId):
        self.thread = threading.Thread()
        self.song = None
        self.id = GuildId
        self.queue, self.loop = self.read()
        self.order = 0
        self.channel = False
        self.client = None

    async def connect(self, channel):
        self.channel = channel
        self.client = await channel.connect()
        asyncio.run_coroutine_threadsafe(self.worker(), client.loop)

    def play(self, mode=False, threaded = False):
        if self.thread.is_alive() and threaded == False:
            return False
        srcPath = os.path.join(variables.non_obtainables.ROOT_DIR, "lib/Song_Library") + "/"
        download = False
        if not mode:
            song = random.choice(Music.getMusicLib())
        elif type(mode) == tuple:
            srcPath = os.path.join(variables.non_obtainables.ROOT_DIR, "lib/Cache") + "/"

            if os.path.exists(srcPath + str(self.id) + 'raw.part'):
                os.remove(srcPath + str(self.id) + 'raw.part')
            if os.path.exists(srcPath + str(self.id) + 'raw.ytdl'):
                os.remove(srcPath + str(self.id) + 'raw.ytdl')
            if os.path.exists(srcPath + str(self.id) + 'raw.mp3'):
                os.remove(srcPath + str(self.id) + 'raw.mp3')

            subprocess.run(f'/usr/local/bin/yt-dlp -f mp3/bestaudio/best -x --audio-format mp3 -o "{srcPath}{self.id}raw" {mode[0]}', shell = True)

            download = True
            song = str(self.id) + '.mp3'
        else:
            for item in Music.getMusicLib():
                if mode in item:
                    song = item
                    break
        if self.client.is_playing():
            self.client.stop()
        if download:
            if os.path.exists(srcPath + song):
                while True:
                    try:
                        os.remove(srcPath + song)
                        break
                    except PermissionError:
                        time.sleep(0.3)
            os.rename(srcPath + str(self.id) + 'raw.mp3', srcPath + song)
        srcPath += song
        self.client.play(discord.FFmpegPCMAudio(source=srcPath))
        if srcPath.split("/")[-2] == "Song_Library":
            song = song.split(".")
            song.pop(-1)
            song = ".".join(song)
        else:
            song = mode[1]
        self.song = Music(song, srcPath, mode)
        return song

    async def youtube(self, mode):
        if self.thread.is_alive():
            return False
        self.thread = threading.Thread(target=self.play, args=[mode, True], daemon=True)
        self.thread.start()
        while self.thread.is_alive():
            await asyncio.sleep(0.3)
        return True

    async def worker(self):
        while self.client.is_connected():
            try:
                if not (self.client.is_playing() or self.client.is_paused()):
                    if not (self.thread.is_alive() or self.client.is_playing()):
                        self.song = None
                        if self.loop == 2:
                            await self.next()
                        elif self.loop == 3:
                            self.song.repeat()
                        elif not await self.next():
                            if self.loop == 1:
                                self.play()
            except Exception as e:
                with open(os.path.join(variables.non_obtainables.ROOT_DIR, "WorkerCrash.txt"), "w") as w:
                    w.write(str(e))

            await asyncio.sleep(0.3)
        self.cleanup()

    async def next(self):
        if self.queue == []:
            return False
        if self.loop == 2:
            self.order += 1
            index = self.order
        else:
            index = 0
        while True:
            try:
                if type(self.queue[index]) == tuple:
                    if not await self.youtube(self.queue[index]):
                        return 2
                else:
                    self.play(self.queue[index])
                if not self.loop == 2:
                    self.queue.pop(0)
                    self.write()
                return self.song.name
            except IndexError:
                self.order = 0
                index = 0

    def append(self, song):
        self.queue.append(song)
        self.write()

    def remove(self, index):
        if index <= self.order:
            if self.order != 0:
                self.order -= 1
        song = self.queue.pop(index)
        self.write()
        if type(song) == tuple:
            song = song[1]
        return song

    def purge(self):
        self.queue = []
        try:
            os.remove(os.path.join(variables.non_obtainables.ROOT_DIR, f"lib/Queues/{self.id}.json"))
        except FileNotFoundError:
            return

    def mode(self):
        if self.loop == 0:
            self.loop = 1
            return "Bot will randomly choose a song from library after this song or queue."
        elif self.loop == 1:
            self.loop = 2
            self.order = 0
            if self.song:
                self.queue = [self.song.mode] + self.queue
            else:
                self.queue = self.queue
            return "Bot will repeat songs in queue."
        elif self.loop == 2:
            self.loop = 3
            return "Bot will repeat current song."
        elif self.loop == 3:
            self.loop = 0
            return "Bot will not do anything after this song or this queue."

    def resume(self):
        self.client.resume()
        self.song.play()

    def pause(self):
        self.client.pause()
        self.song.pause()

    async def disconnect(self):
        await self.client.disconnect()
        self.cleanup()

    def read(self):
        if os.path.exists(os.path.join(variables.non_obtainables.ROOT_DIR, f"lib/Queues/{self.id}.json")):
            with open(os.path.join(variables.non_obtainables.ROOT_DIR, f"lib/Queues/{self.id}.json"), "r") as r:
                songs = json.load(r)
            try:
                for i in range(0, len(songs) - 1):
                    if type(songs[i]) != str:
                        songs[i] = tuple(songs[i])
                loop = songs.pop(-1)
            except TypeError:
                songs = [songs]
                loop = songs
            return (songs, loop)
        return ([], 0)

    def write(self):
        if self.queue:
            with open(os.path.join(variables.non_obtainables.ROOT_DIR, f"lib/Queues/{self.id}.json"), "w") as w:
                json.dump(self.queue + [self.loop], w)
        else:
            with open(os.path.join(variables.non_obtainables.ROOT_DIR, f"lib/Queues/{self.id}.json"), "w") as w:
                json.dump(self.loop, w)

    def cleanup(self):
        try:
            if self.id == 754517440154828901:
                guild_data[self.id] = guild_data[self.id] = GuildClient(self.id)
            else:
                guild_data.pop(self.id)
        except KeyError:
            pass
        if os.path.exists(os.path.join(os.path.join(variables.non_obtainables.ROOT_DIR, "lib/Cache"), f"{self.id}.mp3")):
            try:
                os.remove(os.path.join(os.path.join(variables.non_obtainables.ROOT_DIR, "lib/Cache"), f"{self.id}.mp3"))
            except PermissionError:
                pass

    @staticmethod
    async def getGuildClient(GuildId, channel=None, checkonly=False, no_connect = False):
        if GuildId in guild_data:
            if no_connect:
                pass
            elif guild_data[GuildId].channel == channel:
                return 1
            elif channel != None:
                if guild_data[GuildId].client == None:
                    await guild_data[GuildId].connect(channel)
                else:
                    await guild_data[GuildId].client.move_to(channel)
                    guild_data[GuildId].channel = channel
            elif not no_connect and guild_data[GuildId].client == None:
                return None
        else:
            if no_connect:
                guild_data[GuildId] = GuildClient(GuildId)
            elif channel == None or checkonly == True:
                return None
            else:
                guild_data[GuildId] = GuildClient(GuildId)
                await guild_data[GuildId].connect(channel)
        return guild_data[GuildId]

    @staticmethod
    async def dedicatedWorker(message):
        def play_field(guildClient):
            if guildClient.song:
                length = guildClient.song.getLength().split("\n")[-1]
                return f'{guildClient.song.name}\n\n{length}'
            else:
                if guildClient.thread.is_alive():
                    return "Song currently being loaded"
                return "There is no song currently played"

        def queue_field(songs):
            if songs == []:
                return "No songs queued"
            elif len(songs) > 5:
                songs = songs[0:5]
            value = ""
            for i in range(0, len(songs)):
                value += f"{i + 1}: {songs[i][1] if type(songs[i]) == tuple else songs[i]}\n"
            return value[:-1]

        def mode_field(mode):
            if mode == 1:
                return "Bot will randomly choose a song from library after this song or queue."
            elif mode == 2:
                return "Bot will repeat songs in queue."
            elif mode == 3:
                return "Bot will repeat current song."
            elif mode == 0:
                return "Bot will not do anything after this song or this queue."

        embed = discord.Embed(title=f"**{message.guild.name}**", description="\u200B")
        embed.colour = discord.Colour.dark_purple()
        while True:
            embed.clear_fields()
            if message.guild.id in guild_data:
                embed.add_field(name="**Playing:**", value=play_field(guild_data[message.guild.id]), inline=False)
                embed.add_field(name="**Queue:**", value=queue_field(guild_data[message.guild.id].queue), inline=False)
                embed.add_field(name="**Mode:**", value=mode_field(guild_data[message.guild.id].loop), inline=False)
            else:
                embed.add_field(name="**Playing:**", value="There is no song currently played", inline=False)
                embed.add_field(name="**Queue:**", value="No songs queued", inline=False)
                embed.add_field(name="**Mode:**", value="N/A", inline=False)
            try:
                await message.edit(embed=embed)
            except Exception as e:
                print(f"dedicatedWorker Raised: {e}")
            await asyncio.sleep(0.5)

class Music:
    def __init__(self, name, path, raw):
        self.stime = time.time()
        self.dtime = 0
        self.name = name
        self.path = path
        if raw == False:
            self.mode = path.split("/")[-1]
        else:
            self.mode = raw

    def pause(self):
        self.dtime = time.time() - self.stime
        self.stime = 0

    def play(self):
        self.stime = time.time()

    def repeat(self, client):
        client.play(discord.FFmpegPCMAudio(source=self.path))
        self.stime = time.time()
        self.dtime = 0

    def getLength(self):
        songLength = int(mutagen.File(self.path).info.length)
        if self.stime == 0:
            curtime = 0
        else:
            curtime = time.time() - self.stime
        curtime += self.dtime
        scurtime = int(curtime) % 60 if (int(curtime) % 60) > 9 else "0" + str(int(curtime) % 60)
        ssongLength = songLength % 60 if (songLength % 60) > 9 else "0" + str(songLength % 60)

        return "{}\n\n{}:{} / {}:{}".format(self.name, int(curtime) // 60, scurtime, songLength // 60, ssongLength)

    @staticmethod
    def getMusicLib():
        names = []
        for file in os.listdir(os.path.join(variables.non_obtainables.ROOT_DIR, "lib/Song_Library")):
            if file.endswith(".mp3") or file.endswith(".flac"):
                names.append(file)
        return names

    @staticmethod
    def music_search(name):
        songset = []
        for song in Music.getMusicLib():
            if name.lower() in song.lower():
                song = song.split(".")
                song.pop(-1)
                songset.append(".".join(song))
        return songset

try:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    guild_data = {}
    guild_message = {}

    client = commands.Bot(intents=intents)

    @client.event
    async def on_ready():
        print("[INFO]: Little Hirishima is now connected!")

        channel = await client.fetch_channel(1145714516554948668)
        await GuildClient.getGuildClient(channel.guild.id, no_connect = True)
        asyncio.run_coroutine_threadsafe(GuildClient.dedicatedWorker(await channel.fetch_message(1146389053944647790)), client.loop)

    @client.event
    async def on_voice_state_update(author, before_vcstate, after_vcstate):
        if before_vcstate.channel == None:
            return
        if author == client.user:
            if after_vcstate.channel == None:
                return
            elif before_vcstate.channel != after_vcstate.channel:
                state = await GuildClient.getGuildClient(after_vcstate.channel.guild.id, after_vcstate.channel, checkonly=True)
                if type(state) == GuildClient:
                    await state.disconnect()
        elif len(before_vcstate.channel.members) == 1 and before_vcstate.channel.members[0] == client.user:
            state = await GuildClient.getGuildClient(before_vcstate.channel.guild.id)
            if state:
                await state.disconnect()

    @client.event
    async def on_reaction_add(reaction, author):
        if author == client.user:
            return
        try:
            guildMessage = GuildMessages.getGuildMessages(reaction.message.guild.id, reaction.message)
        except TypeError:
            print("raised")
            return

        if reaction.emoji == "➡️":
            await guildMessage.move(reaction.message, True)
        elif reaction.emoji == "⬅️":
            await guildMessage.move(reaction.message)

    @client.event
    async def on_reaction_remove(reaction, author):
        if author == client.user:
            return
        try:
            guildMessage = GuildMessages.getGuildMessages(reaction.message.guild.id, reaction.message)
        except TypeError:
            return

        if reaction.emoji == "➡️":
            await guildMessage.move(reaction.message, True)
        elif reaction.emoji == "⬅️":
            await guildMessage.move(reaction.message)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == "_destroy":
            dmchannel = str(message.channel)
            if not dmchannel.startswith("Direct Message"):
                last = message.channel.last_message
                await last.delete()
            if message.author.id == 413231303534837762:
                await GuildMessages.purge()
                await client.close()
            else:
                await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content == "_commit":
            dmchannel = str(message.channel)
            if not dmchannel.startswith("Direct Message"):
                last = message.channel.last_message
                await last.delete()
            if message.author.id == 413231303534837762:
                await GuildMessages.purge()
                subprocess.Popen(f"python3 {os.path.abspath(__file__)}", start_new_session = True, shell = True)
                await client.close()
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content =="_shutdownbot":
            dmchannel = str(message.channel)
            if not dmchannel.startswith("Direct Message"):
                last = message.channel.last_message
                await last.delete()
            if message.author.id == 413231303534837762:
                await GuildMessages.purge()
                os.system("sudo shutdown now")
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content =="_restartbot":
            dmchannel = str(message.channel)
            if not dmchannel.startswith("Direct Message"):
                last = message.channel.last_message
                await last.delete()
            if message.author.id == 413231303534837762:
                await GuildMessages.purge()
                os.system("sudo reboot")
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content.startswith("_buffer"):
            dmchannel = str(message.channel)
            if not dmchannel.startswith("Direct Message"):
                last = message.channel.last_message
                await last.delete()
            if message.author.id == 413231303534837762:
                if message.content == "_buffer":
                    response = ["```","List of animes buffered:",""]
                    for i in os.listdir(variables.non_obtainables.bufferdirectory):
                        if i == "desktop.ini":
                            continue
                        response.append(i)
                    if len(response) == 3:
                        await message.channel.send("No animes buffered", delete_after=3)
                    else:
                        response = "\n".join(response)
                        await message.channel.send(response + "\n```")
                elif message.content.startswith("_bufferadd"):
                    subprocess.Popen([sys.executable,
                        variables.non_obtainables.downloadbuffer,
                        " ".join(message.content.split(" ")[1:])])
                    await message.channel.send("Added to buffer", delete_after=3)
                elif message.content.startswith("_bufferremove"):
                    folder = " ".join(message.content.split(" ")[1:])
                    if folder in os.listdir(variables.non_obtainables.bufferdirectory):
                        shutil.rmtree(os.path.join(variables.non_obtainables.bufferdirectory, folder))
                        await message.channel.send("Removed from buffer", delete_after=3)
                    else:
                        await message.channel.send("This anime is not buffered", delete_after=3)
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        sentmessage = message.content
        if "<@" in sentmessage and ">" in sentmessage:
            for item in message.guild.members:
                if f"<@{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
        if "<:" in sentmessage and ">" in sentmessage:
            for item in message.guild.emojis:
                if f"<:{item.name}:{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")
        if sentmessage.lstrip() == '':
            return
        with open(os.path.join(variables.non_obtainables.ROOT_DIR, 'Chat log.txt'),"a", encoding='utf-8') as c:
            c.write(f"[{time.strftime('%x')}][{time.strftime('%X')}]-{{{message.guild.name}}}-{{{message.channel}}}-<{message.author}> {sentmessage}\n")
        if "@Little Hirishima" in sentmessage and message.guild.id != 990191738524139590:
            response_set = ["I AM A HORNY BITCH","I LOVE MIKE TYSON","I'M A PIECE OF SHIT","DICK AND BALLS I LOVE","PUT IT DEEP IN ME","YOU'RE WARM IN MY STOMACH"]
            response = [f"The fuck you want? {message.author.mention}","Ain't human but watcha want?","Hi friend","Ui-MAMA",
            "yeh you can't talk with me", "you sir can suck a dick",f"{message.guild.get_member(413231303534837762).mention} help this man","Who are you?",
            "shhhhh","...",f'Please write this in a piece of paper to prove that you\'re human\n```\n"{random.choice(response_set)}"\n```']
            await message.channel.send(random.choice(response))

    @client.slash_command(name='roll', description="Do a roll with our gacha minigame (Only in #jenshin)")
    async def roll(ctx, mode: discord.Option(str,"Input 10 for ten roll", required=False, choices=[discord.OptionChoice("10 roll",value="10")])):
        if ctx.channel.id == 905576290608902164:
            gachastart = gacha()
            if not mode == "10":
                await ctx.respond(f"{ctx.author.mention}\n{gachastart.roll()}")
            else:
                await ctx.respond(f"{ctx.author.mention}\n{gachastart.ten_roll()}")
        else:
            await ctx.respond("This command is only allowed in <#905576290608902164>", delete_after=3)

    @client.slash_command(name='connect', description="Connect bot to your voice channel")
    async def connect(ctx):
        await ctx.defer()
        voice = ctx.author.voice
        if voice:
            state = await GuildClient.getGuildClient(ctx.guild.id, voice.channel)
            if state == 1:
                await ctx.respond("Bot is already connected to your voice channel", delete_after=3)
                return
            await ctx.respond(f"Bot is connected to {voice.channel.mention}", delete_after=6)
        else:
            await ctx.respond("You are not connected to a voice channel", delete_after=3)

    @client.slash_command(name='disconnect', description="Disconnect bot from a voice channel")
    async def disconnect(ctx):
        await ctx.defer()
        state = await GuildClient.getGuildClient(ctx.guild.id)
        if state:
            await state.client.disconnect()
            state.cleanup()
            await ctx.respond("Bot successfully disconnected", delete_after=6)
        else:
            await ctx.respond("Bot is not connected to a voice channel",delete_after=3)

    @client.slash_command(name='play', description="Plays a song. If paused, resumes the song.")
    async def play(ctx, song: discord.Option(str, "Add song from library to play", required=False), youtube: discord.Option(str, "Add song from youtube to play", required=False)):
        await ctx.defer()
        voice = ctx.author.voice
        if voice:
            state = await GuildClient.getGuildClient(ctx.guild.id, voice.channel)
            if state == 1:
                state = await GuildClient.getGuildClient(ctx.guild.id)
            if not song:
                if youtube:
                    listsong = youtube_search(youtube)
                    if len(listsong) == 0:
                        await ctx.respond("Song not Found??", delete_after=3)
                        return
                    elif not len(listsong) == 1:

                        def check(message):
                            try:
                                mes = int(message.content)
                                if not mes in range(1, len(listsong) + 1):
                                    raise ValueError
                            except ValueError:
                                return False
                            if message.author == ctx.author and message.channel == ctx.channel:
                                return True
                            return False

                        await ctx.respond("Acknowledge!", delete_after=0)
                        response = "**Choose a song:**\n\n"
                        for i in range(0, len(listsong)):
                            response = response + '**' +str(i + 1) + ":** " + listsong[i][0] + " *- " + listsong[i][1] + "*" + "\n"
                        question = await ctx.channel.send(response)
                        try:
                            answer = await client.wait_for('message', check=check, timeout=20)
                            await answer.delete()
                            await question.delete()
                            answer = int(answer.content) - 1
                        except asyncio.TimeoutError:
                            await question.delete()
                            return
                    else:
                        answer = 0
                    if not await state.youtube((listsong[answer][2], listsong[answer][0])):
                        await ctx.respond("Song currently being loaded. Please wait for the song to play or use queue", delete_after=3)
                        return
                    await ctx.respond("**Playing song:** " + listsong[answer][0], delete_after=10)
                    # await ctx.respond("**Song will play after a few moments:** " + listsong[answer][0], delete_after=10)
                else:
                    if state.client.is_paused():
                        state.resume()
                        await ctx.respond("Song resumed!", delete_after=6)
                    else:
                        song = state.play()
                        if song == False:
                            await ctx.respond("Song currently being loaded. Please wait for the song to play or use queue", delete_after=3)
                            return
                        await ctx.respond("**Playing song:** " + song, delete_after=10)
            else:
                listsong = Music.music_search(song)
                if len(listsong) == 0:
                    await ctx.respond("Song not Found??", delete_after=3)
                    return
                elif not len(listsong) == 1:

                    def check(message):
                        try:
                            mes = int(message.content)
                            if not mes in range(1, len(listsong) + 1):
                                raise ValueError
                        except ValueError:
                            return False
                        if message.author == ctx.author and message.channel == ctx.channel:
                            return True
                        return False

                    await ctx.respond("Acknowledge!", delete_after=0)
                    response = "**Choose a song:**\n\n"
                    for i in range(0, len(listsong)):
                        response = response + '**' + str(i + 1) + ":** " + listsong[i] + "\n"
                    question = await ctx.channel.send(response)
                    try:
                        answer = await client.wait_for('message', check=check, timeout=20)
                        await answer.delete()
                        await question.delete()
                        answer = int(answer.content)
                        listsong = listsong[answer - 1]
                    except asyncio.TimeoutError:
                        await question.delete()
                        return
                else:
                    listsong = "".join(listsong)
                await ctx.respond("**Playing song:** " + state.play(listsong), delete_after=10)
        else:
            await ctx.respond("You are not connected to a voice channel", delete_after=3)

    @client.slash_command(name='pause', description="Pauses the song")
    async def pause(ctx):
        await ctx.defer()
        state = await GuildClient.getGuildClient(ctx.guild.id)
        if state:
            if state.client.is_playing():
                if not state.client.is_paused():
                    state.pause()
                    await ctx.respond("Song paused!", delete_after=6)
                else:
                    await ctx.respond("Song is already paused.", delete_after=3)
            else:
                await ctx.respond("Bot is not playing a song.", delete_after=3)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='next', description="Plays next in queue. If none, randomly chooses a song")
    async def next(ctx):
        await ctx.defer()
        state = await GuildClient.getGuildClient(ctx.guild.id)
        if state:
            song = await state.next()
            if song == 2:
                await ctx.respond("Song currently being loaded. Please wait for the song to play or use queue", delete_after=3)
                return
            elif song == False:
                song = state.play()
            else:
                await ctx.respond("**Playing song:** " + song, delete_after=10)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='queue', description="Add, remove, or list songs in queue")
    async def queue(ctx, add: discord.Option(str, "Add song from library to queue", required=False),
        youtube: discord.Option(str, 'Add song from youtube to queue', required=False,),
        remove: discord.Option(str, 'Remove a song from queue. type "all" to remove all songs in queue', required=False,)):
        await ctx.defer()
        if add or youtube:
            listsong = Music.music_search(add) if add else youtube_search(youtube)
            if len(listsong) == 0:
                await ctx.respond("Song not Found??", delete_after=3)
                return
            elif not len(listsong) == 1:

                def check(message):
                    try:
                        mes = int(message.content)
                        if not mes in range(1, len(listsong) + 1):
                            raise ValueError
                    except ValueError:
                        return False
                    if message.author == ctx.author and message.channel == ctx.channel:
                        return True
                    return False

                await ctx.respond("Acknowledge!", delete_after=0)
                response = "**Choose a song:**\n\n"
                for i in range(0, len(listsong)):
                    if add:
                        response = response + "**" + str(i + 1) + ":** " + listsong[i] + "\n"
                    else:
                        response = response + '**' +str(i + 1) + ":** " + listsong[i][0] + " *- " + listsong[i][1] + "*" + "\n"
                question = await ctx.channel.send(response)
                try:
                    answer = await client.wait_for('message', check=check, timeout=20)
                    await answer.delete()
                    await question.delete()
                    answer = int(answer.content) - 1
                except asyncio.TimeoutError:
                    await question.delete()
                    return
            else:
                answer = 0
            state = await GuildClient.getGuildClient(ctx.guild.id, no_connect = True)
            if add:
                state.append(listsong[answer])
                await ctx.respond(f"**Song added to queue:**\n\n{listsong[answer]}", delete_after=10)
            else:
                state.append((listsong[answer][2], listsong[answer][0]))
                await ctx.respond(f"**Song added to queue:**\n\n{listsong[answer][0]}", delete_after=10)
        elif remove:
            try:
                state = await GuildClient.getGuildClient(ctx.guild.id, no_connect = True)
                remove = int(remove) - 1
                await ctx.respond(f"**Song removed from queue:** {state.remove(remove)}", delete_after=10)
            except ValueError:
                if remove == "all":
                    state.purge()
                    await ctx.respond("Queue removed!",delete_after=10)
                else:
                    await ctx.respond("Only the order (number) of the song in queue is allowed.", delete_after=3)
            except IndexError:
                await ctx.respond("This is not in queue.", delete_after=3)
        else:
            state = await GuildClient.getGuildClient(ctx.guild.id, no_connect = True)
            if state.queue != []:
                guildMessage = GuildMessages.getGuildMessages(ctx.guild.id)
                await guildMessage.setQueue(ctx, state.queue)
            else:
                await ctx.respond("There are no songs in queue.", delete_after=3)

    @client.slash_command(name='loop', description="Change mode for loop")
    async def loop(ctx):
        state = await GuildClient.getGuildClient(ctx.guild.id, no_connect = True)
        if state:
            await ctx.respond(state.mode(), delete_after=10)
        else:
            await ctx.respond("Bot is not in a voice channel", delete_after=3)

    @client.slash_command(name='playing', description="Sauce for da song")
    async def playing(ctx):
        await ctx.defer()
        state = await GuildClient.getGuildClient(ctx.guild.id)
        if state and state.client.is_playing():
            await ctx.respond("**Playing song:**\n{}".format(state.song.getLength()))
        else:
            await ctx.respond("Yeah, I also don't know that song", delete_after=3)

    @client.slash_command(name='list', description="List of songs in library")
    async def list(ctx):
        await ctx.defer()
        guildMessage = GuildMessages.getGuildMessages(ctx.guild.id)
        await guildMessage.setList(ctx)

    with open(os.path.join(variables.non_obtainables.ROOT_DIR, 'Little_Hirishima Secrets.json'), "r") as f:
        TOKEN = json.load(f)['TOKEN']

    client.run(TOKEN)
except RuntimeError:
    pass
except ClientConnectorError:
    time.sleep(10)
    subprocess.Popen(f"python3 {os.path.abspath(__file__)}", start_new_session = True, shell = True)
except:
    import traceback
    with open(os.path.join(variables.non_obtainables.ROOT_DIR,'Little Hirishima Crash Report.txt'),"w") as f:
        f.write(traceback.format_exc())
    print("[ERROR] " + traceback.format_exc())

from botPath import *
import discord, threading, json, os, time, asyncio
from voiceClient import voiceClient
from musicData import Music
import guildData

client: discord.Bot = None

class webClient:
    __webClients = {}
    __webID = 0

    def __init__(self, req_id : int, guild_id : int):
        self.guild_id = guild_id
        self.id = str(webClient.__webID)
        with open(os.path.join(REQUESTSDIRECTORY, req_id + ".con"), "w") as w:
            w.write(self.id)
        threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        self.loadGuild()

        seen = time.time()
        while time.time() - seen <= 20:
            for i in os.listdir(REQUESTSDIRECTORY):
                if i == self.id:
                    with open(i, "r") as r:
                        request = r.read().split("\n")

                    if request[0] == "info":
                        with open(os.path.join(REQUESTSDIRECTORY, i + ".out"), "w") as w:
                            json.dump({"some data"}, w)
                    elif request[0] == "play":
                        song = Music(name = request[1], channel = request[2], id = request[3], thumb = request[4], length = request[5])
                        vc = voiceClient.query(self.guild_id)
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.play(song, force = True), client.loop)
                        else:
                            self.song = None
                            self.loop_ind = -1
                            self.is_paused = False
                            self.is_connected = False
                    elif request[0] == "queueadd":
                        # invoke to loop?
                        voiceClient.queueGuild(self.guild_id, add=Music(name = request[1], channel = request[2], id = request[3], thumb = request[4], length = request[5]))
                    elif request[0] == "queueremove":
                        voiceClient.queueGuild(self.guild_id, remove=int(request[1]))
                    elif request[0] == "move":
                        pass
                    elif request[0] == "next":
                        vc = voiceClient.query(self.guild_id)
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.next(index = int(request[1]), force = True), client.loop)
                        else:
                            self.song = None
                            self.loop_ind = -1
                            self.is_paused = False
                            self.is_connected = False
                    elif request[0] == "pause":
                        pass
                    elif request[0] == "resume":
                        pass
                    elif request[0] == "loop":
                        pass
                    elif request[0] == "refresh":
                        self.loadGuild()

                    os.remove(i)
            time.sleep(0.3)

        webClient.__webClients.pop(int(self.id))

    def loadGuild(self):
        vc = voiceClient.query(self.guild_id)
        if vc:
            self.song = vc.song
            self.queue = vc.queue
            self.loop = vc.loop
            self.loop_ind = vc.loop_ind
            self.is_paused = vc.is_paused
            self.is_connected = True
        else:
            self.song = None
            self.queue, self.loop = guildData.loadVoice(self.guild_id)
            self.loop_ind = -1
            self.is_paused = False
            self.is_connected = False

    @staticmethod
    def subscribe(req_id : int, guild_id : int):
        webClient.__webClients[webClient.__webID] = webClient(req_id, guild_id)
        webClient.__webID += 1


def initializeWebLink(bot : discord.Bot):
    global client
    
    client = bot

    def webListener():
        while True:
            for i in os.listdir(REQUESTSDIRECTORY):
                if i.endswith(".req"):
                    id = i.split(".")[0]
                    with open(i, "r") as r:
                        guild_id = int(r.read())
                    webClient(guild_id, id)
                    os.remove(i)

            time.sleep(0.5)

    threading.Thread(target=webListener, daemon=True).start()
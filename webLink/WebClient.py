from botPath import *
import threading, json, os, time, asyncio
from discord.ext import commands
from voiceClient import voiceClient, __baseClient
from musicData import Music
import guildData

client: commands.Bot = None

class webClient(__baseClient):
    __webClients = {}
    __webID = 0

    def __init__(self, req_id : int, guild_id : int) -> None:
        self.guild_id = guild_id
        self.id = str(webClient.__webID)
        with open(os.path.join(REQUESTSDIRECTORY, req_id + ".con"), "w") as w:
            w.write(self.id)
        threading.Thread(target=self.worker, daemon=True).start()

    def getClient(self) -> voiceClient:
        vc = voiceClient.query(self.guild_id)
        if vc:
            return vc
        else:
            self.song = None
            self.loop_ind = -1
            self.is_paused = False
            self.is_connected = False

        return None

    def worker(self) -> None:
        self.loadGuild()

        seen = time.time()
        while time.time() - seen <= 20:
            for i in os.listdir(PIPESDIRECTORY):
                if i == self.id:
                    with open(i, "r") as r:
                        request = r.read().split("\n")

                    if request[0] == "info":
                        with open(os.path.join(PIPESDIRECTORY, i + ".out"), "w") as w:
                            json.dump({
                                "song": self.song.toDict() if self.song else None,
                                "is_connected": self.is_connected,
                                "queue": self.queue,
                                "loop": self.loop,
                                "loop_ind": self.loop_ind,
                                "is_paused": self.is_paused
                            }, w)
                    elif request[0] == "play":
                        song = Music(name = request[1], channel = request[2], id = request[3], thumb = request[4], length = request[5])
                        vc = self.getClient()
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.play(song, force = True), client.loop)
                    elif request[0] == "queueadd":
                        voiceClient.queueGuild(self.guild_id, add=Music(name = request[1], channel = request[2], id = request[3], thumb = request[4], length = request[5]))
                    elif request[0] == "queueremove":
                        voiceClient.queueGuild(self.guild_id, remove=int(request[1]))
                    elif request[0] == "seek":
                        vc = self.getClient()
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.seek(float(request[1])), client.loop)
                    elif request[0] == "next":
                        vc = self.getClient()
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.next(index = int(request[1]), force = True), client.loop)
                    elif request[0] == "pause":
                        vc = self.getClient()
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.pause(), client.loop)
                    elif request[0] == "resume":
                        vc = self.getClient()
                        if vc:
                            asyncio.run_coroutine_threadsafe(vc.unpause(), client.loop)
                    elif request[0] == "loop":
                        voiceClient.loopState(self.guild_id)
                    elif request[0] == "refresh":
                        self.loadGuild()
                    elif request[0] == "close":
                        os.remove(i)
                        seen = 0
                        break

                    os.remove(i)
                    seen = time.time()
                    break
            time.sleep(0.3)

        webClient.__webClients.pop(int(self.id))

    def loadGuild(self) -> None:
        vc = voiceClient.query(self.guild_id)
        if vc:
            self.song = vc.song
            self.queue = [i.toDict() for i in vc.queue]
            self.loop = vc.loop
            self.loop_ind = vc.loop_ind
            self.is_paused = vc.is_paused
            self.is_connected = True
        else:
            self.song = None
            self.queue, self.loop = guildData.loadVoice(self.guild_id)
            self.queue = [i.toDict() for i in self.queue]
            self.loop_ind = -1
            self.is_paused = False
            self.is_connected = False

    @staticmethod
    def subscribe(req_id : int, guild_id : int):
        webClient.__webClients[webClient.__webID] = webClient(req_id, guild_id)
        webClient.__webID += 1


def initializeWebLink(bot : commands.Bot):
    global client
    
    client = bot

    def webListener():
        while True:
            for i in os.listdir(REQUESTSDIRECTORY):
                if i.endswith(".req"):
                    id = i.split(".")[0]
                    with open(i, "r") as r:
                        guild_id = int(r.read())
                    webClient.subscribe(id, guild_id)

            time.sleep(0.5)

    threading.Thread(target=webListener, daemon=True).start()
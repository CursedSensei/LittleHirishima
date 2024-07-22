from botPath import *
import discord, threading, json, os, time
from voiceClient import voiceClient
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
                        pass
                    elif request[0] == "queue":
                        pass
                    elif request[0] == "move":
                        pass
                    elif request[0] == "next":
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
        else:
            self.song = None
            self.queue, self.loop = guildData.loadVoice(self.guild_id)
            self.loop_ind = -1
            self.is_paused = False

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
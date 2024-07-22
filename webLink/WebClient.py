from botPath import *
import discord, threading, io, os, time
import voiceClient

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
                        pass
                        # send data in json
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
        pass

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
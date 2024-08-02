from botPath import *
from botConst import *
from musicData import Music
import json, discord

async def loadGuilds(client : discord.Bot):
    guilds = []
    async for guild in client.fetch_guilds(limit=100):
        guilds.append(guild.id)

    with open(GUILDSFILE, "w") as w:
        json.dump(guilds, w)

def updateGuilds(add : discord.Guild = None, remove : discord.Guild = None):
    with open(GUILDSFILE, "r") as r:
        guilds = json.load(r)

    if add:
        guilds.append(add.id)
    elif remove:
        guilds.remove(remove.id)

    with open(GUILDSFILE, "w") as w:
        json.dump(guilds, w)

def loadVoice(guild_id : int) -> tuple[list, int]:
    guildSpace = os.path.join(GUILDPATH, str(guild_id))
    
    if not os.path.exists(guildSpace):
        os.mkdir(guildSpace)
    
    guildSpace = os.path.join(guildSpace, 'voice.json')
    if not os.path.exists(guildSpace):
        with open(guildSpace, "w") as w:
            json.dump([DEFAULT], w)
        return ([], DEFAULT)
    
    with open(guildSpace, "r") as r:
        voice = json.load(r)
    loop = voice.pop(-1)

    voice = [Music(**i) for i in voice]

    return (voice, loop)

def updateVoice(guild_id : int, loop : int, queue : list[Music] = []) -> None:
    guildSpace = os.path.join(GUILDPATH, str(guild_id), 'voice.json')

    queue = [i.toDict() for i in queue]

    with open(guildSpace, "w") as w:
        json.dump(queue + [loop], w)


def updateRecent(guild_id : int, song : Music) -> None:
    recentFile = os.path.join(GUILDPATH, str(guild_id), 'recent.json')

    if os.path.exists(recentFile):
        with open(recentFile, "r") as r:
            recents = json.load(r)
    else:
        recents = []

    found = False

    for i in range(0, len(recents)):
        if recents[i]['id'] == song.id:
            found = True
            recent = recents.pop(i)
            recent["plays"] += 1

            recents.insert(0, recent)
            break

    if not found:
        recents.insert(0, song.toDict(plays = 1))

    with open(recentFile, "w") as w:
        json.dump(recents, w)
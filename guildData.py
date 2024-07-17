from botPath import *
from botConst import *
from musicData import Music
import json

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

    queue = [{"name": i.name, "channel": i.channel, "thumb": i.thumb, "id": i.id, "length": i.length} for i in queue]

    with open(guildSpace, "w") as w:
        json.dump(queue + [loop], w)

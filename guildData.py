from botPath import *
from botConst import loopState
import json

def loadVoice(guild_id : int) -> tuple[list, loopState]:
    guildSpace = os.path.join(GUILDPATH, str(guild_id))
    
    if not os.path.exists(guildSpace):
        os.mkdir(guildSpace)
    
    guildSpace = os.path.join(guildSpace, 'voice.json')
    if not os.path.exists(guildSpace):
        with open(guildSpace, "w") as w:
            json.dump([loopState.DEFAULT], w)
        return ([], loopState.DEFAULT)
    
    with open(guildSpace, "r") as r:
        voice = json.load(r)
    loop = voice.pop(-1)

    return (voice, loop)

def updateVoice(guild_id : int, loop : loopState, queue = []) -> None:
    guildSpace = os.path.join(GUILDPATH, str(guild_id), 'voice.json')

    with open(guildSpace, "w") as w:
        json.dump(queue + [loop], w)


def loadPopular() -> list[list[str, int]]:
    with open(LIBRARYLOG, "r") as r:
        library = json.load(r)
    return library

def updatePopular(library : list[list[str, int]]) -> None:
    with open(LIBRARYLOG, "w") as w:
        json.dump(library, w)
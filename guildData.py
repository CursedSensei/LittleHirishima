import botPath
from voiceClient import loopState

def loadVoice(guild_id : int) -> tuple[list, loopState]:
    return ([], loopState.DEFAULT)

def updateVoice(guild_id : int, loop : loopState, queue = []):
    pass


def loadPopular() -> list[list[str, int]]:
    return {}

def updatePopular(library : list[list[str, int]]):
    pass
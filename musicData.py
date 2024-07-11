from time import time
from lib.lib.youtube_search import youtube_search
import guildData

class Music:
    def __init__(self, start = False, **kwargs) -> None:
        self.name = kwargs['name']
        self.channel = kwargs['channel']
        self.thumb = kwargs['thumb']
        self.id = kwargs['id']
        self.length = kwargs['length']
        
        self.time = time() if start else None
        self.offset = 0

    def play(self):
        self.time = time()

    def pause(self):
        self.offset += time() - self.time


class lovedMusic:
    def __init__(self) -> None:
        self.library = guildData.loadPopular()

    async def log(self, id : str, file_path : str):
        pass

def youtube_query(query : str) -> list[Music]:
    return [Music(name = i[0], channel = i[1], id = i[2], thumb = i[3], length = i[4]) for i in youtube_search(query)]
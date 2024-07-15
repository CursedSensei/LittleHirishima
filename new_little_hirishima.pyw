import botPath
import voiceClient
import musicData
import botControl

import json
import discord
from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError

try:
    musicLogger = musicData.lovedMusic()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = commands.Bot(intents=intents)

    @client.slash_command(name='play', description="Plays a song. If paused, resumes the song.")
    async def play(ctx: discord.ApplicationContext, query: discord.Option(str, "Song to search from youtube", required=False)):
        pass
    botControl.initializeAdmin(client)

    with open(botPath.TOKENPATH, "r") as f:
        TOKEN = json.load(f)['TOKEN']

    client.run(TOKEN)
except RuntimeError:
    pass
except ClientConnectorError:
    import subprocess, time, os

    time.sleep(10)
    subprocess.Popen(f"python3 {os.path.abspath(__file__)}", start_new_session = True, shell = True)
except:
    import traceback
    with open(botPath.ERRORPATH,"w") as f:
        f.write(traceback.format_exc())
    print("[ERROR] " + traceback.format_exc())

import botPath
import voiceClient
import musicData

import discord, json
from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError

try:
    musicLogger = musicData.lovedMusic()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = commands.Bot(intents=intents)

    voiceClient.initializeVoice(client)

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
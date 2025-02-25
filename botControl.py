import discord
from botPath import *
from botResponse import OllamaSession
import subprocess, os, shutil, sys, time
from asyncio import sleep

stacktureProcess: subprocess.Popen = subprocess.Popen(['/home/aoi/.cargo/bin/cargo', 'run'], env={'OPENSSL_DIR': '/usr', 'OPENSSL_LIB_DIR': '/usr/local/lib64', 'OPENSSL_INCLUDE_DIR': '/usr/include'}, cwd="/home/aoi/Desktop/stackture-server")

def initializeAdmin(client : discord.Bot):
    async def removeCommand(message : discord.Message):
        dmchannel = str(message.channel)
        if not dmchannel.startswith("Direct Message"):
            last = message.channel.last_message
            try:
                await last.delete()
            except:
                pass

    @client.event
    async def on_message(message : discord.Message):
        global stacktureProcess
        if message.author == client.user:
            return

        if message.content == "_destroy":
            if message.author.id == 413231303534837762:
                await removeCommand(message)
                await client.close()
                stacktureProcess.terminate()
                return

        if message.content == "_commit":
            if message.author.id == 413231303534837762:
                await removeCommand(message)
                subprocess.run("git pull", cwd=ROOT_DIR, shell = True)
                subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'little_hirishima.pyw')], start_new_session = True)
                await client.close()
                stacktureProcess.terminate()
                return

        if message.content =="_shutdownbot":
            if message.author.id == 413231303534837762:
                await removeCommand(message)
                os.system("sudo shutdown now")
                return

        if message.content =="_restartbot":
            if message.author.id == 413231303534837762:
                await removeCommand(message)
                os.system("sudo reboot")
                return
            
        if message.content =="_pull":
            if message.guild.id == 1338837641797435488:
                stacktureProcess.terminate()
                await removeCommand(message)
                gitPullProcess = subprocess.Popen(['git', 'pull'], cwd='/home/aoi/Desktop/stackture-server')
                while gitPullProcess.poll() == None:
                    await sleep(3)
                stacktureProcess = subprocess.Popen(['/home/aoi/.cargo/bin/cargo', 'run'], env={'OPENSSL_DIR': '/usr', 'OPENSSL_LIB_DIR': '/usr/local/lib64', 'OPENSSL_INCLUDE_DIR': '/usr/include'}, cwd="/home/aoi/Desktop/stackture-server")
                await message.channel.send('Pulled and Restarted :D', delete_after=5)
                return
        
        if message.content =="_start":
            if message.guild.id == 1338837641797435488:
                stacktureProcess.terminate()
                await removeCommand(message)
                stacktureProcess = subprocess.Popen(['/home/aoi/.cargo/bin/cargo', 'run'], env={'OPENSSL_DIR': '/usr', 'OPENSSL_LIB_DIR': '/usr/local/lib64', 'OPENSSL_INCLUDE_DIR': '/usr/include'}, cwd="/home/aoi/Desktop/stackture-server")
                await message.channel.send('Restarted :D', delete_after=5)
                return

        if message.content.startswith("_buffer"):
            if message.author.id == 413231303534837762:
                await removeCommand(message)
                if message.content == "_buffer":
                    response = ["```","List of animes buffered:",""]
                    for i in os.listdir(ANIMEDIRECTORY):
                        if i == "desktop.ini":
                            continue
                        response.append(i)
                    if len(response) == 3:
                        await message.channel.send("No animes buffered", delete_after=3)
                    else:
                        response = "\n".join(response)
                        await message.channel.send(response + "\n```")
                elif message.content.startswith("_bufferadd"):
                    subprocess.Popen([sys.executable,
                        ANIMEDOWNLOADER,
                        " ".join(message.content.split(" ")[1:])])
                    await message.channel.send("Added to buffer", delete_after=3)
                elif message.content.startswith("_bufferremove"):
                    folder = " ".join(message.content.split(" ")[1:])
                    if folder in os.listdir(ANIMEDIRECTORY):
                        shutil.rmtree(os.path.join(ANIMEDIRECTORY, folder))
                        await message.channel.send("Removed from buffer", delete_after=3)
                    else:
                        await message.channel.send("This anime is not buffered", delete_after=3)
                return

        isMentioned = False
        sentmessage = message.content
        if "<@" in sentmessage and ">" in sentmessage:
            for item in message.guild.members:
                if f"<@{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
                    if item.id == client.user.id:
                        isMentioned = True
        if "<:" in sentmessage and ">" in sentmessage:
            for item in message.guild.emojis:
                if f"<:{item.name}:{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")
        if sentmessage.lstrip() == '':
            return
        with open(CHATLOG,"a", encoding='utf-8') as c:
            c.write(f"[{time.strftime('%x')}][{time.strftime('%X')}]-{{{message.guild.name}}}-{{{message.channel}}}-<{message.author}> {sentmessage}\n")

        if isMentioned:
            OllamaSession.addOllama(message.channel, client)

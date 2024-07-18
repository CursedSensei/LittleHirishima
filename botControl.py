import discord
from botPath import *
import subprocess, os, shutil, sys, time, random

def initializeAdmin(client : discord.Bot):
    async def removeCommand(message : discord.Message):
        dmchannel = str(message.channel)
        if not dmchannel.startswith("Direct Message"):
            last = message.channel.last_message
            await last.delete()

    @client.event
    async def on_message(message : discord.Message):
        if message.author == client.user:
            return

        if message.content == "_destroy":
            await removeCommand(message)
            if message.author.id == 413231303534837762:
                await client.close()
            else:
                await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content == "_commit":
            await removeCommand(message)
            if message.author.id == 413231303534837762:
                os.system("git pull")
                subprocess.Popen(f"python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'little_hirishima.pyw')}", start_new_session = True, shell = True)
                await client.close()
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content =="_shutdownbot":
            await removeCommand(message)
            if message.author.id == 413231303534837762:
                os.system("sudo shutdown now")
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content =="_restartbot":
            await removeCommand(message)
            if message.author.id == 413231303534837762:
                os.system("sudo reboot")
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        if message.content.startswith("_buffer"):
            await removeCommand(message)
            if message.author.id == 413231303534837762:
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
            else:
                last = await message.channel.send(f"fuck you {message.author.mention} your not my daddy.", delete_after=3)
            return

        sentmessage = message.content
        if "<@" in sentmessage and ">" in sentmessage:
            for item in message.guild.members:
                if f"<@{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
        if "<:" in sentmessage and ">" in sentmessage:
            for item in message.guild.emojis:
                if f"<:{item.name}:{item.id}>" in sentmessage:
                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")
        if sentmessage.lstrip() == '':
            return
        with open(CHATLOG,"a", encoding='utf-8') as c:
            c.write(f"[{time.strftime('%x')}][{time.strftime('%X')}]-{{{message.guild.name}}}-{{{message.channel}}}-<{message.author}> {sentmessage}\n")
        if "@Little Hirishima" in sentmessage and message.guild.id != 990191738524139590:
            response_set = ["I AM A HORNY BITCH","I LOVE MIKE TYSON","I'M A PIECE OF SHIT","DICK AND BALLS I LOVE","PUT IT DEEP IN ME","YOU'RE WARM IN MY STOMACH"]
            response = [f"The fuck you want? {message.author.mention}","Ain't human but watcha want?","Hi friend","Ui-MAMA",
            "yeh you can't talk with me", "you sir can suck a dick",f"{message.guild.get_member(413231303534837762).mention} help this man","Who are you?",
            "shhhhh","...",f'Please write this in a piece of paper to prove that you\'re human\n```\n"{random.choice(response_set)}"\n```']
            await message.channel.send(random.choice(response))

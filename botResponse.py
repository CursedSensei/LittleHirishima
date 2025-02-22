from ollama import AsyncClient
from discord import TextChannel, Bot
from asyncio import create_task, wait_for
from time import time
from datetime import datetime

ollamaClient = AsyncClient("http://192.168.1.4:11434")

class OllamaSession:
    def __init__(self, channel: TextChannel, bot: Bot):
        self.channel = channel
        self.bot = bot
        create_task(self.worker())

    async def worker(self):
        try:
            lastChat = time()
            while True:
                async with self.channel.typing():
                    context = []
                    async for message in self.channel.history(limit=10):
                        sentmessage = message.content
                        if "<@" in sentmessage and ">" in sentmessage:
                            for item in message.guild.members:
                                if f"<@{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
                        if "<:" in sentmessage and ">" in sentmessage:
                            for item in message.guild.emojis:
                                if f"<:{item.name}:{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")

                        context.insert(0, '[' + str(message.created_at) + '] <' + message.author.name + '> ' + sentmessage)

                    await wait_for(ollamaClient.ps(), timeout=3)

                    print(context)
                    response = await ollamaClient.chat(model='llama3.1', messages=[
                        {
                            'role': 'system',
                            'content': 'Your name is Little Hirishima. You are in a group chat. You should respond when it is clear, based on the context of the conversation, that you are being addressed. This includes: 1) When a user directly asks you a question or makes a request, even without mentioning your name. 2) When a user is responding to a previous message of yours.  If the conversation is a general discussion and your name is not mentioned, remain silent.'
                        },
                        {
                            'role': 'user',
                            'content': "Context:\n\n[datetime] <user> message\n\n" + '\n'.join(context) + '\n\nCurrent Datetime: ' + str(datetime.utcnow()),
                        },
                    ], tools=[
                        {
                            'type': 'function',
                            'function': {
                                'name': 'chat',
                                'description': "Chat to the channel.",
                                "parameters": {
                                    'type': 'object',
                                    'properties': {
                                        'message': {
                                            'type': 'string',
                                            'description': 'Message to chat to channel. Merge all the responses you want to chat here.'
                                        }
                                    }
                                },
                                'required': ['message']
                            }
                        },
                        {
                            'type': 'function',
                            'function': {
                                'name': 'ignore',
                                'description': "Use this if you will not chat.",
                                "parameters": {},
                                'required': []
                            }
                        }
                    ])

                    print(response.message)

                    for i in response.message.tool_calls:
                        if (i.function.name == "chat"):
                            await self.channel.send(i.function.arguments.get('message'))
                            lastChat = time()

                await self.bot.wait_for('message', check=lambda mes: mes.channel == self.channel, timeout=max(0, 120 - (time() - lastChat)))
        except:
            print(self.channel.id, ' Session AI closed')
            sessions.pop(self.channel.id)

    @staticmethod
    def addOllama(channel: TextChannel, bot: Bot):
        if sessions.get(channel.id) == None:
            sessions.update({channel.id: OllamaSession(channel, bot)})

sessions: dict[int, OllamaSession] = {}
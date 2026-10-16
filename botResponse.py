import random
import json
from litellm import acompletion
from discord import TextChannel, Bot
from asyncio import create_task, wait_for
from time import time
from datetime import datetime

from ai.const import COMPLETION_AI_TOOLS, SYSTEM_PROMPT

AI_MODEL = "openai/local-qwen"
AI_ENDPOINT = "http://192.168.1.113:8090/v1"
AI_API_KEY = "sk-no-key-required"
AI_DISABLED = True

botID = 0

class AISession:
    context: list[dict] = [{}]
    mood: float = random.uniform(5.0, 1.0)
    lastChat = time()
    latestMessageDatetime: datetime | None = None 

    def __init__(self, channel: TextChannel, bot: Bot):
        self.channel = channel
        self.bot = bot
        create_task(self.worker())

    def __generate_system_prompt(self):
        return {'role': 'system', 'content': SYSTEM_PROMPT + f"Current Time: {datetime.utcnow()}\nCurrent Mood: {self.mood:.2f}\n"}

    def __set_mood(self, newMood: float):
        self.mood = max(0.0, min(1.0, newMood))

    async def worker(self):
        try:
            while True:
                async with self.channel.typing():
                    async for message in self.channel.history(limit=10, after=self.latestMessageDatetime, oldest_first=True):
                        sentmessage = message.content
                        if "<@" in sentmessage and ">" in sentmessage:
                            for item in message.guild.members:
                                if f"<@{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
                        if "<:" in sentmessage and ">" in sentmessage:
                            for item in message.guild.emojis:
                                if f"<:{item.name}:{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")

                        self.context.append({
                            'role': 'user' if message.author.id != botID else 'assistant',
                            'content': '[' + str(message.created_at) + '] <' + message.author.name + '> ' + sentmessage
                        })
                        self.latestMessageDatetime = message.created_at

                    self.context[0] = self.__generate_system_prompt()
                    print(self.context)

                    response = await acompletion(
                        model=AI_MODEL,
                        messages=self.context,
                        tools=COMPLETION_AI_TOOLS,
                        tool_choice="required",
                        reasoning_effort='low',
                        api_base=AI_ENDPOINT,
                        api_key=AI_API_KEY
                    )

                    for i in response.choices[0].message.tool_calls:
                        if (i.function.name == "chat"):
                            arguments = json.loads(i.function.arguments)

                            AIMessage = arguments['message']
                            newMood = arguments.get('set_mood_after', 0)

                            AIIdx = 0
                            while len(AIMessage[AIIdx : AIIdx + 1475]):
                                await self.channel.send(AIMessage[AIIdx : AIIdx + 1475])
                                AIIdx += 1475

                            self.lastChat = time()
                            self.__set_mood(newMood)
                        elif (i.function.name == "ignore"):
                            newMood = json.loads(i.function.arguments).get('set_mood', 0)
                            self.__set_mood(newMood)

                await self.bot.wait_for('message', check=lambda mes: mes.channel == self.channel, timeout=max(0, 120 - (time() - self.lastChat)))
        except:
            print(f'Session AI closed at [{self.channel.guild.name} - {self.channel.name}]')
            sessions.pop(self.channel.id)

    @staticmethod
    def addOllama(channel: TextChannel, bot: Bot):
        global botID

        if AI_DISABLED:
            return
        
        if sessions.get(channel.id) == None:
            sessions.update({channel.id: AISession(channel, bot)})
        botID = bot.user.id

sessions: dict[int, AISession] = {}

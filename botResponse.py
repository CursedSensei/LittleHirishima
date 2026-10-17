import random
import json
import httpx
from litellm import acompletion
from discord import TextChannel, Bot
from asyncio import create_task, wait, FIRST_COMPLETED, create_task
from time import time
from datetime import datetime

from ai.const import COMPLETION_AI_TOOLS, SYSTEM_PROMPT

AI_MODEL = "openai/local-qwen"
AI_ENDPOINT = "http://192.168.1.113:8090/v1"
AI_API_KEY = "sk-no-key-required"
AI_TIMEOUT_SECONDS = 30.0
AI_DISABLED = True

botID = 0

class AISession:
    context: list[dict] = [{}]
    mood: float = random.uniform(0.5, 1.0)
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

    async def __wait_for_message(self, timeout: float | None = None) -> None:
        await self.bot.wait_for('message', check=lambda mes: mes.channel == self.channel and mes.author.id != botID, timeout=timeout)

    async def worker(self):
        try:
            while True:
                async with self.channel.typing():
                    newContext = []

                    async for message in self.channel.history(limit=10, after=self.latestMessageDatetime, oldest_first=False):
                        sentmessage = message.content
                        if "<@" in sentmessage and ">" in sentmessage:
                            for item in message.guild.members:
                                if f"<@{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<@{item.id}>",f"@{item.name}")
                        if "<:" in sentmessage and ">" in sentmessage:
                            for item in message.guild.emojis:
                                if f"<:{item.name}:{item.id}>" in sentmessage:
                                    sentmessage = sentmessage.replace(f"<:{item.name}:{item.id}>",f":{item.name}:")

                        newContext.insert(0, {
                            'role': 'user' if message.author.id != botID else 'assistant',
                            'content': '[' + str(message.created_at) + '] <' + message.author.name + '> ' + sentmessage
                        })

                        if (self.latestMessageDatetime is None) or (message.created_at > self.latestMessageDatetime):
                            self.latestMessageDatetime = message.created_at

                    self.context[0] = self.__generate_system_prompt()
                    self.context.extend(newContext)

                    msg_task = create_task(self.__wait_for_message(), name="wait_for_message")
                    llm_task = create_task(acompletion(
                        model=AI_MODEL,
                        messages=self.context,
                        tools=COMPLETION_AI_TOOLS,
                        tool_choice="required",
                        reasoning_effort='low',
                        api_base=AI_ENDPOINT,
                        api_key=AI_API_KEY,
                        timeout=AI_TIMEOUT_SECONDS
                    ))

                    done, pending = await wait({msg_task, llm_task}, return_when=FIRST_COMPLETED)
                    
                    for task in pending:
                        task.cancel()

                    done_task = done.pop()
                    if done_task.get_name() == "wait_for_message":
                        continue

                    response = done_task.result()

                    for i in response.choices[0].message.tool_calls:
                        if (i.function.name == "chat"):
                            arguments = json.loads(i.function.arguments)

                            AIMessage = arguments['message']
                            newMood = arguments.get('set_mood_after', self.mood)

                            AIIdx = 0
                            while len(AIMessage[AIIdx : AIIdx + 1475]):
                                await self.channel.send(AIMessage[AIIdx : AIIdx + 1475])
                                AIIdx += 1475

                            self.lastChat = time()
                            self.__set_mood(newMood)
                        elif (i.function.name == "ignore"):
                            newMood = json.loads(i.function.arguments).get('set_mood_after', self.mood)
                            self.__set_mood(newMood)

                await self.__wait_for_message(timeout=max(0, 120 - (time() - self.lastChat)))
        except:
            print(f'Session AI closed at [{self.channel.guild.name} - {self.channel.name}]')
            sessions.pop(self.channel.id)

    @staticmethod
    async def isOnline() -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(AI_ENDPOINT + "/models", timeout=5.0)

            return response.status_code == 200
        except:
            return False
        

    @staticmethod
    async def addOllama(channel: TextChannel, bot: Bot):
        global botID

        if AI_DISABLED or not await AISession.isOnline():
            return
        
        if sessions.get(channel.id) == None:
            sessions.update({channel.id: AISession(channel, bot)})
        botID = bot.user.id

sessions: dict[int, AISession] = {}

import botPath
import guildData
import asyncio, discord


class voiceClient:
    __voiceClients = {}

    def __init__(self, guild_id : int, channel_id : int, client : discord.VoiceClient, bot : discord.Bot) -> None:
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.client = client
        
        self.queue, self.loop = guildData.loadVoice(guild_id)

        asyncio.run_coroutine_threadsafe(self.worker(), bot.loop)

    def cleanup(self) -> None:
        self.client.cleanup()
        if (self.guild_id in voiceClient.__voiceClients):
            voiceClient.__voiceClients.pop(self.guild_id)

    async def worker(self) -> None:
        while self.client.is_connected():
            # to implement
            await asyncio.sleep(0.3)

    @staticmethod
    def query(guild_id : int) -> object | None:
        if (guild_id in voiceClient.__voiceClients):
            return voiceClient.__voiceClients[guild_id]
        return None

    @staticmethod
    def create(guild_id : int, channel_id : int, client : discord.VoiceClient, bot : discord.Bot):
        vc = voiceClient(guild_id, channel_id, client, bot)
        voiceClient.__voiceClients[guild_id] = vc
        return vc


def initializeVoice(client: discord.Bot) -> None:
    @client.slash_command(description="Connect bot to your voice channel")
    async def connect(ctx: discord.ApplicationContext):
        if (not ctx.author.voice):
            await ctx.respond("You are not connected to a voice channel", delete_after=3)
            return

        await ctx.defer()
        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if (vClient == None):
            voiceClient.create(ctx.guild_id, vChannel.id, await vChannel.connect(), client)
            await ctx.respond(f"Bot is connected to {vChannel.mention}", delete_after=6)
        elif (vClient.channel_id == vChannel.id):
            await ctx.respond("Bot is already connected to your voice channel", delete_after=3)
        else:
            await ctx.respond("Bot is already connected to a voice channel", delete_after=3)

    @client.slash_command(name='disconnect', description="Disconnect bot from a voice channel")
    async def disconnect(ctx: discord.ApplicationContext):
        if (not ctx.author.voice):
            await ctx.respond("You are not connected to a voice channel", delete_after=3)
            return
        
        await ctx.defer()
        vClient = voiceClient.query(ctx.guild_id)
        vChannel = ctx.author.voice.channel

        if (vClient == None):
            await ctx.respond(f"Bot is not connected to a voice channel", delete_after=6)
        elif (vClient.channel_id == vChannel.id):
            await vClient.client.disconnect()
            vClient.cleanup()

            await ctx.respond("Bot successfully disconnected", delete_after=6)
        else:
            await ctx.respond("You are not connected to the Bot's voice channel", delete_after=3)
from discord.ext import commands
import discord
import logging

logger = logging.getLogger(__name__)


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener("on_message")
    async def war(self, message):
        word = "война"
        if word in message.content.casefold():
            await message.channel.send("ВОЙНЯЯЯЯЯ!!!!")
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def wrong(self, message):
        word = " ой "
        if word in message.content.casefold():
            await message.channel.send("НЕ ТА БАЗА!")
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def add_reaction(self, message):
        words = {
            "квад": discord.utils.get(self.bot.emojis, name="quad"),
            "алло": "📞",
            "окно": "🪟",
        }
        for key, value in words.items():
            if key in message.content.casefold():
                await message.add_reaction(value)


def setup(bot):
    bot.add_cog(Listener(bot))

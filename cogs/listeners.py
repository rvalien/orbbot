import discord
import logging
import random

from discord.ext import commands

logger = logging.getLogger(__name__)


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener("on_message")
    async def word_react(self, message):
        trigger_words = {"война": "ВОЙНЯЯЯЯЯ!!!", "извините": "ПИРОЖКИ!!!"}

        word = next((value for key, value in trigger_words.items() if key in message.content.casefold()), None)
        if word:
            await message.channel.send(word)
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def add_reaction(self, message):
        react_dict = {
            "квад": discord.utils.get(self.bot.emojis, name="quad"),
            "алло": "📞",
            "окно": "🪟",
            "123": "🛎️",
            "пирожки": random.choice(["🥐", "🥨", "🥯", "🥮"]),
        }

        emoji = next((value for key, value in react_dict.items() if key in message.content.casefold()), None)
        if emoji:
            await message.add_reaction(emoji)
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Listener(bot))

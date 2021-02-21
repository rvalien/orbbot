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
    async def kvad(self, message):
        word = "квад"
        if word in message.content.casefold():
            emoji = discord.utils.get(self.bot.emojis, name="quad")
            await message.add_reaction(emoji)

    @commands.Cog.listener("on_message")
    async def window(self, message):
        word = "окно"
        if word in message.content.casefold():
            await message.add_reaction('🪟')


def setup(bot):
    bot.add_cog(Listener(bot))

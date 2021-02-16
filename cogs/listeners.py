from discord.ext import commands

import logging

logger = logging.getLogger(__name__)


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener("on_message")
    async def war(self, message):
        war = "война"
        if war in message.content.casefold():
            await message.channel.send("ВОЙНЯЯЯЯЯ!!!!")
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def kvad(self, message):
        war = " квад"
        if war in message.content.casefold():
            await message.channel.send("Паша, kwad!")
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Listener(bot))

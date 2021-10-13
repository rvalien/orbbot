import json
import requests

from discord.ext import commands


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.is_owner()
    async def members(self, ctx):
        am = self.bot.get_all_members()
        for m in am:
            print(m.id, m.name)


def setup(bot):
    bot.add_cog(DevCommands(bot))

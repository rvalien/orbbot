import asyncio

from discord.ext import commands

reactions = ["👍", "👎"]


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def poll(self, ctx, *, question):
        """
        simple poll with only 2 reactions (👍, 👎)
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        m = await ctx.send(f"Poll: {question} - {ctx.author}")
        for emoji in reactions:
            await m.add_reaction(emoji)

    @commands.command()
    async def ping(self, ctx):
        """
        used to check if the bot is alive
        """
        await ctx.send(f"pong! {round(self.bot.latency * 1000)} ms")


def setup(bot):
    bot.add_cog(Poll(bot))

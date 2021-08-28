import os
import random
from discord.ext import commands

delay = int(os.environ["DELAY"])


class BookClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["books", "my_list", "my_books"])
    async def my_list(self, ctx):
        await ctx.send(f"your books: []")

    @commands.command(aliases=["add_books"])
    async def add_book(self, ctx):
        await ctx.send(f"book added ")

    @commands.command()
    async def remove_book(self, ctx):
        await ctx.send(f"book removed")

    @commands.command(aliases=["dice", "die"])
    async def roll(self, ctx):
        """
        roll dice and set as reaction on your command
        """
        dice = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")
        die = random.choice(dice)
        await ctx.message.add_reaction(die)


def setup(bot):
    bot.add_cog(BookClub(bot))

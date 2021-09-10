import os
from discord.ext import commands

delay = int(os.environ["DELAY"])
# TODO не работает ещё ничего для книжного клуба


class BookClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["books", "my_list", "my_books"])
    async def my_list(self, ctx):
        await ctx.send(f"your books: []")

    @commands.command(aliases=["add_books"])
    async def add_book(self, ctx):
        await ctx.send(f"book added")

    @commands.command()
    async def remove_book(self, ctx):
        await ctx.send(f"book removed")


def setup(bot):
    bot.add_cog(BookClub(bot))

"""
this bot made with ❤️
"""

__author__ = "Valien"
__version__ = "0.0.14"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

import discord
import os
import logging
import asyncpg

from discord.ext import commands
from tasks.tasks import change_status, bdays_check

INITIAL_EXTENSIONS = [
    "cogs.qc",
    "cogs.listeners",
    "cogs.commands",
    "cogs.dev",
    "cogs.games",
]
token = os.environ["TOKEN"]
# token = os.environ["TEST_TOKEN"]
prefix = os.environ["PREFIX"]
database_url = os.environ["DATABASE_URL"]

intents = discord.Intents.default()
intents.members = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info("run")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    intents=intents,
    description="Small bot for lil QC community",
)


@bot.event
async def on_ready():
    """https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready"""

    bot.pg_con = await asyncpg.create_pool(database_url)
    await bot.pg_con.execute("CREATE TABLE IF NOT EXISTS users(id bigint PRIMARY KEY, data text);")
    await bot.change_presence(status=discord.Status.idle)
    print(f"Init {bot.user.name}-{bot.user.id}\nAPI version: {discord.__version__}\nbot version: {__version__}")
    await bot.change_presence(status=discord.Status.online)
    print("beep-boop i'm online...!")

    print("load loop tasks")
    change_status.start(bot)
    bdays_check.start(bot)

    print("load extension")
    for extension in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
            logger.info(f"load: {extension}\n")
        except Exception as e:
            logger.warning(f"Failed to load extension {extension}\n{type(e).__name__}: {e}")
    print("let's play")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="wat"))
    else:
        logger.error(ctx.message.author, error)
        print(ctx.message.author, error)


if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)

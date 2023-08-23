"""
This bot made with ❤️
"""

__author__ = "Valien"
__version__ = "0.0.16"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

import asyncpg
import datetime
import discord
import logging.handlers
import os
import redis

from discord.ext import commands
from models.db_gino import on_startup as gino_on_startup
from tasks.tasks import bdays_check, deadline_check

INITIAL_EXTENSIONS = [
    "cogs.qc",
    # "cogs.listeners",
    "cogs.commands",
    "cogs.books",
    # "cogs.games",
    # "cogs.roles",
]
token = os.environ["TOKEN"]
# token = os.environ["TEST_TOKEN"]

admin = os.environ["ADMIN"]
prefix = os.getenv("PREFIX", "!")
database_url = os.environ["DATABASE_URL"]
CLIENT = redis.from_url(os.environ["REDIS_URL"])

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    intents=intents,
    description="Small bot for lil QC community",
    case_insensitive=True,
)


@bot.event
async def on_ready():
    """https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready"""

    bot.github = "https://github.com/rvalien/orbbot"
    bot.launch_time = datetime.datetime.utcnow()
    bot.pg_con = await asyncpg.create_pool(database_url)

    sql_path = "sql_queries"
    for file in os.listdir(sql_path):
        logger.info(f"prepare db with: {file}\n")
        with open(os.path.join(sql_path, file), encoding="utf-8", mode="r") as raw_file:
            query = raw_file.read()
            await bot.pg_con.execute(query)

    await gino_on_startup(database_url)
    logger.info(f"Init {bot.user.name}-{bot.user.id}.API version: {discord.__version__}. bot version: {__version__}")
    logger.info(f"beep-boop i'm online...{bot.launch_time}!")
    bdays_check.start(bot)
    deadline_check.start(bot, CLIENT)
    for extension in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            logger.warning(f"Failed to load extension {extension}{type(e).__name__}: {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction("⚠️")
    else:
        logger.error(f"{ctx.message.author}, {error}")


if __name__ == "__main__":
    bot.run(token, reconnect=True)

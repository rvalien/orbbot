"""
This bot made with ❤️
"""

__author__ = "Valien"
__version__ = "0.0.15"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

import asyncpg
import datetime
import discord
import logging
import os
import redis

from discord.ext import commands
from models.db_gino import on_startup as gino_on_startup
from tasks.tasks import change_status, bdays_check, deadline_check

INITIAL_EXTENSIONS = [
    "cogs.qc",
    "cogs.listeners",
    "cogs.commands",
    "cogs.dev",
    "cogs.games",
    "cogs.roles",
]
token = os.environ["TOKEN"]
# token = os.environ["TEST_TOKEN"]

admin = os.environ["ADMIN"]
prefix = os.getenv("PREFIX", "!")
database_url = os.environ["DATABASE_URL"]
redis_url = os.environ.get("REDISTOGO_URL", "redis://localhost:6379")
CLIENT = redis.from_url(redis_url)

intents = discord.Intents.default()
intents.members = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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
    # загрузка словаря реакций бота на определённые сообщения.
    records = await bot.pg_con.fetch("select trigger, reaction_list from add_reaction")
    bot.reaction = dict(records)
    # загрузка активностей для статуса
    statuses = await bot.pg_con.fetch("select activity from presence")
    bot.statuses = statuses

    # подготовка базы данных
    sql_path = "sql_queries"
    for file in os.listdir(sql_path):
        logger.info(f"prepare db with: {file}\n")
        with open(os.path.join(sql_path, file), encoding="utf-8", mode="r") as raw_file:
            query = raw_file.read()
            await bot.pg_con.execute(query)

    await gino_on_startup(database_url)
    await bot.change_presence(status=discord.Status.idle)
    logger.info(f"Init {bot.user.name}-{bot.user.id}\nAPI version: {discord.__version__}\nbot version: {__version__}")
    await bot.change_presence(status=discord.Status.online)
    logger.info(f"beep-boop i'm online...{bot.launch_time}!")
    logger.info("load loop tasks")
    change_status.start(bot)
    bdays_check.start(bot)
    deadline_check.start(bot, CLIENT)
    logger.info("load extension")
    if admin:
        user = bot.get_user(int(admin))
        await user.send(f"i'm online since {bot.launch_time}")

    for extension in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
            logger.info(f"load: {extension}\n")
        except Exception as e:
            logger.warning(f"Failed to load extension {extension}\n{type(e).__name__}: {e}")
    logger.info("extension loaded")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="wat"))
    else:
        logger.error(ctx.message.author, error)


if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)

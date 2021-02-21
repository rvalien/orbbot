__author__ = "Valien"
__version__ = "0.0.10"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

from discord.ext import commands

import discord
import os
import logging

INITIAL_EXTENSIONS = ["cogs.qc", "cogs.listeners", "cogs.commands"]
token = os.environ["TOKEN"]
prefix = os.environ["PREFIX"]
# token = os.environ["TEST_TOKEN"]
# prefix = "!"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("run")
bot = commands.Bot(command_prefix=prefix, description="Small bot for lil QC community")


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready"""

    print(f"Init {bot.user.name}-{bot.user.id}\nAPI version: {discord.__version__}\nbot version: {__version__}")
    game = discord.Game("Жмурки")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("beep-boop i'm online...!")
    logger.info("beep-boop i'm online...!LOGER")


if __name__ == "__main__":
    for extension in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
            logger.info(f"load: {extension}\n")
        except Exception as e:
            logger.warning(f"Failed to load extension {extension}\n{type(e).__name__}: {e}")

    bot.run(token, bot=True, reconnect=True)

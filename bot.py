__author__ = "Valien"
__version__ = "0.0.9"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

from discord.ext import commands

import os
import logging

INITIAL_EXTENSIONS = [
    "cogs.qc",
    "cogs.listeners",
    "cogs.commands"
]
token = os.environ["TOKEN"]
prefix = os.environ["PREFIX"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("run")
bot = commands.Bot(command_prefix=prefix)

for extension in INITIAL_EXTENSIONS:
    try:
        bot.load_extension(extension)
        logger.info(f"load: {extension}\n")
    except Exception as e:
        logger.warning(f"Failed to load extension {extension}\n{type(e).__name__}: {e}")

bot.run(token)

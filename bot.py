__author__ = "Valien"
__version__ = "0.0.9"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien/orbbot"

from discord.ext import commands
from discord import Game

import os
import logging
import asyncio

INITIAL_EXTENSIONS = ["cogs.qc", "cogs.listeners", "cogs.commands"]
token = os.environ["TOKEN"]
prefix = os.environ["PREFIX"]

logger = logging.getLogger(__name__)


def load_cogs(bot):
    for extension in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
            logger.info(f"load: {extension}\n")
        except Exception as e:
            logger.warning(f"Failed to load extension {extension}\n{type(e).__name__}: {e}")


class Bot(commands.Bot):
    def init(self, commands_prefix):
        commands_prefix = Bot(command_prefix=prefix)


async def on_ready(self):
    load_cogs(self)
    await asyncio.sleep(3)
    logger.info(f"\nBot run\nversion:{__version__}\n")
    await bot.change_presence(activity=Game(name="QC"))


if __name__ == "__main__":
    bot = Bot(command_prefix=prefix)
    bot.load_extension("cogs.commands")
    # orbb.remove_command('help')
    bot.run(token)

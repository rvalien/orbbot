import discord

from discord.ext import tasks
from itertools import cycle


@tasks.loop(hours=1.0)
async def change_status(self):
    status = cycle(
        ["HoMM I", "HoMM II", "HoMM III", "HoMM IV", "HoMM V", "HoMM VI", "HoMM VII", "HoMM VIII", "HoMM IX", "HoMM X"]
    )
    while not self.is_closed():
        await self.change_presence(activity=discord.Game(next(status)))

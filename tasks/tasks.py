import asyncio
import datetime
import discord
import os

from discord.ext import tasks
from moduls import random_gif
from itertools import cycle

apikey = os.environ["TENSOR_API_KEY"]
delay = int(os.environ["DELAY"])


@tasks.loop(hours=5.0)
async def change_status(self):
    status = cycle(
        ["HoMM I", "HoMM II", "HoMM III", "HoMM IV", "HoMM V", "HoMM VI", "HoMM VII", "HoMM VIII", "HoMM IX", "HoMM X"]
    )
    while not self.is_closed():
        await self.change_presence(activity=discord.Game(next(status)))


@tasks.loop(hours=5.0)
async def bdays_check(self):
    if 9 <= datetime.datetime. utcnow().hour <= 20:
        query = """
        select user_id
        from bdays
        where extract(month from bday) = (SELECT date_part('month', (SELECT current_timestamp)))
        and extract(day from bday) = (SELECT date_part('day', (SELECT current_timestamp)))
        """

        party_dude = await self.pg_con.fetchval(query)
        if party_dude:
            user = self.get_user(party_dude)
            channel = self.get_channel(774365764190732309)  # づ｡◕‿‿◕｡づ
            # channel = self.get_channel(811505442252521492)  # dev🛠

            embed = discord.Embed()
            url = random_gif(apikey, "birth day")
            embed.set_image(url=url)

            async with channel.typing():
                await asyncio.sleep(0.10)

            await channel.send(f"{user.mention} happy BD, **{user.name}**! We Love you!", embed=embed)

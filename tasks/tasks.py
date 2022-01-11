import asyncio
import datetime
import discord
import os

from discord.ext import tasks
from moduls import random_gif
from itertools import cycle

apikey = os.environ["TENSOR_API_KEY"]
delay = int(os.environ["DELAY"])

CHANNELS = {
    "books": 825411232159760405,
    "づ｡◕‿‿◕｡づ": 774365764190732309,
    "dev🛠": 811505442252521492,
}


@tasks.loop(hours=5.0)
async def change_status(self):
    status = cycle(
        ["Quake Champions", "Control", "Hollow knight", "Alien isolation", "Banner saga", "Divinity: Original sin 2"]
    )
    while not self.is_closed():
        await self.change_presence(activity=discord.Game(next(status)))


@tasks.loop(hours=5.0)
async def bdays_check(self):

    # TODO уйти от сырого sql к моделям пользователя
    if 10 <= datetime.datetime.utcnow().hour <= 20:
        query = """
        select user_id
        from bdays
        where extract(month from bday) = (SELECT date_part('month', (SELECT current_timestamp)))
        and extract(day from bday) = (SELECT date_part('day', (SELECT current_timestamp)))
        """

        party_dude = await self.pg_con.fetchval(query)
        if party_dude:
            user = self.get_user(party_dude)
            channel = self.get_channel(CHANNELS.get("づ｡◕‿‿◕｡づ"))

            embed = discord.Embed()
            url = random_gif(apikey, "birth day")
            embed.set_image(url=url)

            async with channel.typing():
                await asyncio.sleep(0.10)

            await channel.send(f"{user.mention} happy BD, **{user.name}**! We Love you!", embed=embed)


@tasks.loop(hours=6)
async def deadline_check(self, redis_client, keyword: str = "book_club_notify_timestamp"):
    """
    уведомляет о скором сроке обсуждения книг.
    Использует редис и базу данных. Очевидно можно и без редиса и в базе хранить дату последнего выполнения проверки,
    но я хотел его применить для научных целей.
    """
    channel = self.get_channel(CHANNELS.get("books"))
    utc_now = datetime.datetime.utcnow()
    timestamp = redis_client.get(keyword)
    # todo можно добавить название книги.
    if 8 <= utc_now.hour <= 15:
        if timestamp is None or datetime.datetime.fromtimestamp(int(timestamp)).date() != utc_now.date():
            days = await self.pg_con.fetchval("select deadline - current_date from book_club_deadline")
            if days and days < 0:
                await self.pg_con.execute("truncate table book_club_deadline")
            elif days and days <= 7:
                redis_client.set(keyword, int(utc_now.timestamp()))
                await channel.send(f"Дней до обсуждения: {days}")

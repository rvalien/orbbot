import asyncio
import datetime
import discord
import logging
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


@tasks.loop(hours=1)
async def deadline_check(self, redis_client):
    # channel = self.get_channel(757694875096449029) тестовый канал на тестовом сервере
    channel = self.get_channel(CHANNELS.get("books"))
    keyword = "book_club_notify_timestamp"

    utc_now = datetime.datetime.utcnow()
    timestamp = redis_client.get(keyword)

    logging.warning(f"deadline_check, {channel} {keyword} {utc_now}")

    if 8 <= utc_now.hour <= 15:
        logging.warning("10 <= utc_now.hour <= 20 TRUE")
        if timestamp is None or datetime.datetime.fromtimestamp(int(timestamp)).date() != utc_now.date():
            days = await self.pg_con.fetchval("select deadline - current_date from  book_club_deadline")
            logging.warning(f"days, {days}")
            if days and days <= 7:
                logging.info("if days and days <= 7 TRUE")
                redis_client.set(keyword, int(utc_now.timestamp()))
                await channel.send(f"Дней до обсуждения: {days}")
            logging.warning(f"days: {days}")
        logging.warning(f"timestamp: {timestamp}\nutc_now.date(): {utc_now.date()}")

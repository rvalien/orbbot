import asyncio
import logging
import random
import os

from datetime import date, datetime, timedelta
from sqlalchemy import func
from discord.ext import commands
from models.db_gino import User
from bot import CLIENT

delay = int(os.environ["DELAY"])


def correct_day_end(days: int) -> str:
    string = "дней"
    if str(days).endswith("1") and days != 11:
        string = "день"
    elif days in (2, 3, 4, 22, 23, 24):
        string = "дня"
    return string


class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def poll(self, ctx, *, question):
        """
        A simple poll with only 2 reactions (👍, 👎)
        type `poll Аm i good?` and wait.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        message = await ctx.send(f"Poll: {question} - {ctx.author}")
        for emoji in ["👍", "👎"]:
            await message.add_reaction(emoji)

    @commands.command()
    async def ping(self, ctx):
        """
        Used to check if the bot alive
        """
        await ctx.send(f"🏓 pong! {round(self.bot.latency * 1000)} ms", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def random(self, ctx, *, players: str = None):
        """
        Split input players separated by a comma to 2 teams
        $random player1, player2, player3, player4
        team 🍏: player1, player3
        team 🍎: player2, player4

        If your list hasn't changed for the last 30 minutes,
        you can reuse it by inputting `!random` command without any arguments.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        key = f"{ctx.message.author.nick}_last_random_usage"
        logging.warning(CLIENT.smembers(key))

        if players is None and len(CLIENT.smembers(key)) == 0:
            await ctx.send("Nothing to randomize. Insert items separated by commas.", delete_after=delay)
        else:
            p_list = players.split(", ") if players else list(map(lambda x: x.decode("utf-8"), CLIENT.smembers(key)))
            CLIENT.delete(key)
            CLIENT.sadd(key, *p_list)
            CLIENT.expire(key, timedelta(minutes=30))

            random.shuffle(p_list)
            separator = int(len(p_list) / 2)
            await ctx.send(
                f"**team 🍏**: {', '.join(p_list[:separator])}\n**team 🍎**: {', '.join(p_list[separator:])}",
                delete_after=delay,
            )
            await ctx.message.delete(delay=delay)

    @commands.command(aliases=["dice", "die"])
    async def roll(self, ctx):
        """
        🎲 roll dice and set result as reaction on your command
        """
        dice = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")
        die = random.choice(dice)
        await ctx.message.add_reaction(die)

    @commands.command()
    async def bday(self, ctx, *, name: str = None):
        """
        `bday` — show users birthday.
        До Дня рождения name1 осталось 1 день.
        До Дня рождения name2 осталось 11 дней.

        `bday all` — return list of all names with birthdays
        14.04   name1
        22.04   name2
        04.05   name3

        `bday <name>` — replay with date if found name in db
        14.04 or 🤷‍♂️
        """

        def day_of_year(user_object):
            return user_object.birth_date - date(user_object.birth_date.year, 1, 1)

        async with ctx.typing():
            await asyncio.sleep(0.5)

        if name and name.casefold() == "all":
            users = await User.query.gino.all()
            users.sort(key=day_of_year)

            message = "🎉🥳🥳🥳🥳🥳🥳🎉:\n"
            for user in users:
                message += f"{user.month_and_day}\t{user.user_name}\n"

            await ctx.send(message)

        elif name:
            user = await User.query.where(User.user_name.ilike(name)).gino.first()
            await ctx.reply(user.month_and_day if user else "🤷‍♂️", mention_author=False)

        else:
            current_date = datetime.utcnow()
            cur_month_users = await User.query.where(
                func.date_part("month", User.birth_date) == current_date.month
            ).gino.all()

            if cur_month_users:
                for user in cur_month_users:
                    days_left = user.birth_date.day - current_date.day
                    if days_left > 0:
                        await ctx.send(
                            f"До Дня Рождения **{user.user_name}** осталось {days_left} {correct_day_end(days_left)}."
                        )
            else:
                await ctx.send("В этом месяце - никого.")
        await ctx.message.delete(delay=delay)


async def setup(bot):
    await bot.add_cog(SimpleCommands(bot))

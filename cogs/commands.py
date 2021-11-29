import asyncio
import logging
import random
import os

from datetime import datetime, timedelta
from discord.ext import commands
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
        simple poll with only 2 reactions (👍, 👎)
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
        used to check if the bot is alive
        """
        await ctx.send(f"🏓 pong! {round(self.bot.latency * 1000)} ms", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def random(self, ctx, *, players: str = None):
        """
        split input players separated by comma to 2 teams
        $random player1, player2, player3, player4
        team 🍏: player1, player3
        team 🍎: player2, player4

        If your list hasn't been changed for the last 30 minutes,
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
        bday - show happy birthday users who are coming soon in the current month
        ``` До Дня рождения name1 осталось 1 день.
            До Дня рождения name2 осталось 11 дней.```

        bday all - return list of  all names with b
        ``` 14.04    name1
            22.04    name2
            04.05    name3```

        bday <name> - replay with date if name was found in db
        ``` 14.04 or 🤷‍♂️```
        """

        async with ctx.typing():
            await asyncio.sleep(0.5)

        if name and name.casefold() == "all":
            query = """
            select to_char(bday, 'DD.MM') as dm, user_name from bdays
            order by extract(month from bday), extract(day from bday)
            """
            rows = await self.bot.pg_con.fetch(query)
            message = "🎉🥳🥳🥳🥳🥳🥳🎉:\n"
            for row in rows:
                message += f'{row["dm"]}\t{row["user_name"]}\n'

            await ctx.send(message)

        elif name:
            query = f"select to_char(bday, 'DD.MM') as dm from bdays where lower(user_name) = '{name.casefold()}'"
            value = await self.bot.pg_con.fetchval(query)
            await ctx.reply(value if value else "🤷‍♂️", mention_author=False)

        else:
            query = """
            select raw.user_name
            , raw.day::integer
            , raw.until::integer
            from (
            select user_name
            , extract(day from bday)                                                         as day
            , extract(day from bday) - (SELECT date_part('day', (SELECT current_timestamp))) as until
            from bdays
            where extract(month from bday) = (SELECT date_part('month', (SELECT current_timestamp)))
            and extract(day from bday) > (SELECT date_part('day', (SELECT current_timestamp)))
            order by extract(day from bday) - (SELECT date_part('day', (SELECT current_timestamp)))
            ) raw;
            """

            rows = await self.bot.pg_con.fetch(query)
            for row in rows:
                await ctx.send(
                    f'До Дня рождения **{row["user_name"]}** осталось {row["until"]} {correct_day_end(row["until"])}.'
                )
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def deadline(self, ctx, date=None):
        """
        show deadline or set
        to show deadline use command `!deadline`
        to set deadline use command `!deadline 2021-12-31`
        """
        async with ctx.typing():
            if date:
                try:
                    deadline = datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError as e:
                    raise await ctx.reply(f"fuck off: {e}\n", mention_author=False)
                if datetime.utcnow().date() <= deadline:
                    await self.bot.pg_con.execute("truncate table book_club_deadline")
                    await self.bot.pg_con.execute("insert into book_club_deadline VALUES ('{0}')".format(deadline))
                    for rune in ("🇩", "🇴", "🇳", "🇪"):
                        await ctx.message.add_reaction(rune)
                else:
                    await ctx.reply("deadline: can't bee less that now", mention_author=False)
            else:
                await asyncio.sleep(0.3)
                query = "select deadline from book_club_deadline"
                value = await self.bot.pg_con.fetchval(query)
                await ctx.reply(f'deadline {value if value else "is not set"}\n', mention_author=False)
        await ctx.message.delete(delay=delay)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))

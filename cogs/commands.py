import asyncio
import random
import os

from discord.ext import commands
from discord.utils import get

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
    async def random(self, ctx, *, players: str):
        """
        split input players by space to 2 teams
        $random player1 player2 player3 player4
        team 🍏: player1, player3
        team 🍎: player2, player4
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        players_list = players.split(" ")
        random.shuffle(players_list)
        separator = int(len(players_list) / 2)
        await ctx.send(
            f"**team 🍏**: {', '.join(players_list[:separator])}\n**team 🍎**: {', '.join(players_list[separator:])}",
            delete_after=delay,
        )
        await ctx.message.delete(delay=delay)

    @commands.command(aliases=["dice", "die"])
    async def roll(self, ctx):
        """
        roll dice and set as reaction on your command
        """
        dice = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")
        die = random.choice(dice)
        await ctx.message.add_reaction(die)

    @commands.command()
    async def migrate(self, ctx):
        """
        move all voice members to another channel
        """
        voice_channel = ctx.message.author.voice.channel
        all_members = voice_channel.members
        voice_channel_list = ctx.guild.voice_channels
        empty_channel = next(filter(lambda x: not x.members, voice_channel_list))
        for member in all_members:
            await member.move_to(empty_channel)
            await member.move_to(voice_channel)

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
    # @commands.is_owner()
    # @commands.has_permissions(administrator=True)
    async def role(self, ctx, name: str = None):
        member = ctx.message.author
        allowed_roles = (845598058389700608, 845956928185565184)

        if name:
            role = get(ctx.guild.roles, name=name)
            if role.id in allowed_roles and role not in member.roles:
                await ctx.send(f"add role {role.name} to {member.name}")
                await member.add_roles(role)

            elif role in member.roles:
                await ctx.send(f"remove role {role.name} from {member.name}")
                await member.remove_roles(role)

        else:
            yr = set(member.roles)
            ar = list(set(ctx.guild.roles) - yr)
            ar = list(filter(lambda x: x.id in allowed_roles, ar))

            yr = "\n".join(list(map(lambda x: x.name, member.roles)))
            ar = "\n".join(list(map(lambda x: x.name, ar)))
            await ctx.send(f"Allowed roles:\n`{ar}`\n\nYour roles:\n`{yr}`")


def setup(bot):
    bot.add_cog(SimpleCommands(bot))

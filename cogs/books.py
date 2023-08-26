import asyncio
import os
import random

from datetime import datetime
from discord.ext import commands
from moduls import get_members_voice

delay = int(os.environ["DELAY"])


class BookClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deadline(self, ctx, date=None):
        """
        Show deadline or set
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
                await asyncio.sleep(0.1)
                query = "select deadline from book_club_deadline"
                value = await self.bot.pg_con.fetchval(query)
                await ctx.reply(f'deadline {value if value else "is not set"}\n', mention_author=False)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def order(self, ctx):
        voice_channel = None
        try:
            voice_channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f"You are not in voice channel", delete_after=delay)

        if voice_channel:
            all_members = get_members_voice(ctx)
            if all_members:
                random.shuffle(all_members)
                await ctx.send(f'\n**order**: {", ".join(all_members)}\n', delete_after=delay)
            else:
                await ctx.send(f"\nIs there anyone alive in {voice_channel}?\n", delete_after=delay)
        await ctx.message.delete(delay=delay)


async def setup(bot):
    await bot.add_cog(BookClub(bot))

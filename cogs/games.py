import asyncio
import random
import discord
from discord.ext import commands


class SimpleGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


@commands.command()
async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
    """ Give someone a beer! 🍻 """
    if not user or user.id == ctx.author.id:
        return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
    if user.id == self.bot.user.id:
        return await ctx.send("*drinks beer with you* 🍻")
    if user.bot:
        return await ctx.send(
            f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/"
        )

    beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
    beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
    msg = await ctx.send(beer_offer)

    def reaction_check(m):
        if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
            return True
        return False

    try:
        await msg.add_reaction("🍻")
        await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
        await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
    except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
    except discord.Forbidden:
        # Yeah so, bot doesn't have reaction permission, drop the "offer" word
        beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        await msg.edit(content=beer_offer)


@commands.command(aliases=["slots", "bet"])
@commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
async def slot(self, ctx):
    """ Roll the slot machine """
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)

    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

    if a == b == c:
        await ctx.send(f"{slotmachine} All matching, you won! 🎉")
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
    else:
        await ctx.send(f"{slotmachine} No match, you lost 😢")


def setup(bot):
    bot.add_cog(SimpleGames(bot))

import asyncio
import os
import sys
import discord

from discord.ext import commands
from moduls import random_gif, random_map

print("init bot")
if sys.platform == "win32":
    from config import *

    print("local execute")

token = os.environ["TOKEN"]
apikey = os.environ["TENSOR_API_KEY"]


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """show server description for new member"""
        text = """
✨{0.mention}✨, welcome to QC community for normal (mostly) players.\nWe love custom games: ⛳, 💈, duels\nlang: 🇩🇪 🇷🇺 🇬🇧
"""
        channel = member.guild.system_channel
        embed = discord.Embed()
        url = random_gif(apikey, "hello")
        embed.set_image(url=url)

        if channel is not None:
            async with channel.typing():
                await asyncio.sleep(0.5)
            await channel.send(text.format(member), embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Says goodbye"""
        text = f"""
{member.mention} left us 🥺. We should find him and punish 👺.({str(member)}{member.display_name}{member.nick})
Считаю, что он ушёл очень больно. Считаю, что он мучался в всвоём отключении. Жаль, конечно, этого добряка.
Конечно, он со мной не играл... Пару игр он со мной поиграл, все равно жалко его. Хороший был человек
"""
        channel = member.guild.system_channel
        embed = discord.Embed()
        url = random_gif(apikey, "bye")
        embed.set_image(url=url)
        if channel is not None:
            async with channel.typing():
                await asyncio.sleep(0.5)
            await channel.send(text.format(member), embed=embed)

    @commands.command()
    async def hi(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        channel = member.guild.system_channel
        async with channel.typing():
            await asyncio.sleep(0.5)
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Hello {0.name}~".format(member))
        else:
            await ctx.send("Hello {0.name}... This feels familiar.".format(member))

    @commands.command()
    async def profile(self, ctx, *, member=None):
        """show link to qc profile"""
        if member:
            await ctx.send(f"https://stats.quake.com/profile/{member}")
        else:
            await ctx.send("nickname not set. Try: `$profile clawz`")

    @commands.command()
    async def orbb(self, ctx, *, member: discord.Member = None):
        """orbb info"""
        # member = member or ctx.author
        # channel = member.guild.system_channel
        # embed = discord.Embed()
        # url = random_gif("what?")
        # embed.set_image(url=url)

        # if channel is not None:
        #     async with channel.typing():
        #         await channel.send(embed=embed)

        await ctx.send(
            "I'm **Orbb**. I can do:\n😸 show quake profile link `$profile somename`\n😻 chose random map `$rmap`\n🙀 just hello `$hi`"
        )

    @commands.command()
    async def rmap(self, ctx, *, member: discord.Member = None):
        """orbb info"""
        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")


bot = commands.Bot(command_prefix="$")
bot.add_cog(Greetings(bot))
bot.run(token)

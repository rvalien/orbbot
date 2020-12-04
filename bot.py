import asyncio
import os
import sys
import discord
import random
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
        nicks = f"{str(member)} "

        if member.display_name:
            nicks += f"{member.display_name} "

        if member.nick:
            nicks += f"{member.nick}"
        text = f"""
{member.mention} ({nicks}) left us 🥺. We should find him and punish 👺.

Считаю, что он ушёл очень больно.
Считаю, что он мучался в всвоём отключении.
Жаль, конечно, этого добряка.
Конечно, он со мной не играл... Пару игр он со мной поиграл, все равно жалко его.
Хороший был человек.
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
        await ctx.send(
            "I'm **Orbb**. I can do:\n"
            "👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 shuffle members of voice channel to 2 teams `$team`\n"
            "😸 show quake profile link `$profile somename`\n"
            "🗺️ chose random map `$map`\n"
            "🤓 chose random spectator from voice chat users `$spec`\n"
            "👋 just hello `$hi`"
        )

    @commands.command()
    async def map(self, ctx, *, member: discord.Member = None):
        """orbb info"""
        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")

    @commands.command()
    async def team(self, ctx, *, member: discord.Member = None):
        """orbb info"""
        if ctx.message.author.voice:
            print(ctx.message.author.voice.channel.members)
            voice_channel = ctx.message.author.voice.channel
            all_members = voice_channel.members
            print(voice_channel)
            print(all_members)
            random.shuffle(all_members)
            random.shuffle(all_members)
            separator = len(all_members) // 2
            team1 = list(all_members[:separator])
            team2 = list(all_members[separator:])
            if team1:
                await ctx.send(
                    f'**team** 🌻: {", ".join(map(lambda x: x.name, team1))}',
                    tts=False,
                )
            if team2:
                await ctx.send(
                    f'**team** ❄️: {", ".join(map(lambda x: x.name, team2))}',
                    tts=False,
                )
        else:
            await ctx.send("voice channel is empty", tts=False)


bot = commands.Bot(command_prefix="$")
bot.add_cog(Greetings(bot))
bot.run(token)

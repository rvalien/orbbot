import asyncio
import os
import sys
import discord
import random
import time
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

    @commands.command()
    async def hi(self, ctx, *, member: discord.Member = None):
        """👋 just hello"""
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
        """😸 show quake profile link `$profile somename`"""
        if member:
            await ctx.send(f"https://stats.quake.com/profile/{member}")
        else:
            await ctx.send("nickname not set. Try: `$profile clawz`")

    @commands.command()
    async def map(self, ctx, *, member: discord.Member = None):
        """"🗺️ chose random map"""
        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")

    @commands.command()
    async def team(self, ctx, *, member: discord.Member = None):
        """👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 shuffle members of voice channel to 2 teams"""
        if ctx.message.author.voice:
            voice_channel = ctx.message.author.voice.channel
            all_members = voice_channel.members
            print(all_members)
            if not all_members:
                await ctx.send("🤖 beep boop.. need more time to calculate")
            else:
                random.shuffle(all_members)
                random.shuffle(all_members)
                separator = len(all_members) // 2
                team1 = list(all_members[:separator])
                team2 = list(all_members[separator:])

                await ctx.send(f"let's shuffle all persons from **{voice_channel}** voice channel", tts=False)

                if team1:
                    await ctx.send(f'**team** 🌻: {", ".join(map(lambda x: x.name, team1))}', tts=False)
                if team2:
                    await ctx.send(f'**team** ❄️: {", ".join(map(lambda x: x.name, team2))}', tts=False)
        else:
            await ctx.send("voice channel is empty", tts=False)

    @commands.command()
    async def spec(self, ctx, *, member: discord.Member = None):
        """Spectator random choice if player more than 8"""
        # await ctx.send("who wanna play?")

        msg = await ctx.channel.send("Who wanna play now? Add you reaction bellow ⬇️")
        for emoji in ['✅', '❌']:
            await msg.add_reaction(emoji)
        await asyncio.sleep(20)
        msg = await ctx.channel.fetch_message(msg.id)
        # get reactors who react first emoji
        reactors = await msg.reactions[0].users().flatten()
        # remove bots
        reactors = list(filter(lambda x: not x.bot, reactors))

        if len(reactors) > 8:
            random.shuffle(reactors)
            players = reactors[:8]
            specs = reactors[8:]
            await ctx.channel.send(f"{', '.join([x.name for x in specs])}  it's ☕ time!")
        else:
            embed = discord.Embed()
            url = random_gif(apikey, random.choice(["everyone", "war"]))
            embed.set_image(url=url)
            await ctx.channel.send(f"Everyone can play!\n{[x.name for x in reactors]}",  embed=embed)


bot = commands.Bot(command_prefix="$")
bot.add_cog(Greetings(bot))
bot.run(token)

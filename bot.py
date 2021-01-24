__author__ = "Valien"
__version__ = "0.0.6"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien"

from discord.ext import commands
from moduls import random_gif, random_map

import asyncio
import discord
import os
import random
import logging

token = os.environ["TOKEN"]
apikey = os.environ["TENSOR_API_KEY"]

logger = logging.getLogger(__name__)


class OrbbCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def profile(self, ctx, *, member=None):
        """😸 Show quake profile link `$profile some_name`"""
        if member:
            await ctx.send(f"https://stats.quake.com/profile/{member}")
        else:
            await ctx.send("nickname not set. Try: `$profile clawz`")

    @commands.command()
    async def map(self, ctx, *, member: discord.Member = None):
        """🗺️ Choose random map"""
        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")

    @commands.command()
    async def team(self, ctx, *, anything=None):
        """👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 Shuffles members into 2 teams. See more with `$help team`
        You can type any word or number as a message after `$team` command.
        If message passed: Bot sends a message and shuffles members who react with emoji on it.
        If message not passed: Bot shuffles members from voice channel."""
        if not anything:
            msg = await ctx.channel.send("@here Who wanna play now? Add you reaction bellow ⬇️")
            for emoji in ["✅", "❌"]:
                await msg.add_reaction(emoji)
            await asyncio.sleep(20)
            msg = await ctx.channel.fetch_message(msg.id)
            # get reactors who react first emoji
            logger.info(msg.reactions, msg.reactions[0].users().flatten(), msg.reactions[1].users().flatten())
            reactors = await msg.reactions[0].users().flatten()
            # remove bots
            reactors = list(filter(lambda x: not x.bot, reactors))
            # get only names
            all_members = list(map(lambda x: x.name, reactors))

            if not all_members:
                await ctx.send("🤖 beep boop.. no one wants")
            else:
                random.shuffle(all_members)
                random.shuffle(all_members)  # double random
                separator = len(all_members) // 2
                team1 = list(all_members[:separator])
                team2 = list(all_members[separator:])
                await ctx.send("let's shuffle all persons who react my message", tts=False)
                if team1:
                    await ctx.send(f'**team** 🌻: {", ".join(team1)}', tts=False)
                if team2:
                    await ctx.send(f'**team** ❄️: {", ".join(team2)}', tts=False)

        else:
            if ctx.message.author.voice:
                voice_channel = ctx.message.author.voice.channel
                all_members = voice_channel.members
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
        """If player more than 8, 👁️bot choose random spectators. """

        msg = await ctx.channel.send("@here Who wanna play? Add you reaction bellow ⬇️")
        for emoji in ["✅", "❌"]:
            await msg.add_reaction(emoji)
        await asyncio.sleep(20)
        msg = await ctx.channel.fetch_message(msg.id)
        # get reactors who react first emoji
        reactors = await msg.reactions[0].users().flatten()
        logger.info(msg.reactions, msg.reactions[0].users().flatten(), msg.reactions[1].users().flatten())
        # remove bots
        reactors = list(filter(lambda x: not x.bot, reactors))
        # get only names
        reactors = list(map(lambda x: x.name, reactors))
        embed = discord.Embed()
        url = random_gif(apikey, random.choice(["everyone", "war"]))
        embed.set_image(url=url)
        if len(reactors) > 8:
            random.shuffle(reactors)
            players = reactors[:8]
            specs = reactors[8:]
            await ctx.channel.send(f"Lucky ones: {', '.join(players)}\nIt's ☕ time for {', '.join(specs)}", embed=embed)
        else:
            await ctx.channel.send(f"Everyone can play!\n{', '.join(reactors)}", embed=embed)

    @commands.command()
    async def pzdc(self, ctx, *, member: discord.Member = None):
        """это пиздец"""

        heroes = [
            "Anarki",
            "Athena",
            "B.J. Blazkowicz",
            "Clutch",
            "Death Knight",
            "Doom Slayer",
            "Eisen",
            "Galena",
            "Keel",
            "Nyx",
            "Ranger",
            "ScaleBearer",
            "Slash",
            "Sorlag",
            "Strogg & Peeker",
            "Visor",
        ]
        if ctx.message.author.voice:
            voice_channel = ctx.message.author.voice.channel
            all_members = voice_channel.members
            if not all_members:
                await ctx.send("🤖 beep boop.. need more time to calculate")
            else:
                all_members = list(filter(lambda x: not x.bot, all_members))
                all_members = list(map(lambda x: x.name, all_members))
                random.shuffle(all_members)
                random.shuffle(heroes)
                separator = len(all_members) // 2
                team1 = list(all_members[:separator])
                team1 = [list(tup) for tup in zip(team1, heroes[:separator])]
                team1 = list(map(lambda x: " = ".join(x), team1))
                random.shuffle(heroes)
                team2 = list(all_members[separator:])
                team2 = [list(tup) for tup in zip(team2, heroes[:separator])]
                team2 = list(map(lambda x: " = ".join(x), team2))

                await ctx.send(f"let's shuffle all persons from **{voice_channel}** voice channel", tts=False)
                if team1:
                    await ctx.send(f'**team** 🌻: {", ".join(team1)}', tts=False)
                if team2:
                    await ctx.send(f'**team** ❄️: {", ".join(team2)}', tts=False)
            icon, text = random_map()
            await ctx.send(f"{icon}\n{text}")
        else:
            await ctx.send("voice channel is empty", tts=False)


logger.info("run")
bot = commands.Bot(command_prefix="$")
bot.add_cog(OrbbCommands(bot))
bot.run(token)

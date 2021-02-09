__author__ = "Valien"
__version__ = "0.0.6"
__maintainer__ = "Valien"
__link__ = "https://github.com/rvalien"

from discord.ext import commands
from moduls import random_gif, random_map, text_formatter, get_members_voice

import asyncio
import discord
import os
import random
import logging

token = os.environ["TOKEN"]
apikey = os.environ["TENSOR_API_KEY"]

logger = logging.getLogger(__name__)

VOTE_REACT = {"yes": "✅", "no": "❌", "time": "🔟", "half_time": "5️⃣", "stop": "🛑"}
VOTE_TIME = 10
HEROES = [
    {"name": "Anarki", "emoji": "Anarki"},
    {"name": "Athena", "emoji": "Athena"},
    {"name": "B.J. Blazkowicz", "emoji": "BJ"},
    {"name": "Clutch", "emoji": "Clutch"},
    {"name": "Death Knight", "emoji": "DeathKnight"},
    {"name": "Doom Slayer", "emoji": "Doom"},
    {"name": "Eisen", "emoji": "Eisen"},
    {"name": "Galena", "emoji": "Galena"},
    {"name": "Keel", "emoji": "Keel"},
    {"name": "Nyx", "emoji": "Nyx"},
    {"name": "Ranger", "emoji": "Ranger"},
    {"name": "ScaleBearer", "emoji": "Scalebearer"},
    {"name": "Slash", "emoji": "Slash"},
    {"name": "Sorlag", "emoji": "Sorlag"},
    {"name": "Strogg", "emoji": "Strogg"},
    {"name": "Visor", "emoji": "Visor"},
]


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
    async def map(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        """🗺️ Choose random map"""
        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")

    @commands.command()
    async def team(self, ctx, *, anything=None, time=VOTE_TIME):
        """👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 Shuffles members into 2 teams. See more with `$help team`
        You can type any word or number as a message after `$team` command.
        If message passed: Bot sends a message and shuffles members who react with emoji on it.
        If message not passed: Bot shuffles members from voice channel."""
        if not anything:
            async with ctx.typing():
                await asyncio.sleep(1)
            msg = await ctx.channel.send(
                f"""@here Who wanna play now? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)"""
            )
            for emoji in [VOTE_REACT.get("yes"), VOTE_REACT.get("no"), VOTE_REACT.get("time")]:
                await msg.add_reaction(emoji)
            await asyncio.sleep(time / 2)
            msg = await ctx.channel.fetch_message(msg.id)
            await msg.remove_reaction(emoji=VOTE_REACT.get("time"), member=msg.author)
            await msg.add_reaction(emoji=VOTE_REACT.get("half_time"))
            await asyncio.sleep(time / 2)
            await msg.remove_reaction(emoji=VOTE_REACT.get("half_time"), member=msg.author)
            await msg.add_reaction(VOTE_REACT.get("stop"))
            # get reactors who react first emoji
            logger.info(msg.reactions, msg.reactions[0].users().flatten(), msg.reactions[1].users().flatten())
            reactors = await msg.reactions[0].users().flatten()
            # remove bots
            reactors = list(filter(lambda x: not x.bot, reactors))
            # get only names
            all_members = list(map(lambda x: x.name, reactors))
            # voice_members = get_members_voice(ctx)
            if not all_members:
                await ctx.send("🤖 beep boop.. no one wants")
            else:
                random.shuffle(all_members)
                random.shuffle(all_members)  # double random
                separator = len(all_members) // 2
                team1 = list(all_members[:separator])
                team2 = list(all_members[separator:])
                await ctx.send("let's shuffle all persons who **react** my message", tts=False)
                if team1:
                    await ctx.send(f'\n**team** 🌻: {", ".join(team1)}', tts=False)
                if team2:
                    await ctx.send(f'\n**team** ❄️: {", ".join(team2)}', tts=False)

        else:
            if ctx.message.author.voice:
                voice_channel = ctx.message.author.voice.channel
                all_members = voice_channel.members
                if not all_members:
                    async with ctx.typing():
                        await asyncio.sleep(1)
                    await ctx.send("🤖 beep boop.. need more time to calculate")
                else:
                    random.shuffle(all_members)
                    random.shuffle(all_members)
                    separator = len(all_members) // 2
                    team1 = list(all_members[:separator])
                    team2 = list(all_members[separator:])
                    async with ctx.typing():
                        await asyncio.sleep(1)
                    await ctx.send(f"let's shuffle all persons from **{voice_channel}** voice channel", tts=False)
                    if team1:
                        await ctx.send(f'\n**team** 🍄: {", ".join(map(lambda x: x.name, team1))}', tts=False)
                    if team2:
                        await ctx.send(f'\n**team** 🍁: {", ".join(map(lambda x: x.name, team2))}', tts=False)
            else:
                await ctx.send("voice channel is empty", tts=False)

    @commands.command()
    async def spec(self, ctx, *, time=VOTE_TIME):
        """If player more than 8, 👁️bot choose random spectators. """
        async with ctx.typing():
            await asyncio.sleep(1)
        msg = await ctx.channel.send(
            f"""@here Who wanna play now? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)"""
        )
        for emoji in [VOTE_REACT.get("yes"), VOTE_REACT.get("no"), VOTE_REACT.get("time")]:
            await msg.add_reaction(emoji)
        await asyncio.sleep(time / 2)
        msg = await ctx.channel.fetch_message(msg.id)
        await msg.remove_reaction(emoji=VOTE_REACT.get("time"), member=msg.author)
        await msg.add_reaction(emoji=VOTE_REACT.get("half_time"))
        await asyncio.sleep(time / 2)
        await msg.remove_reaction(emoji=VOTE_REACT.get("half_time"), member=msg.author)
        await msg.add_reaction(VOTE_REACT.get("stop"))
        msg = await ctx.channel.fetch_message(msg.id)
        # get reactors who react first emoji
        reactors = await msg.reactions[0].users().flatten()
        logger.info(msg.reactions, msg.reactions[0].users().flatten(), msg.reactions[1].users().flatten())
        # remove bots
        reactors = list(filter(lambda x: not x.bot, reactors))
        # get only names
        reactors = list(map(lambda x: x.name, reactors))
        embed = discord.Embed()
        url = random_gif(apikey, random.choice(["team play", "fight", "war"]))
        embed.set_image(url=url)
        if len(reactors) > 8:
            random.shuffle(reactors)
            players = reactors[:8]
            specs = reactors[8:]
            await ctx.channel.send(f"Lucky ones: {', '.join(players)}\nIt's ☕ time for {', '.join(specs)}", embed=embed)
        else:
            await ctx.channel.send(f"Everyone can play!\n{', '.join(reactors)}", embed=embed)

    @commands.command()
    async def pzdc(self, ctx, *, time=VOTE_TIME):
        """random map, character and team shuffle"""
        # all_members = get_members_voice(ctx)
        async with ctx.typing():
            await asyncio.sleep(1)
        msg = await ctx.channel.send(
            f'@here Who wanna play **PIZDEC**? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)'
        )
        for emoji in [VOTE_REACT.get("yes"), VOTE_REACT.get("no"), VOTE_REACT.get("time")]:
            await msg.add_reaction(emoji)
        await asyncio.sleep(time / 2)
        msg = await ctx.channel.fetch_message(msg.id)
        await msg.remove_reaction(emoji=VOTE_REACT.get("time"), member=msg.author)
        await msg.add_reaction(emoji=VOTE_REACT.get("half_time"))
        await asyncio.sleep(time / 2)
        await msg.remove_reaction(emoji=VOTE_REACT.get("half_time"), member=msg.author)
        await msg.add_reaction(VOTE_REACT.get("stop"))
        msg = await ctx.channel.fetch_message(msg.id)
        reactors = await msg.reactions[0].users().flatten()
        reactors = list(filter(lambda x: not x.bot, reactors))
        all_members = list(map(lambda x: x.name, reactors))

        emojies = list(map(lambda x: x.get("emoji"), HEROES))
        emojies = list(map(lambda x: discord.utils.get(bot.emojis, name=x), emojies))
        emojies = list(map(str, emojies))
        random.shuffle(all_members)

        separator = len(all_members) // 2

        team1 = list(all_members[:separator])
        team2 = list(all_members[separator:])

        random.shuffle(emojies)
        team1 = [list(tup) for tup in zip(team1, emojies[:separator])]

        random.shuffle(emojies)
        team2 = [list(tup) for tup in zip(team2, emojies[: len(team2)])]

        await ctx.send(f"\n**team** ❄️:\n{text_formatter(team1)}\n", tts=False)
        await ctx.send(f"\n**team** 🌻:\n{text_formatter(team2)}\n", tts=False)

        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")


logger.info("run")
bot = commands.Bot(command_prefix="$")
bot.add_cog(OrbbCommands(bot))
bot.run(token)

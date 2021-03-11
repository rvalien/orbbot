"""
commands for QC game
"""

import asyncio
import discord
import os
import random
import logging

from discord.ext import commands
from moduls import random_gif, random_map, text_formatter, get_random_spectators_and_players, get_members_voice, HEROES

apikey = os.environ["TENSOR_API_KEY"]
VOTE_REACT = {"yes": "✅", "no": "❌", "time": "🔟", "half_time": "5️⃣", "stop": "🛑"}
VOTE_TIME = 10

logger = logging.getLogger(__name__)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def profile(self, ctx, *, member=None):
        """
        😸 Show quake profile link `$profile some_name`
        """
        if member:
            await ctx.send(f"https://stats.quake.com/profile/{member}")
        else:
            await ctx.send("nickname not set. Try: `$profile clawz`")

    @commands.command()
    async def map(self, ctx):
        """
        🗺️ Choose random map
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")

    @commands.command()
    async def team(self, ctx, *, players=None, time: int = VOTE_TIME):
        """
        Shuffles members into 2 teams and spectators. See more with `$help team`
        3 types of use:
          * type `team` Bot sends a message and shuffles members who react with emoji on it.
          * type `team and any letter or number or word shorter than 3 chars`. Bot calculate members from voice channel
          * type `team player1 player2` bot calculate members from voice channel and player names from message
        """
        voice_channel = ctx.message.author.voice.channel
        if not players:
            async with ctx.typing():
                await asyncio.sleep(0.5)
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
            reactors = await msg.reactions[0].users().flatten()
            # remove bots
            reactors = list(filter(lambda x: not x.bot, reactors))
            # get only names
            all_members = list(map(lambda x: x.name, reactors))
            await ctx.send("let's shuffle all persons who **react** my message")
        else:
            all_members = get_members_voice(ctx)
            if len(players) > 3:
                await ctx.send(f"let's shuffle all persons from **{voice_channel}** voice channel")
                players_list = players.split(" ")
                all_members += players_list

        if all_members:
            players, spectators = get_random_spectators_and_players(all_members)
            separator = int(len(players) / 2)
            team1 = list(players[:separator])
            team2 = list(players[separator:])

            if team1:
                await ctx.send(f'\n**team** 🌻: {", ".join(team1)}\n')
            if team2:
                await ctx.send(f'\n**team** ❄️: {", ".join(team2)}\n')
            if spectators:
                await ctx.send(f"\nIt's ☕ time for {', '.join(spectators)}\n")
        else:
            await ctx.send(f"\nIs there anyone alive in {voice_channel}?\n")

    @commands.command()
    async def spec(self, ctx, *, time: int = VOTE_TIME):
        """
        If player more than 8, 👁️bot choose random spectators.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)
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
        # remove bots
        reactors = list(filter(lambda x: not x.bot, reactors))
        # get only names
        reactors = list(map(lambda x: x.name, reactors))
        players, spectators = get_random_spectators_and_players(reactors)
        logger.info(f"command spec:\n{reactors=}\n{players=}\n{spectators=}\n")

        embed = discord.Embed()
        url = random_gif(apikey, random.choice(["team play", "fight", "war"]))
        embed.set_image(url=url)

        spec_mess = (f"Lucky ones: {', '.join(players)}\nIt's ☕ time for {', '.join(spectators)}",)
        no_spec_mess = (f"Everyone can play!\n{', '.join(players)}",)
        logger.info(f"command spec\n, {reactors=}\n{players=}\n{spectators}\n")
        await ctx.channel.send(spec_mess if spectators else no_spec_mess, embed=embed)

    @commands.command()
    async def pzdc(self, ctx, *, time: int = VOTE_TIME):
        """
        random map, character and team shuffle
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)
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

        emojis = list(map(lambda x: x.get("emoji"), HEROES))
        emojis = list(map(lambda x: discord.utils.get(self.bot.emojis, name=x), emojis))
        emojis = list(map(str, emojis))

        players, spectators = get_random_spectators_and_players(all_members)
        separator = int(len(players) / 2)
        team1 = list(players[:separator])
        team2 = list(players[separator:])

        random.shuffle(emojis)
        team1 = [list(tup) for tup in zip(team1, emojis[:separator])]

        random.shuffle(emojis)
        team2 = [list(tup) for tup in zip(team2, emojis[: len(team2)])]
        logger.info(f"command pzdc:\n{all_members=}\n{players=}\n{spectators=}\n")
        await ctx.send(f"\n**team** ❄️:\n{text_formatter(team1)}\n")
        await ctx.send(f"\n**team** 🌻:\n{text_formatter(team2)}\n")
        if spectators:
            await ctx.send(f"\nIt 's ☕ time for {', '.join(spectators)}")

        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}")


def setup(bot):
    bot.add_cog(Commands(bot))

"""
Commands for QC game
"""

import asyncio
import discord
import os
import random
import logging

from discord.ext import commands
from moduls import (
    generate_team_image,
    get_members_voice,
    get_random_spectators_and_players,
    HEROES,
    random_gif,
    random_map,
    text_formatter,
)

apikey = os.environ["TENSOR_API_KEY"]
VOTE_REACT = {"yes": "✅", "no": "❌", "time": "🔟", "half_time": "5️⃣", "stop": "🛑"}
delay = int(os.environ["DELAY"])
VOTE_TIME = 10

logger = logging.getLogger(__name__)


class QcCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def profile(self, ctx, *, member=None):
        """
        😸 Show quake profile link `$profile some_name`, or it will use your discord nickname.
        """
        p = member if member else ctx.author.nick
        await ctx.send(f"https://quake-stats.bethesda.net/profile/{p}", delete_after=delay)
        await ctx.send(f"https://dev.quake-champions.com/profile/{p}", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def map(self, ctx):
        """
        🗺️ Choose a random map.
        Church of Azathoth", "Tempest Shrine", "Lockbox", "Burial Chamber", "Ruins of Sartnath", "Blood Covenant"
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)

        icon, text = random_map()
        await ctx.send(f"{icon}\n{text}", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command(aliases=["team"])
    async def voice(self, ctx, *, players=None):
        """
        Shuffles members into 2 teams and spectators. See more with `$help team`
        2 types of use:
          * type `voice` — Bot calculate members from voice channel
          * type `voice player1, player2` — bot calculate members from voice channel and player names from a message.
        """
        voice_channel = None
        try:
            voice_channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f"You are not in voice channel", delete_after=delay)

        if voice_channel:
            all_members = get_members_voice(ctx)
            if players is not None and len(players) > 3:
                await ctx.send(f"let's shuffle all persons from **{voice_channel}** voice channel", delete_after=delay)
                players_list = players.split(", ")
                all_members += players_list

            if all_members:
                players, spectators = get_random_spectators_and_players(all_members)
                separator = int(len(players) / 2)
                team1 = list(players[:separator])
                team2 = list(players[separator:])

                if team1:
                    await ctx.send(f'\n**team** 🌻: {", ".join(team1)}\n', delete_after=delay)
                if team2:
                    await ctx.send(f'\n**team** ❄️: {", ".join(team2)}\n', delete_after=delay)
                if spectators:
                    await ctx.send(f"\nIt's ☕ time for {', '.join(spectators)}\n", delete_after=delay)
            else:
                await ctx.send(f"\nIs there anyone alive in {voice_channel}?\n", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def vote(self, ctx, *, time: int = VOTE_TIME):
        """
        Shuffles members into 2 teams and spectators. See more with `$help vote`
          Type `vote` Bot sends a message and shuffles members who react with an emoji on it.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)
        msg = await ctx.channel.send(
            f'Who wanna play now? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)',
            delete_after=delay,
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
        await ctx.send("let's shuffle all persons who **react** my message", delete_after=delay)
        if all_members:
            players, spectators = get_random_spectators_and_players(all_members)
            separator = int(len(players) / 2)
            team1 = list(players[:separator])
            team2 = list(players[separator:])

            if team1:
                await ctx.send(f'\n**team** 🌻: {", ".join(team1)}\n', delete_after=delay)
            if team2:
                await ctx.send(f'\n**team** ❄️: {", ".join(team2)}\n', delete_after=delay)
            if spectators:
                await ctx.send(f"\nIt's ☕ time for {', '.join(spectators)}\n", delete_after=delay)
        await ctx.message.delete(delay=delay)

    @commands.command()
    async def spec(self, ctx, *, time: int = VOTE_TIME):
        """
        If player more than 8, 👁️bot choose random spectators.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)
        msg = await ctx.channel.send(
            f'Who wanna play now? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)',
            delete_after=delay,
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

        spec_mess = f"Lucky ones: {', '.join(players)}\nIt's ☕ time for {', '.join(spectators)}"
        no_spec_mess = (f"Everyone can play!\n{', '.join(players)}",)
        logger.info(f"command spec\n, {reactors=}\n{players=}\n{spectators}\n")
        await ctx.channel.send(spec_mess if spectators else no_spec_mess, embed=embed, delete_after=delay)

    @commands.command(aliases=["пиздец"])
    async def pzdc(self, ctx, *, time: int = VOTE_TIME):
        """
        Random character and team shuffle.
        Bot separate every one, who react on this message to two teams.
        Return images with characters and names who should play that characters.
        """
        async with ctx.typing():
            await asyncio.sleep(0.5)
        msg = await ctx.channel.send(
            f'Who wanna play **PIZDEC**? Add you reaction bellow ⬇️ ({VOTE_REACT.get("time")} seconds to vote)',
            delete_after=delay,
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

        players, spectators = get_random_spectators_and_players(all_members)

        # make short names
        players = list(map(lambda x: f"{x[:10]}..." if len(x) >= 13 else x, players))
        random.shuffle(players)
        separator = int(len(players) / 2)
        team1 = list(players[:separator])
        team2 = list(players[separator:])
        emojis = list(map(lambda x: x.get("patch"), HEROES))
        random.shuffle(emojis)
        generate_team_image(emojis[:separator], team1)
        await ctx.send("team 1", file=discord.File("team.png"), delete_after=delay)
        random.shuffle(emojis)
        generate_team_image(emojis[: len(team2)], team2)
        await ctx.send("team 2", file=discord.File("team.png"), delete_after=delay)

        if spectators:
            await ctx.send(f"\nIt's ☕ time for {', '.join(spectators)}", delete_after=delay)


def setup(bot):
    bot.add_cog(QcCommands(bot))

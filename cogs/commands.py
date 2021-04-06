import asyncio
import json
import random
import requests

from discord.ext import commands


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
        await ctx.send(f"🏓 pong! {round(self.bot.latency * 1000)} ms")

    @commands.command(aliases=["привет", "эй"])
    async def talk(self, ctx, *, question):

        url = "https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict"
        payload = {"text": question}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        await ctx.send(response.json()["predictions"])

    @commands.command()
    @commands.is_owner()
    async def debug(self, ctx):
        voice_channel = ctx.message.author.voice.channel
        all_members = voice_channel.members
        voice_channel_list = ctx.guild.voice_channels
        print(voice_channel_list)
        print(voice_channel)
        print(dir(voice_channel))

        # await ctx.send(dir(ctx))
        # await ctx.send(ctx.channel.id)

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
            f"**team 🍏**: {', '.join(players_list[:separator])}\n**team 🍎**: {', '.join(players_list[separator:])}"
        )

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


def setup(bot):
    bot.add_cog(SimpleCommands(bot))

import asyncio
import discord
from discord.ext import commands
from moduls import random_gif
import config


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        text = """
✨{0.mention}✨, welcome to QC community for normal (mostly) players.\nWe love custom games: ⛳, 💈, duels\nlang: 🇩🇪 🇷🇺 🇬🇧
"""
        channel = member.guild.system_channel
        embed = discord.Embed()
        url = random_gif("hello")
        embed.set_image(url=url)

        if channel is not None:
            async with channel.typing():
                await asyncio.sleep(0.5)
            await channel.send(text.format(member), embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        text = """
{0.mention} left us 🥺. We should find him and punish 👺
"""
        channel = member.guild.system_channel
        embed = discord.Embed()
        url = random_gif("bye")
        embed.set_image(url=url)
        if channel is not None:
            async with channel.typing():
                await asyncio.sleep(0.5)
            await channel.send(text.format(member), embed=embed)

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        channel = member.guild.system_channel
        async with channel.typing():
            await asyncio.sleep(0.5)
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))

    @commands.command()
    async def profile(self, ctx, *, member=None):
        """ """
        if member:
            await ctx.send(f"https://stats.quake.com/profile/{member}")
        else:
            await ctx.send(f"nickname not set. Try: `$profile clawz`")

    @commands.command()
    async def orbb(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        channel = member.guild.system_channel
        # embed = discord.Embed()
        # url = random_gif("what?")
        # embed.set_image(url=url)

        # if channel is not None:
        #     async with channel.typing():
        #         await channel.send(embed=embed)

        await ctx.send("I'm **Orbb**. I can do:\nshow profile link `$profile somename`\nNOTHING\nmore nothing")


bot = commands.Bot(command_prefix='$')
bot.add_cog(Greetings(bot))
bot.run(config.TOKEN)

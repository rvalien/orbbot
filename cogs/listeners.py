import discord
import logging
import random

from discord.ext import commands

logger = logging.getLogger(__name__)


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        pos = "Humiliation"
        neg = "rl"
        self.yes_emoji = discord.utils.get(
            self.bot.emojis, name=pos) if discord.utils.get(self.bot.emojis, name=pos) else "✔️"
        self.no_emoji = discord.utils.get(
            self.bot.emojis, name=neg) if discord.utils.get(self.bot.emojis, name=neg) else "❌"

    @commands.Cog.listener("on_message")
    # TODO: вынести это в панель администратора которую нужно сделать
    async def word_react(self, ctx):
        trigger_words = {
            # "война": "ВОЙНЯЯЯЯЯ!!!",
            "извините": "ПИРОЖКИ!!!",
            # "сколько в": "ДА СКОЛЬКО В ТЕБЕ ЖИЗНИ?",
            "огонь": "ОЖОГ ВСЕЙ КИСЬКИ!",
            "ты меня ": "ты меня снимаешь? 🦇",
            "всем спасибо, пока": "Всем спасибо, пока.",
        }

        if not ctx.author.bot:
            word = next((value for key, value in trigger_words.items() if key in ctx.content.casefold()), None)
            if word:
                await ctx.channel.send(word)
                await self.bot.process_commands(ctx)

    @commands.Cog.listener("on_message")
    async def status_change(self, ctx):
        # TODO: вынести это в панель администратора которую нужно сделать

        trigger_words = {
            "всем пока": {
                "message": "bb, cu, <3!!!",
                "status": discord.Status.idle,
                "activity": discord.Activity(type=discord.ActivityType.listening, name="White noise"),
            },
            "рекомендую": {
                "message": "можно без рекомендаций?",
                "status": discord.Status.idle,
                "activity": discord.Activity(type=discord.ActivityType.listening, name="White noise"),
            },
            # "сейчас": {
            #     "message": "ЩЯС Я ВАС ВСЕХ БЛЯ!...",
            #     "status": discord.Status.idle,
            #     "activity": discord.Activity(type=discord.ActivityType.listening, name="White noise"),
            # },
            "всем привет": {
                "message": f"Привет, {ctx.author.name}",
                "status": discord.Status.online,
                "activity": discord.Activity(type=discord.ActivityType.watching, name="Duck Tales"),
            },
            "hi all": {
                "message": f"Hello, {ctx.author.name}",
                "status": discord.Status.online,
                "activity": discord.Streaming(name="How to insert and remove contact lenses",
                                              url="https://www.youtube.com/watch?v=zwVizcDAlX0"),
            },
            "погнали": {
                "message": "ПОГНАЛИ КОТА!",
                "status": discord.Status.do_not_disturb,
                "activity": discord.Game("QC"),
            },
        }

        if not ctx.author.bot:
            scenario = next((value for key, value in trigger_words.items() if key in ctx.content.casefold()), None)
            if scenario:
                if scenario.get("message"):
                    await ctx.channel.send(scenario["message"])
                if scenario.get("status"):
                    await self.bot.change_presence(status=scenario.get("status"), activity=scenario.get("activity"))

    @commands.Cog.listener("on_message")
    async def guild_call(self, ctx):
        react_dict = {
            f"<@&{discord.utils.get(ctx.guild.roles, name='SacTime').id}": (self.yes_emoji, self.no_emoji),
        }
        if not ctx.author.bot:
            emojis = next((value for key, value in react_dict.items() if key in ctx.content.casefold()), None)
            if emojis:
                for emoji in emojis:
                    await ctx.add_reaction(emoji)
                    await self.bot.process_commands(ctx)

    @commands.Cog.listener("on_message")
    async def add_reaction(self, ctx):
        if not ctx.author.bot:
            emojis = next(
                (random.choice(value) for key, value in self.bot.reaction.items() if key in ctx.content.casefold()),
                None)
            if emojis:
                for emoji in emojis:
                    await ctx.add_reaction(emoji)
                    await self.bot.process_commands(ctx)

    @commands.Cog.listener("on_message")
    async def goto_bed(self, ctx):
        if not ctx.author.bot:
            if ctx.content.casefold() in ("пи", "pi", "π") or ctx.content.casefold().startswith(
                    "3,14") or ctx.content.casefold().startswith("3.14"):
                link = "https://cdn.discordapp.com/attachments/381896931724492800/649586450681036813/slep.mp4"
                await ctx.reply("здуй спать!", mention_author=True)
                await ctx.reply(link)


def setup(bot):
    bot.add_cog(Listener(bot))

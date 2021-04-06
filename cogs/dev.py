import json
import requests

from discord.ext import commands


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["привет", "эй", "вопрос"])
    async def talk(self, ctx, *, question):

        url = "https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict"
        payload = {"text": question}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200 and "predictions" in response.json().keys():
            await ctx.send(f'{response.json()["predictions"][:500]}...')
        else:
            print(f"{response.text=}{response.status_code=}")
            await ctx.send("noope")

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


def setup(bot):
    bot.add_cog(DevCommands(bot))

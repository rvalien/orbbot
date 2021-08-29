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
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200 and "predictions" in response.json().keys():
            await ctx.send(f'{response.json()["predictions"][:500]}...')
        else:
            print(f"{response.text=}{response.status_code=}")
            await ctx.send("noope")

    @commands.command()
    @commands.is_owner()
    async def members(self, ctx):
        am = self.bot.get_all_members()
        for m in am:
            print(m.id, m.name)


def setup(bot):
    bot.add_cog(DevCommands(bot))

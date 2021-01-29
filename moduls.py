import json
import random
import requests
import asyncio


def random_gif(apikey, search_term, lmt=8):
    r = requests.get(f"https://api.tenor.com/v1/random?q={search_term}&key={apikey}&limit={lmt}")
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    gif_id = top_8gifs["results"][0]["id"]
    gif_url = top_8gifs["results"][0]["media"][0]["gif"]["url"]
    r = requests.get(f"https://api.tenor.com/v1/registershare?id={gif_id}&key={apikey}&q={search_term}")
    if r.status_code in (200, 202):
        return gif_url
    else:
        print(r.content)
        print(r.status_code)


def random_map():
    map_dict = {
        "🕳️": "Карта Church of Azathoth «Церковь Азатот»",
        "🟩": "Карта Tempest Shrine «Храм Бури»",
        "🔒📦": "Карта Lockbox",
        "🟥🦎": "Карта Burial Chamber «Погребальная камера»",
        "👁️": "Карта Ruins of Sartnath «Развалины Сарната»",
        "🟦": "Карта Blood Covenant «Кровавый ковенант»",
    }
    key = random.choice(list(map_dict.keys()))
    return key, map_dict[key]


def get_members_voice(context):
    if context.message.author.voice:
        voice_channel = context.message.author.voice.channel
        all_members = voice_channel.members
        if not all_members:
            return None
        else:
            no_bots = list(filter(lambda x: not x.bot, all_members))
            list_of_names = list(map(lambda x: x.name, no_bots))
            return list_of_names
    else:
        return None


# TODO не работает потому что асинхронно надо уметь
# async def get_members_react(context, time=20):
#     msg = await context.channel.send("@here Who wanna play? Add you reaction bellow ⬇️")
#     for emoji in ["✅", "❌"]:
#         await msg.add_reaction(emoji)
#     await asyncio.sleep(time)
#     msg = await context.channel.fetch_message(msg.id)
#     reactors = await msg.reactions[0].users().flatten()
#     reactors = list(filter(lambda x: not x.bot, reactors))
#     reactors = list(map(lambda x: x.name, reactors))
#
#     return reactors


def text_formatter(team: list) -> str:
    """
    transform list of lists into text
    from:
    [['player1', 'Sorlag'], ['player2', 'Nyx'], ['player3', 'Anarki'], ['player4', 'Ranger']]
    to:
    player1 - Sorlag
    player2 - Nyx
    player3 - Anarki
    player4 - Ranger

    :param team: list
    :return: str
    """
    text = ""
    for i in team:
        text += " - ".join(i)
        text += "\n"
    return text

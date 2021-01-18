import json
import random
import requests


def random_gif(apikey, search_term, lmt=8):
    r = requests.get(
        f"https://api.tenor.com/v1/random?q={search_term}&key={apikey}&limit={lmt}"
    )
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    gif_id = top_8gifs["results"][0]["id"]
    gif_url = top_8gifs["results"][0]["media"][0]["gif"]["url"]
    r = requests.get(
        f"https://api.tenor.com/v1/registershare?id={gif_id}&key={apikey}&q={search_term}"
    )
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

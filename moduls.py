import json
import logging
import random
import httpx
import numpy as np
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

HEROES = [
    {"name": "Anarki", "emoji": "Anarki", "patch": "emojis/Anarki.png"},
    {"name": "Athena", "emoji": "Athena", "patch": "emojis/Athena.png"},
    {"name": "B.J. Blazkowicz", "emoji": "BJ", "patch": "emojis/BJ.png"},
    {"name": "Clutch", "emoji": "Clutch", "patch": "emojis/Clutch.png"},
    {"name": "Death Knight", "emoji": "DeathKnight", "patch": "emojis/DeathKnight.png"},
    {"name": "Doom Slayer", "emoji": "Doom", "patch": "emojis/Doom.png"},
    {"name": "Eisen", "emoji": "Eisen", "patch": "emojis/Eisen.png"},
    {"name": "Galena", "emoji": "Galena", "patch": "emojis/Galena.png"},
    {"name": "Keel", "emoji": "Keel", "patch": "emojis/Keel.png"},
    {"name": "Nyx", "emoji": "Nyx", "patch": "emojis/Nyx.png"},
    {"name": "Ranger", "emoji": "Ranger", "patch": "emojis/Ranger.png"},
    {"name": "ScaleBearer", "emoji": "ScaleBearer", "patch": "emojis/ScaleBearer.png"},
    {"name": "Slash", "emoji": "Slash", "patch": "emojis/Slash.png"},
    {"name": "Sorlag", "emoji": "Sorlag", "patch": "emojis/Sorlag.png"},
    {"name": "Strogg", "emoji": "Strogg", "patch": "emojis/Strogg.png"},
    {"name": "Visor", "emoji": "Visor", "patch": "emojis/Visor.png"},
]


def generate_team_image(list_im: list, names: list) -> None:
    # combine images
    images = [Image.open(i) for i in list_im]
    images_comb = np.hstack(images)
    images_comb = Image.fromarray(images_comb)

    # add text
    font = ImageFont.truetype('qfont.ttf', 16)
    draw = ImageDraw.Draw(images_comb)
    margin = 0
    for text in names:
        draw.text((margin, 100), text, font=font)
        margin += 128

    images_comb.save('team.png')


def random_gif(apikey, search_term, lmt=8):
    r = httpx.get(f"https://api.tenor.com/v1/random?q={search_term}&key={apikey}&limit={lmt}")
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    gif_id = top_8gifs["results"][0]["id"]
    gif_url = top_8gifs["results"][0]["media"][0]["gif"]["url"]
    r = httpx.get(f"https://api.tenor.com/v1/registershare?id={gif_id}&key={apikey}&q={search_term}")
    if r.status_code in (200, 202):
        return gif_url
    else:
        logger.warning(r.status_code)
        logger.warning(r.content)


def random_map():
    map_dict = {
        "🕳️": "Church of Azathoth",
        "🟩": "Tempest Shrine",
        "🔒📦": "Lockbox",
        "🟥🦎": "Burial Chamber",
        "👁️": "Ruins of Sartnath",
        "🟦": "Blood Covenant",
    }
    key = random.choice(list(map_dict.keys()))
    return key, map_dict[key]


def get_members_voice(context):
    if context.message.author.voice:
        all_members = context.message.author.voice.channel.members
        if all_members:
            return [user.name for user in all_members if not user.bot]


def get_random_spectators_and_players(all_players: list, separator: int = 8) -> tuple:
    random.shuffle(all_players)
    if len(all_players) < separator:
        separator = (len(all_players[:5]) // 2) * 2
    players = all_players[:separator]
    spectators = all_players[separator:]
    return players, spectators

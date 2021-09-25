import json
import logging
import random
import requests
import numpy as np
from PIL import Image

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


def generate_team_image(list_im):
    imgs = [Image.open(i) for i in list_im]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save('team.png')


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


def get_random_spectators_and_players(all_players: list) -> tuple:
    """
    simple function, that randomize list of players
    split list into players and spectators
    players list less or equal 8 and divisible by two
    :param all_players: list
    :return: tuple with 2 list
    """

    random.shuffle(all_players)
    logger.info("input:", len(all_players))

    separator = 8
    players = all_players[:separator]
    spectators = all_players[separator:]
    return players, spectators

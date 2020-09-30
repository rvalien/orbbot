import requests
import json

from config import TENSOR_API_KEY


def random_gif(search_term, lmt=8):
    r = requests.get(f"https://api.tenor.com/v1/random?q={search_term}&key={TENSOR_API_KEY}&limit={lmt}")
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    gif_id = top_8gifs["results"][0]["id"]
    itemurl = top_8gifs["results"][0]["itemurl"]
    gif_url = top_8gifs["results"][0]["media"][0]["gif"]["url"]
    r = requests.get(f"https://api.tenor.com/v1/registershare?id={gif_id}&key={TENSOR_API_KEY}&q={search_term}")
    if r.status_code in (200, 202):
        return gif_url
        # return top_8gifs
    else:
        print(r.content)
        print(r.status_code)


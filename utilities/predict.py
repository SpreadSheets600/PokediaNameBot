import requests
from urllib.parse import urlparse, unquote


def extract_pokemon_name(url: str):
    path = urlparse(url).path
    path = unquote(path)

    if "output/" in path and path.endswith(".png"):
        name_with_extension = path.split("output/")[-1]
        name = name_with_extension.split(".png")[0]
        return name.split("-")[0]

    return None


def get_pokemon_sprite_url(url: str):
    path = urlparse(url).path
    path = unquote(path)

    if "output/" in path and path.endswith(".png"):
        name_with_extension = path.split("output/")[-1]
        sprite_link = f"https://raw.githubusercontent.com/pokedia/sprites/main/pokemon_images/{name_with_extension}"
        return sprite_link

    return None

def get_pokemon_sprite_name(name: str):
    sprite_link = f"https://raw.githubusercontent.com/pokedia/sprites/main/pokemon_images/{name}.png"

    try:
        response = requests.head(sprite_link, timeout=5)
        if response.status_code == 200:
            return sprite_link
        else:
            return None
    except requests.RequestException:
        return None

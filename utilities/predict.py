import re

from urllib.parse import urlparse, unquote


def extract_pokemon_name(url: str) -> str:
    path = urlparse(url).path
    path = unquote(path)

    if "output/" in path and path.endswith(".png"):
        name_with_extension = path.split("output/")[-1]
        name = name_with_extension.split(".png")[0]
        return name
    
    return None


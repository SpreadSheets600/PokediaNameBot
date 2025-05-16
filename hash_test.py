import io
import pickle
import aiohttp
import asyncio
import imagehash
from PIL import Image

with open("pokemon_hash_map.pkl", "rb") as f:
    HASH_MAP = pickle.load(f)


async def identify_pokemon_by_phash(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            img_hash = imagehash.average_hash(img)

            for h, name in HASH_MAP.items():
                if imagehash.hex_to_hash(h) - img_hash < 5:
                    return name

            return None


if __name__ == "__main__":
    url = "https://images-ext-1.discordapp.net/external/fN55UkBEVZYdGdRDN4ZV39jLjwuGNvYvcWmscG8pj7Y/https/raw.githubusercontent.com/pokedia/sprites/main/output/bagon.png?width=729&height=456"
    result = asyncio.run(identify_pokemon_by_phash(url))
    print(result)

import os
import pickle
import imagehash
from PIL import Image

def create_hash_map(image_dir=r"images/spawn"):
    hash_map = {}
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            try:
                name = os.path.splitext(filename)[0]
                img_path = os.path.join(image_dir, filename)
                img = Image.open(img_path)
                img_hash = imagehash.average_hash(img)
                hash_map[str(img_hash)] = name
            except Exception as e:
                print(f"Failed to hash {filename}: {e}")
    return hash_map


hash_map = create_hash_map(r"images/spawn")
with open("pokemon_hash_map.pkl", "wb") as f:
    pickle.dump(hash_map, f)

print("Hash Map Created And Saved :)")

import re
import ast

with open(f"source/names.txt", "r") as f:
    pokemon_names = ast.literal_eval(f.read())


def solve_hint(hint: str):
    regex_pattern = "^" + hint.replace(" ", "").replace("_", ".") + "$"
    matches = [
        name for name in pokemon_names if re.match(regex_pattern, name, re.IGNORECASE)
    ]
    return matches

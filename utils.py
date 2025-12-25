import requests
import urllib.parse
import random
import sys

def random_commander(
    settings: dict[str, any],
) -> dict:
    query = f'f:commander is:commander year>={settings["earliest_year"]}'

    if settings["colour_identity"] != "random":
        query += f' id={settings["colour_identity"]}'
    if not settings["game_changers"]:
        query += ' not:gamechanger'
    if not settings["universes_beyond"]:
        query += ' not:universesbeyond'
    
    card = request_random_card(query)
    
    cid = ""
    for char in "WUBRG":
        if char in card["color_identity"]:
            cid += char
    if cid == "":
        cid = "C"

    return {
        "name": card["name"], 
        "set": card["set"],
        "colour_identity": cid
    }

def random_card(
    settings: dict[str, any],
    is_nonland: bool = True,
) -> dict:
    query = f'f:commander id<={settings["colour_identity"]} -t:sticker -t:attraction year>={settings["earliest_year"]}'
    if(is_nonland):
        query += ' (-t:land or (is:dfc not:mdfc))'
    else:
        query += ' t:land -(is:dfc not:mdfc)'
        if settings["lands_produce_colours"]:
            query += f' produces<={settings["colour_identity"]}'
    
    if not settings["game_changers"]:
        query += ' not:gamechanger'
    if not settings["universes_beyond"]:
        query += ' not:universesbeyond'

    card = request_random_card(query)

    return {
        "name": card["name"], 
        "set": card["set"],
    }

def request_random_card(query: str):
    url = urllib.parse.quote_plus(f'https://api.scryfall.com/cards/random?q={query}', safe=':/?=&')

    headers = {
        'User-Agent': 'commander-randomizer/0.1',
        'Accept': "*/*"
    }

    r = requests.get(url, headers)
    if(r.status_code == 404):
        print("Could not find a card with these parameters. Halting execution.")
        sys.exit()
    return r.json()


def random_colour_identity_from_num(n: int) -> str:
    identities = {
        0: ["C"],
        1: ["W", "U", "B", "R", "G"],
        2: ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"],
        3: ["WUB", "WUR", "WUG", "WBR", "WBG", "WRG", "UBR", "UBG", "URG", "BRG"],
        4: ["WUBR", "WUBG", "WURG", "WBRG", "UBRG"],
        5: ["WUBRG"]
    }
    return random.choice(identities[n])

def write_to_file(name: str, contents: str) -> str:
    attempt = 0
    appended = ""
    while True:
        try:
            filename = f"{name}{appended}.txt"
            with open(filename, "x", encoding="utf-8") as f:
                f.write(contents)
            return f"{filename}"
        except FileExistsError:
            attempt += 1
            appended = f" ({attempt})"
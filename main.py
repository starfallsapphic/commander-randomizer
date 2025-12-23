from utils import random_card, random_commander, write_to_file
from menu_flow import menu_flow
import os
from time import sleep

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("NOTE: this program does not currently support automatically selecting partner commanders.")
    print("If you wish, you may add a partner to the deck after it is generated.\n")

    print("Please choose your desired options.\n")

    settings = menu_flow()

    random_lands_to_generate = settings["random_lands"]
    nonlands_to_generate = 99 - settings["lands"]
    deck = []

    commander = random_commander(
        settings=settings
    )
    print(f"Commander chosen: {commander["name"]}.")
    print(f"Colour identity: {commander["colour_identity"]}\n")
    deck.append(commander)

    settings["colour_identity"] = commander["colour_identity"]

    print("Generating the 99...")

    while random_lands_to_generate > 0:
        dupe = False

        card = random_card(
            settings=settings,
            is_nonland=False,
        )

        for c in deck:
            if c["name"] == card["name"]:
                dupe = True
                print(f"Skipping duplicate card: {card["name"]}")
                break
        
        if not dupe:
            print(f"Adding card #{len(deck)} (land): {card["name"]}")
            deck.append(card)
            random_lands_to_generate -= 1
        sleep(0.1) # for scryfall api - can be optimised with async


    while nonlands_to_generate > 0:
        dupe = False

        card = random_card(
            settings=settings,
            is_nonland=True,
        )

        for c in deck:
            if c["name"] == card["name"]:
                dupe = True
                print(f"Skipping duplicate card: {card["name"]}")
                break

        if not dupe:
            print(f"Adding card #{len(deck)}: {card["name"]}")
            deck.append(card)
            nonlands_to_generate -= 1
        sleep(0.1) # for scryfall api - can be optimised with async
    

    decklist = ""
    for card in deck:
        decklist += f"1x {card["name"]} ({card["set"]})\n"
    

    print(f"\nCommander: {commander["name"]}")
    print(f"{settings["colour_identity"]} deck generated with {len(deck)} cards. To be added: {100-len(deck)} lands.")
    filename = write_to_file("deck", decklist)
    print(f"Decklist written to {filename}.")

if __name__ == "__main__":
    main()
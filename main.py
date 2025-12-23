from utils import random_card, random_commander, write_to_file
from menu_flow import menu_flow
import os
from time import sleep
import threading


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("NOTE: this program does not currently support automatically selecting partner commanders.")
    print("If you wish, you may add a partner to the deck after it is generated.\n")

    print("Please choose your desired options.\n")

    settings = menu_flow()

    global random_lands_to_generate
    global nonlands_to_generate
    global deck

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

    threads_to_run = 10
    threads = []
    for n in range(threads_to_run):
        # Using `args` to pass positional arguments and `kwargs` for keyword arguments
        t = threading.Thread(
            target=add_cards, 
            kwargs={
                "settings": settings, 
                "start_delay": n*0.1, 
                "delay_between": threads_to_run*0.1
            }
        )
        threads.append(t)

    # Start each thread
    for t in threads:
        t.start()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()

    decklist = ""
    for card in deck:
        decklist += f"1x {card["name"]} ({card["set"]})\n"
    

    print(f"\nCommander: {commander["name"]}")
    print(f"{settings["colour_identity"]} deck generated with {len(deck)} cards.")
    if(len(deck) > 100):
        print(f"Add {100-len(deck)} lands to create a legal Commander deck.")

    filename = write_to_file("deck", decklist)
    print(f"Decklist written to {filename}.")


def add_cards(
    settings: dict[str, any], 
    start_delay: float, 
    delay_between: float
) -> None:

    global random_lands_to_generate
    global nonlands_to_generate
    global deck

    sleep(start_delay)

    while random_lands_to_generate > 0 or nonlands_to_generate > 0:
        is_generating_land = random_lands_to_generate > 0

        if is_generating_land:
            random_lands_to_generate -= 1
        else:
            nonlands_to_generate -= 1

        card = random_card(
            settings=settings,
            is_nonland=False if is_generating_land else True,
        )

        dupe = False
        for c in deck:
            if c["name"] == card["name"]:
                dupe = True
                break
        
        if dupe:
            print(f"Skipping duplicate card: {card["name"]}")
            if is_generating_land:
                random_lands_to_generate += 1
            else:
                nonlands_to_generate += 1
        
        if not dupe:
            print(f"[{threading.get_ident()}] Adding card #{len(deck)}{" (land)" if is_generating_land else ""}: {card["name"]}")
            deck.append(card)

        sleep(delay_between) # scryfall api requests an average maximum of 0.1s between each request
    

if __name__ == "__main__":
    main()
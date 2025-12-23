from simple_term_menu import TerminalMenu
from validators import validate_input, validate_lands, validate_random_lands, validate_colour_identity, validate_earliest_year, validate_yes_or_no
import sys

def menu_flow(
    settings: dict[str, any] = {
        "lands": 40,
        "random_lands": 0,
        "colour_identity": "random",
        "earliest_year": 1993,
        "game_changers": True,
        "universes_beyond": True,
        "randomise_set_codes": True,
    }
) -> dict[str, any]:
    while True:
        options = [
            f"# of lands                ({settings["lands"]})", 
            f"# of lands to randomise   ({settings["random_lands"]})", 
            f"colour identity           ({settings["colour_identity"]})",
            f"earliest year printed     ({settings["earliest_year"]})",
            f"toggle game changers      ({"yes" if settings["game_changers"] else "no"})",
            f"toggle universes beyond   ({"yes" if settings["universes_beyond"] else "no"})",
            f"randomise set codes       ({"yes" if settings["randomise_set_codes"] else "no"})",
            f"generate",
            f"exit"
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if(menu_entry_index == 0):
            settings["lands"] = validate_input(f"Input the number of lands to run (currently {settings["lands"]}): ", validate_lands, {"random_lands": settings["random_lands"]})
        if(menu_entry_index == 1):
            settings["random_lands"] = validate_input(f"Input the number of lands that will be randomised (currently {settings["random_lands"]}): ", validate_random_lands, {"lands": settings["lands"]})
        if(menu_entry_index == 2):
            settings["colour_identity"] = validate_input(f"Choose the colour identity of the deck OR number of colours (can be 'c' for colourless, 0-5, or 'random' ) (currently {settings["colour_identity"]}): ", validate_colour_identity)
        if(menu_entry_index == 3):
            settings["earliest_year"] = validate_input(f"Choose the earliest year to get printings from (earliest is 1993) (currently {settings["earliest_year"]}): ", validate_earliest_year)
        if(menu_entry_index == 4):
            settings["game_changers"] = validate_input(f"Choose whether game changers can be chosen (currently {"yes" if settings["game_changers"] else "no"}) (Y/n): ", validate_yes_or_no)
        if(menu_entry_index == 5):
            settings["universes_beyond"] = validate_input(f"Choose whether Universes Beyond cards can be chosen (currently {"yes" if settings["universes_beyond"] else "no"}) (Y/n): ", validate_yes_or_no)
        if(menu_entry_index == 6):
            settings["randomise_set_codes"] = validate_input(f"Choose whether or not to randomise set codes (currently {"yes" if settings["randomise_set_codes"] else "no"}) (Y/n): ", validate_yes_or_no)
        if(menu_entry_index == 7):
            print("Proceeding with given settings...\n")
            return settings
        if(menu_entry_index == 8):
            sys.exit()

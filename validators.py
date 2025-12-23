from typing import Callable

def validate_input(
    message: str, 
    validator: Callable, 
    options: dict[str, any] | None = None
) -> any:
    while True:
        user_input = input(message)

        if options is None:
            validated_input = validator(user_input)
        else:
            validated_input = validator(user_input, options)

        if type(validated_input) is dict:
            print(f'Invalid input: {validated_input["error"]}')
        else:
            return validated_input


def validate_lands(
    q: str, 
    options: dict[str, int]
) -> int | dict[str, str]:
    # accept integers only
    try:
        q = int(q)
    except ValueError:
        return {"error": "number of lands must be an integer"}
    
    # reject not between 0-99
    if q not in range(100):
        return {"error": "number of lands must be between 0 and 99"}
    
    if q < options["random_lands"]:
        return {"error": f"total number of lands cannot be less than than number of randomised lands ({options["random_lands"]})"}
    
    return q


def validate_random_lands(
    q: str, 
    options: dict[str, int]
) -> int | dict[str, str]:
    # accept integers only
    try:
        q = int(q)
    except ValueError:
        return {"error": "number of randomised lands must be an integer"}
    
    # reject not between 0-99
    if q not in range(100):
        return {"error": "number of randomised lands must be between 0 and 99"}
    
    if q > options["lands"]:
        return {"error": f"number of random lands cannot be greater than than total number of lands ({options["lands"]})"}
    
    return q


def validate_colour_identity(q: str | int):
    # random is acceptable
    if q == "random": return q

    # 1-5 is acceptable
    try:
        if(int(q)) in range(1, 6):
            return int(q)
    except ValueError:
        pass

    # C or 0 = colourless is acceptable
    if q.upper() == "C" or q == "0": return "C"
    
    # accept no other numbers
    if type(q) is not str: 
        return {"error": "number must be between 0 and 5"}
    
    # don't accept more than 5 characters
    if len(q) > 5: 
        return {"error": f"{q} is not a valid colour identity"}

    # reject characters outside of wubrg
    for char in q.upper():
        if char not in "WUBRG": 
            return {"error": f"{q} is not a valid colour identity"}

    # get colours
    colours = ""
    for char in "WUBRG":
        if q.upper().count(char) > 1:
            return {"error": f"{q} is not a valid colour identity"}
        elif q.upper().count(char) == 1:
            colours += char
    return colours


def validate_earliest_year(q: str):
    # accept integers only
    try:
        q = int(q)
    except ValueError:
        return {"error": "year must be an integer"}
    
    if(q < 1993):
        return {"error": "year cannot be earlier than 1993"}
    
    return q


def validate_yes_or_no(
    q: str, 
    options: dict[str, bool] = {"default": True}
):
    if(q.lower() == "y" or q.lower() == "yes"):
        return True
    if(q.lower() == "n" or q.lower() == "no"):
        return False
    if(q == ""):
        return options["default"]
    return {"error": f"{q} is not a valid response"}
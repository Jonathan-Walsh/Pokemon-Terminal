#!/usr/bin/env python3

"""The main module that brings everything together."""

import random
import sys
import time
import os

from pokemonterminal import scripter
from pokemonterminal.database import Database
import pokemonterminal.party as party

directory = os.path.dirname(os.path.realpath(__file__))

def print_list(list_of_items):
    """Print all the items in a list. Used for printing each Pokemon from a particular region."""
    print("\n".join(str(item) for item in list_of_items))


def print_columns(items):
    """Print a list as multiple columns instead of just one."""
    rows = []
    items_per_column = int(len(items) / 4) + 1
    for index, pokemon in enumerate(items):
        name = pokemon.get_id() + " " + pokemon.get_name().title()
        name = name.ljust(20)
        if len(rows) < items_per_column:
            rows.append(name)
        else:
            rows[index % items_per_column] += name
    print_list(rows)


def print_types(items):
    print("All existent pokemon types are:\n" + ", ".join(items))


def prefix_search(db, arg):
    """Find all Pokemon in database, db, with the prefix, arg."""
    result = db.names_with_prefix(arg)
    if len(result) == 0:
        print("No Pokemon found with prefix '" + arg + "'.")
    else:
        print_columns(result)


def print_extra(db):
    """Print all the 'Extra' Pokemon from the 'Extra' folder."""
    result = db.get_extra()
    if len(result) == 0:
        print("No Pokemon were found in Images/Extra.")
    else:
        print_columns(result)


def print_usage():
    """Print the instructions of usage."""
    print(
        '''
Usage:
    pokemon [parameter]
    ichooseyou [parameter]

Parameters:
    [name]        -   Change the terminal background to the specified Pokemon.
    [index]       -   Change the terminal background to a Pokemon by its index.
    [region]      -   List all the Pokemon of the specified region.
    [one letter]  -   List all Pokemon who's names begin with a particular letter.
    [two letters] -   List all Pokemon who's names begin with those two letters.

Other Parameters:
    all                           -   List all the Pokemon supported.
    regions                       -   List all the available regions.
    extra                         -   List all the Pokemon from the 'Extra' folder.
    random                        -   Change the terminal background to a random Pokemon.
    random-<region>               -   Change the terminal background to a random Pokemon from the specified region.
    slideshow [time]              -   Iterate through each Pokemon. Optional time (in seconds) between Pokemon.
    slideshow-<region> [time]     -   Iterate through each Pokemon in the specified region. Optional time (in seconds) between Pokemon.
    rnd-slideshow [time]          -   Iterate through each Pokemon in a random order. Optional time (in seconds) between Pokemon.
    rnd-slideshow-<region> [time] -   Iterate through each Pokemon in the specified region in a random order. Optional time (in seconds) between Pokemon.
    party			  -   List all of the pokemon in the current party
    party-[add/remove] [name]     -   Add or remove a specific Pokemon from the party
    party-show [time]             -   Iterate through each Pokemon in the party. Optional time (in seconds) betweeon Pokemon
    rnd-party-show [time]         -   Same as party-show, but in a random order
    light                         -   Change the terminal background to a random light-colored Pokemon.
    dark                          -   Change the terminal background to a random dark-colored Pokemon.
    type [type]                   -   Random pokemon of [type] omit the type for a list of types.
    clear | disable | off         -   Clear the Pokemon in the terminal.
    help                          -   Display this menu.

Wallpaper Parameters:
    pokemon _pikachu               -   Change the wallpaper to the specified Pokemon.
    pokemon _random                -   Change the wallpaper to a random Pokemon.
    pokemon _random-kanto          -   Change the wallpaper to a random Pokemon from the specified region.

Search System Information:
    Any input containing 3 or more characters triggers the internal search system. Examples:
    "pokemon pika" changes the terminal background to Pikachu.
    "pokemon dos"  changes the terminal background to Gyarados.
''')


def slideshow(db, start, end, seconds="0.25", rand=False):
    delay = 0.25
    if seconds is not None:
        delay = float(seconds)

    # Show each Pokemon, one by one.
    r = list(range(start, end))
    if rand:
        random.shuffle(r)
    try:
        for x in r:
            pokemon = db.get_pokemon(x)
            scripter.change_terminal(pokemon.get_path())
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Program was terminated.")
        sys.exit()

def update_current(pokemon):
    """Update file that stores name of current pokemon"""
    with open(directory + "/./Data/current.txt",'w') as file:
        file.write(pokemon)

def evolve(db):
    """Change background to evolution of current pokemon"""
    file =  open(directory + "/./Data/current.txt", 'r')
    lines = file.readlines()
    file.close()
    if (len(lines) == 0):
        print("No current Pokemon saved. Change background and try again")
    else:
        name = lines[0].strip()
        if name in db:
            pokemon = db.get_pokemon(name)
            evos = pokemon.get_evolutions()
            selectedEvo = random.choice(evos)
            if (selectedEvo != ""):
                change_terminal_background(db, selectedEvo)
                update_current(selectedEvo)
            else:
                print("Pokemon is already fully evolved!")
        else:
            print("Current saved Pokemon is invalid. Change background and try again")
            

def change_terminal_background(db, arg):  # arg is a pokemon_name
    """Change the terminal background to the specified Pokemon, if it exists."""
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_terminal(pokemon.get_path())
        update_current(arg)
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Pokemon was found and no suggestions are available.")
        else:
            pokemon = suggestions[0]
            scripter.change_terminal(pokemon.get_path())
            print("Did you mean {}?".format(pokemon.get_name().title()))
            if len(suggestions) > 1:
                print("Other suggestions:")
                print_columns(suggestions[1:])
            update_current(pokemon.get_name())


def change_wallpaper(db, arg):  # arg is a pokemon_name
    """Change the wallpaper to the specified Pokemon, if it exists."""
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_wallpaper(pokemon.get_path())
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Pokemon was found and no suggestions are available.")
        else:
            pokemon = suggestions[0]
            scripter.change_wallpaper(pokemon.get_path())
            print("Did you mean {}?".format(pokemon.get_name().title()))
            if len(suggestions) > 1:  # if there are other suggestions
                print("Other suggestions:")
                print_columns(suggestions[1:])


def multiple_argument_handler(arg, arg2, escape_code):
    db = Database()
    rand = arg.startswith("rnd")
    if "slideshow" in arg:
        try:
            if arg.endswith("slideshow"):
                slideshow(db, 1, 494, arg2, rand)
            elif arg.endswith("slideshow-kanto"):
                slideshow(db, 1, 152, arg2, rand)
            elif arg.endswith("slideshow-johto"):
                slideshow(db, 152, 252, arg2, rand)
            elif arg.endswith("slideshow-hoenn"):
                slideshow(db, 252, 387, arg2, rand)
            elif arg.endswith("slideshow-sinnoh"):
                slideshow(db, 387, 494, arg2, rand)
            elif arg.endswith("slideshow-unova"):
                slideshow(db, 494, 650, arg2, rand)
            elif arg.endswith("slideshow-kalos"):
                slideshow(db, 650, 720, arg2, rand)
            else:
                print('Invalid slideshow command specified.'
                      '\nType "help" to see all the commands.')
        except ValueError:
            print('The slideshow time needs to be a positive number'
                  '\nType "help" to see all the commands.')
    elif arg.lower() == 'type':
        arg2 = arg2.lower()
        if arg2 not in db.get_pokemon_types():
            print("Invalid type specified")
        else:
            target = db.get_pokemon_of_type(arg2).get_name()
            if escape_code:
                change_wallpaper(db, target)
            else:
                change_terminal_background(db, target)
    elif "party-show" in arg:
        try:
            party.party_show(db, arg2, rand)
        except ValueError:
            print('The slideshow time needs to be a positive number'
                  '\nType "help" to see all the commands.')
    elif arg.lower() == 'party-add':
        arg2 = arg2.lower()
        party.party_add(arg2)
    elif arg.lower() == 'party-remove':
        arg2 = arg2.lower()
        party.party_remove(arg2) 
    else:
        print('Invalid command specified.'
              '\nType "help" to see all the commands.')


def single_argument_handler(arg, escape_code):
    """Handle the logic for when there is only one command line parameter inputted."""
    db = Database()

    if len(arg) < 3 and arg.isalpha():
        prefix_search(db, arg)
    elif arg == "extra":
        print_extra(db)
    elif arg == "regions":
        print_list(db.get_regions())
    elif arg == "help" or arg.startswith("-h"):
        print_usage()
    elif arg == "kanto":
        print_columns(db.get_kanto())
    elif arg == "johto":
        print_columns(db.get_johto())
    elif arg == "hoenn":
        print_columns(db.get_hoenn())
    elif arg == "sinnoh":
        print_columns(db.get_sinnoh())
    elif arg == "unova":
        print_columns(db.get_unova())
    elif arg == "kalos":
        print_columns(db.get_kalos())
    elif arg == "all":
        print_columns(db.get_all())
    elif arg in ("clear", "disable", "off"):
        scripter.clear_terminal()
    elif arg == "random" and escape_code:
        change_wallpaper(db, db.get_random())
    elif arg == "random-kanto" and escape_code:
        change_wallpaper(db, db.get_random_from_region("kanto"))
    elif arg == "random-johto" and escape_code:
        change_wallpaper(db, db.get_random_from_region("johto"))
    elif arg == "random-hoenn" and escape_code:
        change_wallpaper(db, db.get_random_from_region("hoenn"))
    elif arg == "random-sinnoh" and escape_code:
        change_wallpaper(db, db.get_random_from_region("sinnoh"))
    elif arg == "random-unova" and escape_code:
        change_wallpaper(db, db.get_random_from_region("unova"))
    elif arg == "random-kalos" and escape_code:
        change_wallpaper(db, db.get_random_from_region("kalos"))
    elif arg == "random":
        change_terminal_background(db, db.get_random())
    elif arg == "random-kanto":
        change_terminal_background(db, db.get_random_from_region("kanto"))
    elif arg == "random-johto":
        change_terminal_background(db, db.get_random_from_region("johto"))
    elif arg == "random-hoenn":
        change_terminal_background(db, db.get_random_from_region("hoenn"))
    elif arg == "random-sinnoh":
        change_terminal_background(db, db.get_random_from_region("sinnoh"))
    elif arg == "random-unova":
        change_terminal_background(db, db.get_random_from_region("unova"))
    elif arg == "random-kalos":
        change_terminal_background(db, db.get_random_from_region("kalos"))
    elif arg == "light" and escape_code:
        change_wallpaper(db, db.get_light())
    elif arg == "dark" and escape_code:
        change_wallpaper(db, db.get_dark())
    elif arg == "light":
        change_terminal_background(db, db.get_light())
    elif arg == "dark":
        change_terminal_background(db, db.get_dark())
    elif arg in ("type", "types"):
        print_types(db.get_pokemon_types())
    elif arg == "slideshow":
        slideshow(db, 1, 494)
    elif arg == "slideshow-kanto":
        slideshow(db, 1, 152)
    elif arg == "slideshow-johto":
        slideshow(db, 152, 252)
    elif arg == "slideshow-hoenn":
        slideshow(db, 252, 387)
    elif arg == "slideshow-sinnoh":
        slideshow(db, 387, 494)
    elif arg == "slideshow-unova":
        slideshow(db, 494, 650)
    elif arg == "slideshow-kalos":
        slideshow(db, 650, 720)
    elif arg.endswith("slideshow"):
        slideshow(db, 1, 494, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-kanto"):
        slideshow(db, 1, 152, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-johto"):
        slideshow(db, 152, 252, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-hoenn"):
        slideshow(db, 252, 387, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-sinnoh"):
        slideshow(db, 387, 494, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-unova"):
        slideshow(db, 494, 650, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-kalos"):
        slideshow(db, 650, 720, rand=arg.startswith("rnd"))
    elif arg == "?":
        print("This function is deprecated.")
    elif arg == "evolve":
        evolve(db)
    elif arg == "party":
        party.party_print()
    elif arg == "party-show":
        party.party_show(db)
    elif arg.endswith("party-show"):
        party.party_show(db, rand=arg.startswith("rnd"))
    elif escape_code:
        change_wallpaper(db, arg)
    else:
        change_terminal_background(db, arg)


def main(argv=sys.argv):
    """Entrance to the program."""
    if len(argv) == 1:
        print('No command line arguments specified.'
              '\nTry typing in a Pokemon name or number.'
              '\nOr type "help" to see all the commands.')
        return
    # If there is an escape code, then change the wallpaper, not the terminal.
    if str(argv[1]).startswith("_"):
        ESCAPE_CODE = True
        argv[1] = argv[1][1:]
    else:
        ESCAPE_CODE = False

    if len(argv) == 2:
        single_argument_handler(argv[1].lower(), ESCAPE_CODE)
    elif len(argv) == 3:
        multiple_argument_handler(argv[1].lower(), argv[2], ESCAPE_CODE)
    else:
        print('Invalid number of arguments.'
              '\nType "help" to see all the commands.')


if __name__ == "__main__":
    # Entrance to the program.
    main(sys.argv)

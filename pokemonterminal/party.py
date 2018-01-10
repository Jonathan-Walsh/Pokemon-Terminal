'''This file contains all the functions necessary for the "party" commands'''

import os
import time
import random
from pokemonterminal.database import Database
from pokemonterminal import scripter

directory = os.path.dirname(os.path.realpath(__file__))
party_file = directory + "/./Data/party.txt"

def party_add(name):
    file = open(party_file, 'r')
    lines = file.readlines()
    file.close()
    inParty = False
    for l in lines:
        if (name == l):
            inParty = True 
    if inParty:
        print("Pokemon already in the party!")
    else:
        file = open(party_file, 'a')
        file.write(name + '\n')
        file.close()

def party_remove(name):
    file = open(party_file, 'r')
    lines = file.readlines()
    file.close()
    updatedLines = []
    lineToRemove = name + '\n'
    for l in lines:
        if (l != lineToRemove):
            updatedLines.append(l)
    file = open(party_file, 'w')
    for l in updatedLines:
        file.write(l)
    file.close()

def party_get_pokemon():
    file = open(party_file, 'r')
    lines = file.read().splitlines()
    db = Database()
    pokemon = []
    for line in lines:
        if db.pokemon_name_exists(line):
            pokemon.append(line)
    file.close()
    return pokemon

def party_show(db, seconds="0.25", rand=False):
    delay = 0.25
    if seconds is not None:
        delay = float(seconds)

    party = party_get_pokemon()

    # Show each Pokemon, one by one.
    if rand:
        random.shuffle(party)
    try:
        for x in party:
            pokemon = db.get_pokemon(x)
            scripter.change_terminal(pokemon.get_path())
            with open(directory + "/./Data/current.txt",'w') as file:
                file.write(x)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Program was terminated.")
        sys.exit()


def party_print():
    print("Pokemon in party:")
    party = party_get_pokemon()
    for pkmn in party:
        print(pkmn)


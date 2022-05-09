import os
import sys
import shutil
import logging
import CODE.world_creator.mappings as wc
from CODE.inventory import Item
from pathlib import Path
from ast import literal_eval
import json

RESOURCES = Path(__file__).parent / "../_RESOURCES/"

COLUMNS, LINES = shutil.get_terminal_size()

def set_console():
    cmd = 'mode 100,50'
    os.system(cmd)


def fancy():
    """"Planned to be used to make the screen look fancy, is open for change"""

    sys.stdout.write("{0:*^{1}}\n".format("", 100))


def clear_console():
    """ Clear the console. POSIX refers to OSX/Linux. """

    os.system('clear' if os.name == 'posix' else 'cls')


def print_to_screen(this_output=str(), _map=str()):
    """Prints to console in given format"""

    clear_console()
    print("{}\n".format(_map))

    print("\033[0m{}\n".format(this_output))


def get_print_value(_val: str) -> str:
    """ Format output value for printing. """

    def get_state_color(state):
        """ Used to color console output. """

        switcher = {
            wc.RIM: '\033[100;100m ',          # Grey background color
            wc.GROUND: '\033[;42m ',         # Green background color
            wc.PLAYER: '\033[46;46m ',        # Green background, Cyan foreground color
            wc.ROAD: '\033[;43m ',
            wc.BUILDING: '\033[;47m ',
            wc.DOORS: '\033[;41m ',
            wc.TUNNEL: '\033[;40m ',
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))


def get_file(file_name: str):

    def evaluator(incoming):
        incoming_world = {}
        for key, value in incoming.items():
            incoming_world[literal_eval(key)] = incoming[key]
        return incoming_world


    with open(RESOURCES / file_name) as file:
        data = json.load(file)
        world_data = data["world"]
        data["world"] = evaluator(world_data)
        return data

def open_file():
    """Reads the needed files into memory"""

    file = []
    worlds = wc.WORLD_NAMES
    world_size = []
    worlds_outgoing = dict()

    def evaluator(incoming, incoming_worlds):
        for key, value in incoming.items():
            incoming_worlds[literal_eval(key)] = incoming[key]
        return incoming_worlds

    for names in worlds:
        worlds_outgoing[names] = dict()
        input_file = names + ".json"
        with open(RESOURCES / input_file) as infile:
            middle_man = [x for x in [{x: y} for x, y in json.load(infile).items()]]
            world_size_init = middle_man[0]
            data = middle_man[1]["world"]

        world_size.append(world_size_init["world_size"]["size"])

        file.append(evaluator(data, worlds_outgoing[names]))

    return file, world_size


def load_save(incoming_inventory):
    """"Loads any available save-file"""

    with open(RESOURCES / "save.log", "r") as savefile:
        save_file_input = savefile.read()

    incoming = (save_file_input.split("\n"))
    posit, world_int_output, inventory_desc, inventory_outgoing = incoming[0], incoming[1], incoming[2], incoming[3:]
    try:
        for each in inventory_outgoing:
            each_key, each_value, each_hidden = each.split("\t")
            incoming_inventory.add_item(Item(each_key, each_value, each_hidden))
    except ValueError:
        pass
    return posit, world_int_output, incoming_inventory

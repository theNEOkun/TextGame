import json
import sys
import Base as b
from ast import literal_eval
import world_creator as wc

INVENTORY = dict()

RIM, GROUND, PLAYER = '#', '-', 'X'  # base cell states
STATE_ELDER, STATE_PRIME_ELDER = 'E', 'P'           # cell states used for higher grade


def print_to_screen(_status, world, posit):
    b.clear_console()
    mapper(world, posit)
    sys.stdout.write("\n\n")
    sys.stdout.write("{}".format(_status))
    sys.stdout.write("\nWhat do you want to do?\n")


def get_print_value(_val: str) -> str:
    """ Format output value for printing. """
    def get_state_color(state):
        """ Used to color console output. """
        switcher = {
            RIM: '\033[45m',          # Magenta background color
            GROUND: '\033[31m',         # Red foreground color
            PLAYER: '\033[36m',        # Cyan foreground color
            STATE_ELDER: '\033[32m',        # Green foreground color
            STATE_PRIME_ELDER: '\033[34m',  # Blue foreground color
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))


def mapper(world, posit):
    _printer = []
    _i = 9
    for _cell in world:
        if world[_cell]["mapping"] != "#":
            if world[_cell] == posit:
                _printer.append(get_print_value(PLAYER) + " ")
            else:
                _printer.append(get_print_value(world[_cell]["mapping"]) + " ")
        else:
            _printer.append(get_print_value(RIM) + " ")

    while _i < len(_printer):
        _printer.insert(_i, "\n")  # Adds linebreaks where needed.
        _i += 9 + 1

    sys.stdout.write(''.join(_printer))  # Prints it out


def open_file():

    the_world = dict()

    with open("_RESOURCES/world.json", "r") as infile:
        data = json.load(infile)

    for key, value in data.items():
        the_world[literal_eval(key)] = data[key]

    return the_world


def place_description(world, posit):
    return world[posit]["description"]["place"] + "\n"


def look(square, in_put):
    if square["interactions"]:
        possible_interactions = square["interactions"]
        inputs = in_put.split(" ")
        cardinals = ("north", "south", "east", "west")

        if "at" in in_put:
            try:
                return possible_interactions[inputs[2]] + "\n"
            except KeyError:
                return "You can't do that\n"
        if "around" in in_put:
            output = str()
            output += square["description"]["place"] + "\n"
            output += "You see:\n"
            for keys, values in square["items"].items():
                output += "{}\n".format(values["desc"])
            return "{:^}\n".format(output)
        if inputs[1] in cardinals:
            try:
                return square["directions"][inputs[1]] + "\n"
            except KeyError:
                return "Where did you want to look?\n"


def walker(world, posit, in_put):
    inputs = in_put.split(" ")
    direction = tuple(world[posit]["neighbours"][inputs[1]]["coord"])
    if world[direction]:
        if world[posit]["neighbours"][inputs[1]]["walk"] == "yes":
            return direction, place_description(world, direction)
        else:
            return posit, ("Can't walk there because {}\n"
                           .format(world[posit]["neighbours"][inputs[1]]["why"]))
    else:
        return posit, "There's no reason to go there\n"


def pickup(square, in_put):
    items = square["items"]
    inputs = in_put.split(" ")
    try:
        print(items[inputs[1]]["description"])
        if square["items"][inputs[1]]["pickup"] == "yes":
            INVENTORY.update({inputs[1]: items[inputs[1]]["description"]})
    except KeyError:
        b.progress("What did you want to pickup?\n")


def inputter(world, posit):
    in_put = str()
    _status = str()
    while in_put != "exit":
        square = world[posit]
        in_put = input()
        if "look" in in_put:
            _status = look(square, in_put)
        if "walk" in in_put or "go" in in_put:
            posit, _status = walker(world, posit, in_put)
        if "pickup" in in_put:
            pickup(square, in_put)
        if "open" in in_put:
            _status = INVENTORY
        print_to_screen(_status, world, posit)
    else:
        b.clear_console()
        sys.stdout.write("Goodbye")


def main_part():
    world = open_file()
    b.set_console()
    posit = (0, 4)
    print_to_screen(place_description(world, posit), world, posit)
    inputter(world, posit)


if __name__ == '__main__':
    sys.stdout.write("Start, or reload world")
    interput = input("What do you want to do?")
    if interput == "start":
        main_part()
    if interput == "reload world":
        wc.creator()
    # wc.mapping()

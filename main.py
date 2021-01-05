import json
import sys
from asciimatics.screen import ManagedScreen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
import Base as b
from ast import literal_eval
import world_creator as wc

INVENTORY = dict()


@ManagedScreen
def screener(_status, world, posit, screen = None):
    map_output = mapper(world, posit)
    screen.print_at(map_output, 0, 0)
    screen.print_at("\n\n{:^}\nWhat do you want to do?\n".format(_status, 50), 10, 0)
    screen.refresh()


def print_to_screen(_status, world, posit):
    b.clear_console()
    map_output = mapper(world, posit)
    sys.stdout.write(map_output)
    sys.stdout.write("\n\n{:^}\nWhat do you want to do?\n".format(_status, 50))


def get_print_value(_val: str) -> str:
    """ Format output value for printing. """
    def get_state_color(state):
        """ Used to color console output. """
        switcher = {
            wc.RIM: '\033[100;100m ',          # Grey background color
            wc.GROUND: '\033[;42m ',         # Green background color
            wc.PLAYER: '\033[46;42m ',        # Green background, Cyan foreground color
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))


def mapper(world, posit):
    _printer = []
    _i = 9
    for _cell in world:
        if world[_cell]["mapping"] != wc.RIM:
            if world[_cell] != world[posit]:
                _printer.append(get_print_value(world[_cell]["mapping"]))
            else:
                _printer.append(get_print_value(wc.PLAYER))
        else:
            _printer.append(get_print_value(wc.RIM))

    while _i < len(_printer):
        _printer.insert(_i, "\n")  # Adds linebreaks where needed.
        _i += 9 + 1

    return "{:^}".format(''.join(_printer), 50)  # Prints the map out


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
    try:
        direction = tuple(world[posit]["neighbours"][inputs[1]]["coord"])
        if world[posit]["neighbours"][inputs[1]]["walk"] == "yes":
            return direction, place_description(world, direction)
        else:
            return posit, ("Can't walk there because {}\n"
                           .format(world[posit]["neighbours"][inputs[1]]["why"]))
    except KeyError:
        return posit, "Where did you want to walk?"


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
        # in_put = input()
        if "look" in in_put:
            _status = look(square, in_put)
        if "walk" in in_put or "go" in in_put:
            posit, _status = walker(world, posit, in_put)
        if "pickup" in in_put:
            pickup(square, in_put)
        if "open" in in_put:
            _status = INVENTORY
        # print_to_screen(_status, world, posit)
        screener(_status, world, posit)
    else:
        b.clear_console()
        sys.stdout.write("Goodbye")


def main_part():
    world = open_file()
    # b.set_console()
    spawn = (0, 4)
    # print_to_screen(place_description(world, spawn), world, spawn)
    screener(place_description(world, spawn), world, spawn)
    inputter(world, spawn)


if __name__ == '__main__':
    sys.stdout.write("Start, or reload world\n")
    interput = input("What do you want to do?")
    if interput == "start":
        main_part()
    if interput == "reload world":
        interput = input("Are you really sure?")
        if interput == "yes":
            wc.creator()
        else:
            pass
    # wc.mapping()

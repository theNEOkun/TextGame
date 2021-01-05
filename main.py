import json
import Base as b
from ast import literal_eval
import world_creator as wc

INVENTORY = dict()


RIM, GROUND, PLAYER = '#', '-', 'X'  # base cell states
STATE_ELDER, STATE_PRIME_ELDER = 'E', 'P'           # cell states used for higher grade


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


def mapper(mapp, posit):
    _printer = []
    _i = 9
    for _cell in mapp:  # This only takes care of adding to the list to be printed out
        if mapp[_cell]:
            if mapp[_cell] == posit:
                _printer.append(get_print_value(PLAYER))
            else:
                _printer.append(get_print_value(mapp[_cell]["part"]))
        else:  # This puts everything into the list
            _printer.append(get_print_value(RIM))

    while _i < len(_printer):
        _printer.insert(_i, "\n")  # Adds linebreaks where needed.
        _i += 9 + 1

    b.progress(''.join(_printer))  # Prints it out


def open_file():
    the_world = dict()

    with open("_RESOURCES/world.json", "r") as infile:
        data = json.load(infile)

    for key, value in data.items():
        the_world[literal_eval(key)] = data[key]

    the_map = dict()

    with open("_RESOURCES/mapp.json", "r") as infile:
        data = json.load(infile)

    for key, value in data.items():
        the_map[literal_eval(key)] = data[key]

    return the_world, the_map


def place_description(world, mapp, posit):
    b.clear_console()
    mapper(mapp, posit)
    b.progress(world[posit]["description"]["place"] + "\n")


def look(square, in_put):
    if square["interactions"]:
        possible_interactions = square["interactions"]
        inputs = in_put.split(" ")
        cardinals = ("north", "south", "east", "west")

        if "at" in in_put:
            try:
                b.progress(possible_interactions[inputs[2]] + "\n")
            except KeyError:
                b.progress("You can't do that\n")
        if "around" in in_put:
            b.clear_console()
            b.fancy()
            output = str()
            output += square["description"]["place"] + "\n"
            output += "You see:\n"
            for keys, values in square["items"].items():
                output += "{}\n".format(values["desc"])
            b.progress("{:^}\n".format(output))
        if inputs[1] in cardinals:
            try:
                b.progress(square["directions"][inputs[1]] + "\n")
            except KeyError:
                b.progress("Where did you want to look?\n")


def walker(world, mapp, posit, in_put):
    inputs = in_put.split(" ")
    try:
        direction = tuple(world[posit]["neighbours"][inputs[1]]["coord"])
        if world[direction]:
            if world[posit]["neighbours"][inputs[1]]["walk"] == "yes":
                place_description(world, mapp, direction)
                return direction
            else:
                b.progress("Can't walk there because it's a {}\n".format(world[posit]["neighbours"][inputs[1]]["why"]))
                return posit
        else:
            b.progress("There's no reason to go there\n")
            return posit
    except KeyError:
        b.progress("Where did you want to go?\n")
        return posit


def pickup(square, in_put):
    items = square["items"]
    inputs = in_put.split(" ")
    try:
        print(items[inputs[1]]["description"])
        if square["items"][inputs[1]]["pickup"] == "yes":
            INVENTORY.update({inputs[1]: items[inputs[1]]["description"]})
    except KeyError:
        b.progress("What did you want to pickup?\n")


def inputter(world, mapp, posit):
    in_put = str()
    while in_put != "exit":
        square = world[posit]
        b.progress(str(posit) + "\n")
        b.progress("What do you want to do?\n")
        in_put = input()
        if "look" in in_put:
            look(square, in_put)
        if "walk" in in_put or "go" in in_put:
            posit = walker(world, mapp, posit, in_put)
        if "pickup" in in_put:
            pickup(square, in_put)
        if "open" in in_put:
            print(INVENTORY)
    else:
        b.clear_console()
        b.progress("Goodbye")


def main_part():
    world, mapp = open_file()
    posit = (4, 0)
    b.set_console()
    place_description(world, mapp, posit)
    inputter(world, mapp, posit)


if __name__ == '__main__':
    main_part()
    # wc.creator()
    # wc.mapping()

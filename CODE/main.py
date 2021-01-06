import json
import sys
import CODE.Base as b
import CODE.items as items
from ast import literal_eval
import CODE.world_creator as wc


def print_to_screen(_status):
    sys.stdout.write("\n{}\n".format(_status))


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


def mapper(world, posit, inventory):
    _printer = []
    _i = 9
    if inventory.is_in_inventory("map"):
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

        return sys.stdout.write("{}".format(''.join(_printer)))  # Prints the map out
    else:
        return ""


def open_file():
    file = []

    worlds = wc.WORLDS
    for key1, value1 in worlds.items():
        worlds[key1] = dict()
        input_file = key1 + ".json"
        with open(b.RESOURCES / input_file) as infile:
            data = json.load(infile)

        for key, value in data.items():
            worlds[key1][literal_eval(key)] = data[key]
        file.append(worlds[key1])

    return file


def place_description(world, posit):
    return world[posit]["description"]["place"] + "\n"


def look(square, in_put, inventory):
    possible_interactions = square["interactions"]
    cardinals = ("north", "south", "east", "west")

    if "at" == in_put[1]:
        try:
            if inventory.is_in_inventory(in_put[1]):
                return "What do you mean?\n"
            else:
                return possible_interactions[in_put[1]]["desc"] + "\n"
        except KeyError:
            return "You can't do that\n"
    if "around" == in_put[1]:
        output = str()
        output += square["description"]["place"] + "\n"
        output += "You see:\n"
        for keys, values in square["items"].items():
            if inventory.is_in_inventory(keys):
                pass
            else:
                output += "{}\n".format(values["desc"])
        return "{:^}\n".format(output)
    if in_put[1] in cardinals:
        try:
            return square["directions"][in_put[1]] + "\n"
        except KeyError:
            return "Where did you want to look?\n"


def walker(square, in_put, world_int, posit):
    _status = ""
    try:
        direction = tuple(square[in_put]["coord"])
        if square[in_put]["walk"] == "yes":
            if square[in_put]["door"] == "yes":
                direction = (square[in_put]["placement"][0],
                             square[in_put]["placement"][1])
                world_int = square[in_put]["world"]
                return direction, _status, world_int
            else:
                return direction, _status, world_int
        else:
            _status = ("Can't walk there because {}\n"
                       .format(square[in_put]["why"]))
            return posit, _status, world_int
    except KeyError:
        _status = "Where did you want to walk?"
        return posit, _status, world_int


def pickup(item_pool, in_put, inventory):
    try:
        if item_pool[in_put]["pickup"] == "yes":
            inventory.add_item(items.Item(in_put, item_pool[in_put]["desc"]))
            return "Picked {} up".format(in_put)
        else:
            return "Can't pick {} up".format(in_put)
    except KeyError or IndexError:
        return "What did you want to pickup?\n"


def inputter(in_put, posit, square, inventory, world_int):
    """Inputter here is what takes commands, and sends them further along on its journey."""
    item_pool = square["items"]
    walking = square["neighbours"]
    inputs = in_put.split(" ")
    _status = str()
    looper = True
    if "look" == inputs[0]:
        _status = look(square, inputs, inventory)
    if inputs[0] in ["go", "walk"]:
        posit, _status, world_int = walker(walking, inputs[1], world_int, posit)
    if "pickup" == inputs[0]:
        _status = pickup(item_pool, inputs[1], inventory)
    if "open" == inputs[0]:
        _status = inventory
    if "where am I" in in_put:
        _status = str(posit) + "\n" + str(world_int)
    # if "save" in in_put:
        # save.debug("Posit: {}\nWorld: {}\nInventory: {}".format(posit, world_int, inventory))
    if "exit" in in_put:
        looper = False
    b.clear_console()
    return _status, posit, world_int, looper


def main_part():
    """This initialises the whole thing, and is mostly used as a starting-point"""
    world_int = 0
    _status = str()
    looper = True
    posit = wc.SPAWN

    logger, save = b.create_logger()
    inventory = items.Inventory()
    worlds = open_file()

    sys.stdout.write("Enter description text here\n")
    while looper:
        world = worlds[world_int]
        square = world[posit]
        mapper(world, posit, inventory)

        print_to_screen(place_description(world, posit))

        in_put = input("What do you want to do?\n")
        _status, posit, world_int, looper = inputter(in_put, posit, square, inventory, world_int)
        logger.info("Posit: {}\nWorld: {}\nInv: {}"
                    .format(posit, world_int, inventory))
        print_to_screen(_status)
    else:
        b.clear_console()
        print_to_screen("Do you want to save?\n")
        in_put = input("yes/no: ")
        if in_put == "yes":
            save.debug("Posit: {}\nWorld: {}\nInventory: {}"
                       .format(posit, world_int, inventory))
            sys.stdout.write("Goodbye\n")
        elif in_put == "no":
            sys.stdout.write("Goodbye\n")
        else:
            b.clear_console()
            main_part()


if __name__ == '__main__':
    """This is the stuff that is first printed out"""
    b.set_console()
    sys.stdout.write("Start, or reload world\n")
    interput = input("What do you want to do? ")
    if interput == "start":
        b.clear_console()
        main_part()
    if interput == "reload world":
        b.clear_console()
        ausput = input("Are you really sure? ")
        if ausput == "yes":
            wc.runner()
        elif ausput == "no":
            main_part()
    # wc.mapping()

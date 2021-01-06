import json
import sys
import CODE.Base as b
import CODE.items as items
from ast import literal_eval
import CODE.world_creator as wc


def print_to_screen(_status, inventory, world=None, posit=None):
    b.clear_console()
    map_output = mapper(world, posit, inventory)
    sys.stdout.write(map_output)
    sys.stdout.write("\n\n{}\n\nWhat do you want to do?\n".format(_status))


def get_print_value(_val: str) -> str:
    """ Format output value for printing. """
    def get_state_color(state):
        """ Used to color console output. """
        switcher = {
            wc.RIM: ' \033[100;100m ',          # Grey background color
            wc.GROUND: ' \033[;42m ',         # Green background color
            wc.PLAYER: ' \033[46;42m ',        # Green background, Cyan foreground color
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))


def mapper(world, posit, inventory):
    def update_world():

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

        return "{}".format(''.join(_printer))  # Prints the map out
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
    if square["interactions"]:
        possible_interactions = square["interactions"]
        inputs = in_put.split(" ")
        cardinals = ("north", "south", "east", "west")

        if "at" in in_put:
            try:
                if inventory.is_in_inventory(inputs[2]):
                    return "What do you mean?\n"
                else:
                    return possible_interactions[inputs[2]]["desc"] + "\n"
            except KeyError:
                return "You can't do that\n"
        if "around" in in_put:
            output = str()
            output += square["description"]["place"] + "\n"
            output += "You see:\n"
            for keys, values in square["items"].items():
                if inventory.is_in_inventory(keys):
                    pass
                else:
                    output += "{}\n".format(values["desc"])
            return "{:^}\n".format(output)
        if inputs[1] in cardinals:
            try:
                return square["directions"][inputs[1]] + "\n"
            except KeyError:
                return "Where did you want to look?\n"


def walker(world, posit, in_put):
    inputs = in_put.split(" ")
    world_int = 0
    try:
        direction = tuple(world[posit]["neighbours"][inputs[1]]["coord"])
        if world[posit]["neighbours"][inputs[1]]["walk"] == "yes":
            if world[posit]["neighbours"][inputs[1]]["door"] == "yes":
                direction = (world[posit]["neighbours"][inputs[1]]["placement"][0],
                             world[posit]["neighbours"][inputs[1]]["placement"][1])
                world_int = world[posit]["neighbours"][inputs[1]]["world"]
                return direction, place_description(world, direction), world_int
            else:
                return direction, place_description(world, direction), world_int
        else:
            return posit, ("Can't walk there because {}\n"
                           .format(world[posit]["neighbours"][inputs[1]]["why"])), world_int
    except KeyError or IndexError:
        return posit, "Where did you want to walk?"


def pickup(square, in_put, inventory):
    item_pool = square["items"]
    inputs = in_put.split(" ")
    try:
        if square["items"][inputs[1]]["pickup"] == "yes":
            inventory.add_item(items.Item(inputs[1], item_pool[inputs[1]]["desc"]))
    except KeyError:
        b.progress("What did you want to pickup?\n")


def inputter(worlds, posit):
    logger, save = b.create_logger()
    world_int = 0
    world = worlds[world_int]
    inventory = items.Inventory()
    in_put = str()
    _status = str()
    while in_put != "exit":
        square = world[posit]
        in_put = input()
        if "look" in in_put:
            _status = look(square, in_put, inventory)
        if "walk" in in_put or "go" in in_put:
            posit, _status, world_int = walker(world, posit, in_put)
        if "pickup" in in_put:
            pickup(square, in_put, inventory)
        if "open" in in_put:
            _status = inventory
        if "where am I" in in_put:
            _status = str(posit) + "\n" + str(world_int)
        if "save" in in_put:
            save.debug("Posit: {}\nWorld: {}\nInventory: {}".format(posit, world_int, inventory))
        logger.info("Posit: {}\nWorld: {}\nWorld_map: {}".format(posit, world_int, mapper(world, posit, inventory)))
        print_to_screen(_status, inventory, world, posit)
    else:
        b.clear_console()
        print_to_screen("Do you want to save?", inventory, world, posit)
        in_put = input()
        if in_put == "yes":
            save.debug("Posit: {}\nWorld: {}\nInventory: {}".format(posit, world_int, inventory))
            sys.stdout.write("Goodbye")
        else:
            sys.stdout.write("Goodbye")


def main_part():
    b.clear_console()
    worlds = open_file()
    b.set_console()
    spawn = wc.SPAWN
    sys.stdout.write("Enter description text here")
    inputter(worlds, spawn)


if __name__ == '__main__':
    sys.stdout.write("Start, or reload world\n")
    interput = input("What do you want to do?")
    if interput == "start":
        main_part()
    if interput == "reload world":
        interput = input("Are you really sure?")
        if interput == "yes":
            wc.runner()
        else:
            pass
    # wc.mapping()

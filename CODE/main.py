import json
import sys
import CODE.Base as b
import CODE.items as items
from time import sleep
from ast import literal_eval
import CODE.world_creator as wc


def print_to_screen(this_output=str(), _map=str()):
    """Prints to console in given format"""
    b.clear_console()
    sys.stdout.write("{}\n".format(_map))

    sys.stdout.write("{}\n".format(this_output))


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


def mapper(world, posit, inventory):
    """Handles the map, and its format"""
    _printer = []
    _i = wc.x_axis
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
            _i += wc.x_axis + 1

        return "{}".format(''.join(_printer))  # Prints the map out
    else:
        return " "


def open_file():
    """Reads the needed files into memory"""
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


def load_save(incoming_inventory):
    with open(b.RESOURCES / "save.log", "r") as savefile:
        save_file_input = savefile.read()

    incoming = (save_file_input.split("\n"))
    posit, world_int_output, inventory_desc, inventory_outgoing = incoming[0], incoming[1], incoming[2], incoming[3:]
    try:
        for each in inventory_outgoing:
            each_key, each_value, each_hidden = each.split("\t")
            print(each_key, each_value)
            incoming_inventory.add_item(items.Item(each_key, each_value, each_hidden))
    except ValueError:
        pass
    return posit, world_int_output, incoming_inventory


def place_description_global(world, posit):
    """Just takes the description of the place the player currently is in"""
    return world[posit]["description"]["place"] + "\n"


def interacter(square, posit, inventory, action, interactive_item, world):
    if action == "open":
        if interactive_item == "door":
            if action in square["interactions"][interactive_item]["action"]:
                if inventory.hidden_info(square["interactions"]["door"]["key"]):
                    coord, coord_ins, walkable, walkable_ins = square["interactions"][interactive_item]["happening"]
                    world[literal_eval(coord)]["neighbours"][walkable]["walk"] = "yes"
                    world[literal_eval(coord_ins)]["neighbours"][walkable_ins]["walk"] = "yes"
                    world[literal_eval(coord)]["directions"][walkable]\
                        = "You see a house with a door on it. On the door there is a blue ribbon."
                else:
                    _status = "You need a specific item to do that"
        elif interactive_item == "chest":
            if inventory.is_in_inventory(square["interactions"]["key"]):
                if action in square["interactions"]["action"]:
                    if inventory.hidden_info(interactive_item):
                        _status = square["interactions"]["happening"]
            else:
                _status = "You need a specific item to do that"
    if action == "interact":
        if inventory.is_in_inventory(square["interactions"]["key"]):
            if action in square["interactions"]["action"]:
                _status = square["interactions"]["happening"]
        else:
            _status = "You need a specific item to do that"
    if action == "pull":
        pass
    if action == "touch":
        pass


def look(square, in_put, inventory):
    """look here takes all the "look" input the player gives"""
    possible_interactions = square["interactions"]
    cardinals = ("north", "south", "east", "west")

    if "at" == in_put[1]:
        try:
            if inventory.is_in_inventory(in_put[1]):  # In case player has an item from the square in his inventory
                return "What do you mean?"
            else:
                return possible_interactions[in_put[1]]["desc"]
        except KeyError:
            return "You can't do that"
    if "around" == in_put[1]:
        output = str()
        output += square["description"]["place"] + "\n"
        output += "You see:"
        for keys, values in square["items"].items():
            if inventory.is_in_inventory(keys):  # Can't look at something you already have
                pass
            else:
                output += "{}\n".format(values["desc"])
        return "{:^}\n".format(output)
    if in_put[1] in cardinals:  # When player is looking in a given direction
        try:
            return square["directions"][in_put[1]]
        except KeyError:
            return "Where did you want to look?"


def walker(square_neighs, in_put, world_int, posit, world):
    """Walker takes care of all things walking, where the player is placed both in a given map, and when walking to
    the next map"""

    dirr = str()
    _status = ""
    direction = posit
    try:
        for key, value in square_neighs.items():
            if key[0] == in_put[0]:
                steps = key
        direction = tuple(square_neighs[steps]["coord"])
    except KeyError:  # In case player inputs wrong direction
        _status = "Where did you want to walk?"
    if square_neighs[steps]["walk"] == "yes":
        # This is for when player is walking through to another map
        if square_neighs[steps]["tunnel"] == "yes":
            direction = (square_neighs[steps]["placement"][0],
                         square_neighs[steps]["placement"][1])
            world_int = square_neighs[steps]["world"]
            _status = "You're walking in a dark tunnel"
        else:
            _status = world[direction]["description"]["place"]
    else:
        _status = ("Can't walk there because {}"
                   .format(square_neighs[steps]["why"]))
        direction = posit

    return direction, _status, world_int


def pickup(item_pool, in_put, inventory):
    """Handles all things related to the inventory of the player, and adding things there"""
    try:
        if item_pool[in_put]["pickup"] == "yes":
            inventory.add_item(items.Item(in_put, item_pool[in_put]["desc"], item_pool[in_put]["hidden_info"]))
            return "Picked {} up".format(in_put)
        else:
            return "Can't pick {} up".format(in_put)
    except KeyError or IndexError:
        return "What did you want to pickup?"


def inputter(in_put, posit, square, inventory, world_int, save, walk_world):
    """Inputter here is what takes commands, and sends them further along on its journey."""
    item_pool = square["items"]
    walking = square["neighbours"]
    inputs = in_put.split(" ")
    _status = str()

    looper = True
    if "look" == inputs[0]:
        _status = look(square, inputs, inventory)
    if inputs[0] in ["go", "walk"]:
        posit, _status, world_int = walker(walking, inputs[1], world_int, posit, walk_world)
    if "pickup" == inputs[0]:
        _status = pickup(item_pool, inputs[1], inventory)
    if "inventory" == in_put or "inv" == in_put:
        _status = inventory
    if "interact with" in in_put or "touch" in inputs[0] or "pull" in inputs[0] or "open" in inputs[0]:
        if "interact with" in in_put:
            input_item = inputs[2]
        else:
            input_item = inputs[1]
        interacter(square, posit, inventory, inputs[0], input_item, walk_world)
    if "where am I" in in_put:
        _status = str(posit) + "\n" + str(world_int)
    if "save" in in_put:
        save.debug("{}\n{}\n{}\n".format(posit, world_int, inventory.saveer()))
    if "exit" in in_put:
        looper = False
    return _status, posit, world_int, looper


def main_part(posit=wc.SPAWN, world_int=0, incoming_inventory=None):
    """This initialises the whole thing, and is mostly used as a starting-point"""
    _status = str()
    looper = True
    if incoming_inventory:
        inventory = incoming_inventory
    else:
        inventory = items.Inventory()

    logger, save = b.create_logger()
    worlds = open_file()

    _status = "Enter description text here\n"
    while looper:
        world = worlds[world_int]  # world_int is taken from the map itself, and goes 0=world_1, 1=world_2 etc
        square = world[posit]  # This is the ground-square the player is standing on.
        logger.info("Posit: {}\nWorld: {}\nInv: {}"
                    .format(posit, world_int, inventory))
        print_to_screen(_status, mapper(world, posit, inventory))
        in_put = input("What do you want to do?\n")
        _status, posit, world_int, looper = inputter(in_put, posit, square, inventory, world_int, save, world)
    else:
        b.clear_console()
        print_to_screen("Do you want to save?\n")
        in_put = input("yes/no: ")
        if in_put == "yes":
            save.debug("{}\n{}\n{}\n"
                       .format(posit, world_int, inventory.saveer()))
            sys.stdout.write("Goodbye\n")
        elif in_put == "no":
            sys.stdout.write("Goodbye\n")
        else:
            b.clear_console()
            pass


if __name__ == '__main__':
    """This is the stuff that is first printed out"""
    b.set_console()
    sys.stdout.write("Start, or reload world\n")
    interput = input("What do you want to do?\n")
    if interput == "start":
        b.clear_console()
        interput = input("Do you want to load a save?\n")
        if interput == "yes":
            try:
                inventory_outside = items.Inventory()
                position, world_int_save, inventory_out = load_save(inventory_outside)
                main_part(literal_eval(position),
                          literal_eval(world_int_save),
                          inventory_out)
            except IndexError:
                main_part()
        if interput == "no":
            main_part()
    if interput == "reload world":
        b.clear_console()
        ausput = input("Are you really sure?\n")
        if ausput == "yes":
            wc.runner()
        elif ausput == "no":
            main_part()
    # wc.mapping()

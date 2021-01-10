import CODE.InputOutput as b
import CODE.items as items
from time import sleep
from ast import literal_eval
import CODE.world_creator as wc


def mapper(world, posit, inventory, size):
    """Handles the map, and its format"""

    x_axis, y_axis = size
    _printer = []
    _i = x_axis
    if inventory.is_in_inventory("map"):
        for _cell in world:
            if world[_cell]["mapping"] != wc.RIM:
                if world[_cell] != world[posit]:
                    _printer.append(b.get_print_value(world[_cell]["mapping"]))
                else:
                    _printer.append(b.get_print_value(wc.PLAYER))
            else:
                _printer.append(b.get_print_value(wc.RIM))

        while _i < len(_printer):
            _printer.insert(_i, "\n")  # Adds linebreaks where needed.
            _i += x_axis + 1

        return "{}".format(''.join(_printer))  # Prints the map out
    else:
        return " "


def place_description_global(world, posit):
    """Just takes the description of the place the player currently is in"""

    return world[posit]["description"]["place"] + "\n"


def door_opener(square, world, door_square, dirr, key_item):
    """This handles the opening of doors"""

    door_interact = square["neighbours"][dirr]

    def updater_door(incoming_order, updater_world_door):
        for each in incoming_order:
            coords, direction = each.split("\n")
            updater_world_door[literal_eval(coords)]["neighbours"][direction]["walk"] = "yes"
            updater_world_door[literal_eval(coords)]["directions"][direction] = "You see an open door"

    if door_square:
        if door_square["key_needed"] == "no":
            input_orders = door_interact["if_open"].split("\t")
            updater_door(input_orders, world)
            _status = "You opened the door"
            return _status
        else:
            if key_item == door_square["key_needed"]:
                input_orders = door_interact["if_open"].split("\t")
                updater_door(input_orders, world)
                _status = "You opened the door with the {}".format(key_item)
                return _status
            else:
                _status = "That's the wrong key"
                return _status


def interacter(square, inventory, action, key_item, interactive_item):
    """This handles everything regarding interactions with things in the world"""

    def chest_opener(inventory_chest_adder, incoming_interactions):
        if incoming_interactions["happening"]:
            incoming_interactions["desc"] = "the {} seems {}ed".format(interactive_item, action)
            chest_items = incoming_interactions["happening"].split("\t")
            for things in chest_items:
                name, desc, hidden = things.split("\n")
                inventory_chest_adder.add_item(items.Item(name,
                                                          desc,
                                                          hidden))
            return "You opened the chest and got some items"
        else:
            return "There's nothing in the chest"
    try:
        sleep(2)
        interactions = square["interactions"][interactive_item]
        _status = ""
        if action == "open":
            if interactive_item == "chest":
                if action in interactions["action"]:
                    if interactions["key"] != "no":
                        if key_item == interactions["key"]:
                            _status = chest_opener(inventory, interactions)
                        else:
                            _status = "That's the wrong item"
                    else:
                        _status = chest_opener(inventory, interactions)
        if action == "interact":
            if inventory.is_in_inventory(interactions["key"]):
                if action in interactions["action"]:
                    _status = interactions["happening"]
            else:
                _status = "You need a specific item to do that"
        if action == "pull":
            pass
        if action == "touch":
            pass
    except KeyError:
        _status = "You can't {} that {}".format(action, interactive_item)

    return _status


def look(square, in_put, inventory):
    """look here takes all the "look" input the player gives"""

    possible_interactions = square["interactions"]
    possible_items = square["items"]
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
        output += "You see:\n"
        for keys, values in possible_items.items():
            if inventory.is_in_inventory(keys):  # Can't look at something you already have
                pass
            else:
                output += "{}\n".format(values["desc"])
        output += "You also see:\n"
        for openables, values in possible_interactions.items():
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
            inventory.add_item(items.Item(item_pool[in_put]["name"],
                                          item_pool[in_put]["desc"],
                                          item_pool[in_put]["hidden_info"]))
            return "Picked {} up".format(in_put)
        else:
            return "Can't pick {} up".format(in_put)
    except KeyError:
        return "What did you want to pickup?"


def inputter(in_put, posit, square, inventory, world_int, save, walk_world):
    """Inputter here is what takes commands, and sends them further along on its journey."""

    inputs = in_put.split(" ")
    _status = str()

    looper = True
    if "look" == inputs[0]:
        if square["mapping"] != wc.DOORS:
            _status = look(square, inputs, inventory)
        else:
            _status = "There's nothing to see here"
    if inputs[0] in ["go", "walk"]:
        walking = square["neighbours"]
        posit, _status, world_int = walker(walking, inputs[1], world_int, posit, walk_world)
    if "pickup" == inputs[0]:
        if square["mapping"] != wc.DOORS:
            item_pool = square["items"]
            item = " ".join(inputs[1:])
            _status = pickup(item_pool, item, inventory)
        else:
            _status = "There's nothing to pick up here"
    if "inventory" == in_put or "inv" == in_put:
        _status = inventory
    if "interact" in in_put or "touch" in inputs[0] or "pull" in inputs[0] or "open" in inputs[0]:
        if "door" in in_put:
            if "the" in in_put:
                nyckel = " ".join(inputs[-2:])
                direction = inputs[4]
                door = walk_world[tuple(square["neighbours"][direction]["coord"])]
                _status = door_opener(square, walk_world, door, direction, nyckel)
            else:
                nyckel = " ".join(inputs[-2:])
                direction = inputs[3]
                door = walk_world[tuple(square["neighbours"][direction]["coord"])]
                _status = door_opener(square, walk_world, door, direction, nyckel)
        elif "door" not in in_put:
            if "interact" in in_put:
                input_item = " ".join(inputs[2:])
            else:
                input_item = inputs[1]
            _status = interacter(square, inventory, inputs[0], " ".join(inputs[3:]), input_item)
    if "where am I" in in_put:
        _status = str(posit) + "\n" + str(world_int)
    if "save" in in_put:
        save.debug("{}\n{}\n{}\n".format(posit, world_int, inventory.saveer()))
        _status = "The game has been saved"
    if "exit" in in_put:
        looper = False
    return _status, posit, world_int, looper


def main_part(_status, posit=wc.SPAWN, world_int=0, incoming_inventory=None):
    """This initialises the whole thing, and is mostly used as a starting-point"""

    _status = str()
    looper = True
    if incoming_inventory:
        inventory = incoming_inventory
    else:
        inventory = items.Inventory()

    logger, save, screen = b.create_logger()
    worlds, world_size = b.open_file()
    while looper:
        world_size_num = world_size[world_int]
        world = worlds[world_int]  # world_int is taken from the map itself, and goes 0=world_1, 1=world_2 etc
        square = world[posit]  # This is the ground-square the player is standing on.
        logger.info("Posit: {}\nWorld: {}\nInv: {}"
                    .format(posit, world_int, inventory))
        b.print_to_screen(_status, mapper(world, posit, inventory, world_size_num))
        in_put = input("What do you want to do?\n")
        _status, posit, world_int, looper = inputter(in_put, posit, square, inventory, world_int, save, world)
    else:
        b.clear_console()
        b.print_to_screen("Do you want to save?\n")
        in_put = input("yes/no: ")
        if in_put == "yes":
            save.debug("{}\n{}\n{}\n"
                       .format(posit, world_int, inventory.saveer()))
            b.print_to_screen("The game has been saved\n\tGoodbye\n")
        elif in_put == "no":
            b.print_to_screen("Goodbye\n")
        else:
            b.clear_console()
            pass


if __name__ == '__main__':
    """This is the stuff that is first printed out"""

    b.set_console()
    b.print_to_screen("Start, or reload world\n")
    interput = input("What do you want to do?\n")
    if interput == "start":
        b.clear_console()
        interput = input("Do you want to load a save?\n")
        if interput == "yes":
            try:
                inventory_outside = items.Inventory()
                position, world_int_save, inventory_out = b.load_save(inventory_outside)
                ingoing_status = "The save has loaded"
                main_part(ingoing_status, literal_eval(position),
                          literal_eval(world_int_save),
                          inventory_out)
            except IndexError:
                ingoing_status = "Enter description text here\n"
                main_part(ingoing_status)
        if interput == "no":
            ingoing_status = "Enter description text here\n"
            main_part(ingoing_status)
    if interput == "reload world":
        b.clear_console()
        ausput = input("Are you really sure?\n")
        if ausput == "yes":
            wc.runner()
        elif ausput == "no":
            ingoing_status = "Starting the game"
            main_part(ingoing_status)
    # wc.mapping()

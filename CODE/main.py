import CODE.InputOutput as InOut
import CODE.logger as Logger
import CODE.items as items
from time import sleep
from ast import literal_eval
import CODE.world_creator as wc
import CODE.world as World_code

import CODE.char as Char


World: World_code.world


def mapper(char: Char) -> string:
    if char.is_in_inventory("map"):
        return World.print_map()
    else:
        return " "


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
    elif inputs[0] in ["go", "walk"]:
        walking = square["neighbours"]
        posit, _status, world_int = walker(walking, inputs[1], world_int, posit, walk_world)
    elif "pickup" == inputs[0]:
        if "inventory" == in_put or "inv" == in_put:
            _status = inventory
    elif "interact" in in_put or "touch" in inputs[0] or "pull" in inputs[0] or "open" in inputs[0]:
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
    elif "where am I" in in_put:
        _status = str(posit) + "\n" + str(world_int)
    elif "save" in in_put:
        save.debug("{}\n{}\n{}\n".format(posit, world_int, inventory.saveer()))
        _status = "The game has been saved"
    elif "exit" in in_put:
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

    logger, save, screen = Logger.create_logger()
    while looper:
        World = World_code.world(world_int, posit)
        logger.info("Posit: {}\nWorld: {}\nInv: {}"
                    .format(posit, World.world_int, inventory))
        InOut.print_to_screen(_status, mapper(world, posit, inventory, World.world_size_num))
        in_put = input("What do you want to do?\n")
        _status, posit, world_int, looper = inputter(in_put, posit, square, inventory, world_int, save, world)
    else:
        InOut.clear_console()
        InOut.print_to_screen("Do you want to save?\n")
        in_put = input("yes/no: ")
        if in_put == "yes":
            save.debug("{}\n{}\n{}\n"
                       .format(posit, world_int, inventory.saveer()))
            InOut.print_to_screen("The game has been saved\n\tGoodbye\n")
        elif in_put == "no":
            InOut.print_to_screen("Goodbye\n")
        else:
            InOut.clear_console()
            pass


def main():
    InOut.set_console()
    InOut.print_to_screen("Start, or reload world\n")
    interput = input("What do you want to do?\n")
    if interput == "start":
        InOut.clear_console()
        interput = input("Do you want to load a save?\n")
        if interput == "yes":
            try:
                inventory_outside = items.Inventory()
                position, world_int_save, inventory_out = InOut.load_save(inventory_outside)
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
        InOut.clear_console()
        ausput = input("Are you really sure?\n")
        if ausput == "yes":
            wc.runner()
        elif ausput == "no":
            ingoing_status = "Starting the game"
            main_part(ingoing_status)
    # wc.mapping()


if __name__ == '__main__':
    main()

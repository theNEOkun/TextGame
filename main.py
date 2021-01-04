import json
import Base as b
from ast import literal_eval
import world_creator as wc

INVENTORY = dict()


def open_file():
    the_world = dict()

    with open("_RESOURCES/world.json", "r") as infile:
        data = json.load(infile)

    for key, value in data.items():
        the_world[literal_eval(key)] = data[key]

    return the_world


def place_description(world, posit):
    b.clear_console()
    b.fancy()
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
                output += "{}\n".format(values["description"])
            b.progress("{:^}\n".format(output))
        if inputs[1] in cardinals:
            try:
                b.progress(square["directions"][inputs[1]] + "\n")
            except KeyError:
                b.progress("Where did you want to look?\n")


def walker(world, posit, in_put):
    inputs = in_put.split(" ")
    try:
        direction = tuple(world[posit]["neighbours"][inputs[1]])
        if world[direction]:
            place_description(world, direction)
            return direction
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


def inputter(world, posit):
    in_put = str()
    while in_put != "exit":
        square = world[posit]
        b.progress(str(posit) + "\n")
        b.progress("What do you want to do?\n")
        in_put = input()
        if "look" in in_put:
            look(square, in_put)
        if "walk" in in_put:
            posit = walker(world, posit, in_put)
        if "pickup" in in_put:
            pickup(square, in_put)
        if "open" in in_put:
            print(INVENTORY)
    else:
        b.clear_console()
        b.progress("Goodbye")


def main_part():
    world = open_file()
    posit = (4, 0)
    b.set_console()
    place_description(world, posit)
    inputter(world, posit)


if __name__ == '__main__':
    main_part()
    # wc.creator()

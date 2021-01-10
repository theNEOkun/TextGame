import json
import itertools
import CODE.InputOutput as b
from time import sleep
from ast import literal_eval

"""LEGEND:
NEXT_MAP means where the next map "is"
PLACEMENT means where you will be placed on that map
NEXT_WORLD is the world number in the list (0=1, 1=2 etc.)
The direction that is there is in relation to the current map, so south of world_2 is world_3
coordinates go (y, x) not (x, y)"""

# The size of each map piece

# Global spawn
SPAWN = (0, 4)

"""Here is the list of maps, and where the doors are"""

WORLDS = {"world_1":
    {"TUNNEL":
        [
            (4, 8)
        ],
        "east": {
            "NEXT_MAP":
                (4, 9),
            "PLACEMENT":
                (4, 0),
            "NEXT_WORLD":
                1,
            "KEY": "no"
        },
        "WORLDS": "x",
        "SIZE": [9, 9]
    },
    "world_2":
        {"TUNNEL":
            [
                (4, 0),
                (8, 5)
            ],
            "west": {
                "NEXT_MAP":
                    (4, -1),
                "PLACEMENT":
                    (4, 8),
                "NEXT_WORLD":
                    0,
                "KEY": "no"
            },
            "south": {
                "NEXT_MAP":
                    (9, 5),
                "PLACEMENT":
                    (0, 5),
                "NEXT_WORLD":
                    2,
                "KEY": "no"
            },
            "WORLDS": "x",
            "SIZE": [9, 9]
        },
    "world_3":
        {"TUNNEL":
            [
                (0, 5),
                (4, 8)
            ],
            "north": {
                "NEXT_MAP":
                    (-1, 5),
                "PLACEMENT":
                    (8, 5),
                "NEXT_WORLD":
                    1,
                "KEY": "no"
            },
            "east": {
                "NEXT_MAP":
                    (4, 9),
                "PLACEMENT":
                    (4, 0),
                "NEXT_WORLD":
                    3,
                "KEY": "no"
            },
            "WORLDS": "x",
            "SIZE": [9, 9]
        },
    "world_4":
        {"TUNNEL":
            [
                (4, 0)
            ],
            "west": {
                "NEXT_MAP":
                    (4, -1),
                "PLACEMENT":
                    (4, 8),
                "NEXT_WORLD":
                    2,
                "KEY": "no"
            },
            "WORLDS": "x",
            "SIZE": [13, 13]
        }
}

THINGS_IN_WORLD = {"world_1": {"building": [(3, 3),
                                            (3, 4),
                                            (3, 5),
                                            (4, 3),
                                            (5, 3),
                                            (5, 4),
                                            (5, 5)],
                               "road": [(1, 4),
                                        (2, 4),
                                        (4, 6),
                                        (4, 7)],
                               "door": [
                                   (4, 5)]},
                   "world_2": {"building": [],
                               "road": [],
                               "door": []},
                   "world_3": {"building": [],
                               "road": [],
                               "door": []},
                   "world_4": {"building": [],
                               "road": [],
                               "door": []}
                   }

# This is used to iterate over when setting each map
WORLD_NAMES = ("world_1", "world_2", "world_3", "world_4")


RIM, GROUND, PLAYER, ROAD, BUILDING, DOORS, TUNNEL = 'M', ' ', 'P', 'R', 'B', 'D', 'T'

NON_WALKABLES = BUILDING, RIM

CARDINALS = ["north", "south", "west", "east"]


def rim_border(each, is_door=None):
    """This creates the borders, and adds the things that are needed in it"""
    return {"description":
                {"place": "How did you get here?"
                 },
            "directions":
                {"north": "placeholder",
                 "south": "placeholder",
                 "west": "placeholder",
                 "east": "placeholder"
                 },
            "interactions":
                {"interact1": "placeholder"
                 },
            "neighbours": calc_neigh(each, is_door, "rim"),
            "mapping": RIM
            }


def central(each):
    """This creates the ground the character walks on, and adds the things that are needed there"""
    return {"description":
                       {"place": "placeholder"
                        },
            "directions":
                {"north": "placeholder",
                 "south": "placeholder",
                 "west": "placeholder",
                 "east": "placeholder"
                 },
            "items":
                {"item1": {"desc": "placeholder",
                           "name": "placeholder",
                           "pickup": "no",
                           "hidden_info": "placeholder",
                           "action": "placeholder"
                           },
                 "item2": {"desc": "placeholder",
                           "name": "placeholder",
                           "pickup": "yes",
                           "hidden_info": "placeholder",
                           "action": "placeholder"
                           },
                 "item3": {"desc": "placeholder",
                           "name": "placeholder",
                           "pickup": "no",
                           "hidden_info": "placeholder",
                           "action": "placeholder"
                           }
                 },
            "interactions":
                {"interact1": {"desc": "placeholder",
                               "key": "no",
                               "action": "placeholder",
                               "happening": "placeholder"},
                 "interact2": {"desc": "placeholder",
                               "key": "no",
                               "action": "placeholder",
                               "happening": "placeholder"},
                 "interact3": {"desc": "placeholder",
                               "key": "no",
                               "action": "placeholder",
                               "happening": "placeholder"},
                 },
            "neighbours": calc_neigh(each),
            "key_needed": "no",
            "mapping": GROUND
            }


def creator_world(each, axis):
    """Used to differentiate between the borders of the screen, and the ground"""
    y_axis, x_axis = axis
    x_, y_ = each
    if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
        return rim_border(each)
    else:
        return central(each)


def calc_neigh(_cell_coord, is_a_door=None, rim=None):
    """Calculates the neighbours for the "ground" cells, and sets them with token values"""
    x_, y_ = _cell_coord
    neighbour = {}
    value = tuple()
    if rim and is_a_door:
        walk = "no"
    else:
        walk = "yes"
    for each in CARDINALS:
        if each == "north":
            value = tuple((x_-1, y_))
        elif each == "south":
            value = tuple((x_+1, y_))
        elif each == "west":
            value = tuple((x_, y_ - 1))
        elif each == "east":
            value = tuple((x_, y_ + 1))

        neighbour.update({each: {"coord": value, "walk": walk, "why": "placeholder", "tunnel": "no", "door": "no"}})

    return neighbour


def caretaker(key, world_grid, world_axis):
    """Caretaker here takes care of setting everything to what it should be"""

    def walkable(world_output_incoming, spawn, world_key):
        """This handles whether or not you can walk on any given piece of cell, and also handles which part that is a
        door"""

        for each_cell in world_output_incoming:
            neighbours = world_output_incoming[each_cell]["neighbours"]
            for card in neighbours:
                for info, value in neighbours[card].copy().items():
                    if info == "coord":
                        try:
                            if world_output_incoming[value]["mapping"] in NON_WALKABLES:
                                neighbours[card].update({"walk": "no",
                                                         "why": "it's a wall"})
                                world_output_incoming[each_cell]["directions"].update({card: "You see a wall"})
                                continue
                            else:
                                if world_output_incoming[value]["mapping"] == DOORS:
                                    neighbours[card].update({"walk": "no",
                                                             "why": "it's closed door",
                                                             "door": "yes",
                                                             "if_open": str(each_cell) + "\n" + card + "\t"})
                                    world_output_incoming[each_cell]["directions"].update({card: "You see a closed door"})
                                else:
                                    neighbours[card].update({"walk": "yes",
                                                             "why": "It's open ground"})
                                    world_output_incoming[each_cell]["directions"].update({card: "You see open ground"})
                                    continue
                        except KeyError:
                            if each_cell in WORLDS[world_key]["TUNNEL"]:
                                try:
                                    # This part takes care of adding the relevant data to the doors
                                    next_world = {"walk": "yes",
                                                  "why": "it's a tunnel",
                                                  "tunnel": "yes",
                                                  "world": WORLDS[world_key][card]["NEXT_WORLD"],
                                                  "placement": WORLDS[world_key][card]["PLACEMENT"],
                                                  "KEY": WORLDS[world_key][card]["KEY"]
                                                  }
                                    neighbours[card].update(next_world)
                                    world_output_incoming[each_cell]["directions"][card] = "it's a dark tunnel"
                                except KeyError:
                                    pass
                            else:
                                neighbours[card].update({"walk": "no",
                                                         "why": "there's nothing there"})
                            if each_cell == spawn:
                                world_output_incoming[each_cell]["directions"][card] = "You see a wall"
                                world_output_incoming[each_cell]["description"] = {"place": "You are in a cave"}
                            continue

    def doors_neighs(world_incoming):
        """"This handles adding the different sides of the doors to the neighbours of the door, so that it is
        opened from both sides."""

        walkable_neighbours = dict()
        for each_cell in world_incoming:
            if world_incoming[each_cell]["mapping"] == DOORS:
                neighbours = world_incoming[each_cell]["neighbours"]
                for card in neighbours:
                    for info, value in neighbours[card].items():
                        if info == "coord":
                            if world_incoming[value]["mapping"] in NON_WALKABLES:
                                continue
                            else:
                                walkable_neighbours.update({str(value): card})
                            if len(walkable_neighbours) < 2:
                                continue
                            elif len(walkable_neighbours) == 2:
                                all_neighs, all_dirr = walkable_neighbours.items()
                                all_coord1, all_dirr1 = all_neighs[0], all_dirr[1]
                                all_coord2, all_dirr2 = all_dirr[0], all_neighs[1]
                                world_incoming[literal_eval(all_coord1)]["neighbours"][all_dirr1]["if_open"] +=\
                                    all_coord2 + "\n" + all_dirr2
                                world_incoming[literal_eval(all_coord2)]["neighbours"][all_dirr2]["if_open"] += \
                                    all_coord1 + "\n" + all_dirr1

    def repeatables(each_cell, world_output_):
        if each_cell in set(WORLDS[key]["TUNNEL"]):
            world_output_[each_cell] = central(each_cell)
            world_output_[each_cell]["mapping"] = TUNNEL
        elif each_cell in set(THINGS_IN_WORLD[key]["building"]):
            world_output_[each_cell] = rim_border(each_cell)
            world_output_[each_cell]["mapping"] = BUILDING
        elif each_cell in set(THINGS_IN_WORLD[key]["road"]):
            world_output_[each_cell] = central(each_cell)
            world_output_[each_cell]["mapping"] = ROAD
        elif each_cell in set(THINGS_IN_WORLD[key]["door"]):
            world_output_[each_cell] = rim_border(each_cell, "is_door")
            world_output_[each_cell]["mapping"] = DOORS
            world_output_[each_cell]["description"] = "You're standing in the door frame"
            world_output_[each_cell]["key_needed"] = "yes"
        elif each not in set(WORLDS[key]["TUNNEL"]):
            world_output_.update({each: creator_world(each, world_axis)})

    world_output = dict()
    for each in world_grid:
        if key == "world_1":
            # This part handles "world_1" and spawn
            if each == SPAWN:
                world_output[SPAWN] = central(SPAWN)
                world_output[SPAWN]["mapping"] = ROAD
                continue
            repeatables(each, world_output)
        elif key != "world_1":
            # This bit handles everything else
            repeatables(each, world_output)

    walkable(world_output, SPAWN, key)
    doors_neighs(world_output)
    return world_output


def world_size(key):
    axis = x_axis, y_axis = WORLDS[key]["SIZE"]

    grid = itertools.product(range(x_axis), range(y_axis))

    return grid, axis


def runner():
    """Runner takes care of starting caretaker and ouputting to file"""
    ouput_file = dict()
    for world in WORLD_NAMES:
        output = "{}.json".format(world)
        with open(b.RESOURCES / output, "w") as outfile:
            ouput_file["world_size"] = {"size": WORLDS[world]["SIZE"]}
            grid, axis = world_size(world)
            ouput_file["world"] = caretaker(world, grid, axis)
            json.dump({x: {str(k): v for k, v in val.items()} for x, val in ouput_file.items()}, outfile, indent=4)

import json
import itertools
from cell import World_Cell
from time import sleep

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


def rim_border(coords: tuple, is_door=None) -> World_Cell:
    """This creates the borders, and adds the things that are needed in it"""
    description = {"place": "How did you get here?", "look": "It's a wall"}
    return World_Cell(coords, description, None, None, RIM)


def world_cell(coords: tuple) -> World_Cell:
    description = {"place": "It is grassland", "look": "You see grassland"}
    return World_Cell(coords, description, None, None, GROUND)


def central(coords: tuple) -> World_Cell:
    """This creates the ground the character walks on, and adds the things that are needed there"""
    description = {"description":
                       {"place": "placeholder"
                        }
                       }
    items = {"items":
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
                 }}
    interactions = {"interactions":
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
             }
            }
    return World_Cell(coords, description, items, interactions, GROUND)


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

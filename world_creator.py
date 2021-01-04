import json
import itertools
from pathlib import Path

RESOURCES = Path(__file__) / "_RESOURCES/"


def creator():
    x_axis = range(9)
    y_axis = range(9)
    world = dict()

    grid = itertools.product(x_axis, y_axis)

    print(grid)

    for each in grid:
        x_, y_ = each
        if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
            world[each] = None  # Set to none and skip onwards
            continue
        else:
            world[each] = {"description": {"place": "placeholder"}}
            world[each].update({"directions":
                                {"north": "placeholder",
                                 "south": "placeholder",
                                 "west": "placeholder",
                                 "east": "placeholder"
                                 },
                                "items":
                                    {"item1": {"desc": "placeholder",
                                               "pickup": "no"},
                                     "item2": {"desc": "placeholder",
                                               "pickup": "yes"},
                                     "item3": {"desc": "placeholder",
                                               "pickup": "no"}
                                     },
                                "interactions":
                                    {"interact1": "placeholder",
                                     "interact2": "placeholder",
                                     "interact3": "placeholder"
                                     },
                                "neighbours": calc_neigh(each)
                                }
                               )

    with open("_RESOURCES/world.json", "w") as outfile:
        json.dump({str(k): v for k, v in world.items()}, outfile, indent=4)


def calc_neigh(_cell_coord):
    x_, y_ = _cell_coord
    neighbour = {}
    neighbour.update({"north": (x_, y_-1)})
    neighbour.update({"south": (x_, y_+1)})
    neighbour.update({"west": (x_-1, y_)})
    neighbour.update({"east": (x_+1, y_)})

    return neighbour

import json
import itertools
from pathlib import Path

RESOURCES = Path(__file__) / "_RESOURCES/"


def mapping():
    x_axis = 9
    y_axis = 9
    mapp = dict()

    grid = itertools.product(range(x_axis), range(y_axis))

    for each in grid:
        x_, y_ = each
        if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
            mapp[each] = None  # Set to none and skip onwards
            continue
        else:
            mapp[each] = {"part": "-"}

    mapp[(0, 4)] = {"part": "-"}

    with open("_RESOURCES/mapp.json", "w") as outfile:
        json.dump({str(k): v for k, v in mapp.items()}, outfile, indent=4)


def creator():
    x_axis = 9
    y_axis = 9
    world = dict()

    grid = itertools.product(range(x_axis), range(y_axis))

    for each in grid:
        x_, y_ = each

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
                            "neighbours": calc_neigh(each),
                            "mapping": "-"
                            }
                           )
        if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
            if world[each] == (4, 0):
                world[(0, 4)]["mapping"] = "-"
            world[each]["mapping"] = "#"  # Set to none and skip onwards
            continue

    with open("_RESOURCES/world.json", "w") as outfile:
        json.dump({str(k): v for k, v in world.items()}, outfile, indent=4)


def calc_neigh(_cell_coord):
    x_, y_ = _cell_coord
    neighbour = {}
    neighbour.update({"north": {"coord": (x_, y_-1), "walk": "no", "why": "placeholder"}})
    neighbour.update({"south": {"coord": (x_, y_+1), "walk": "no", "why": "placeholder"}})
    neighbour.update({"west": {"coord": (x_-1, y_), "walk": "no", "why": "placeholder"}})
    neighbour.update({"east": {"coord": (x_+1, y_), "walk": "no", "why": "placeholder"}})

    return neighbour

import json
import itertools
from pathlib import Path

RESOURCES = Path(__file__) / "_RESOURCES/"

spawn = (0, 4)

RIM, GROUND, PLAYER = 'M', ' ', 'T'


def rim_border(world, each):
    world[each] = {"description":
                       {"place": "How did you get here?"
                        },
                   "interactions":
                       {"interact1": "placeholder"
                        },
                   "neighbours": calc_neigh_rim(each),
                   "mapping": RIM
                   }


def central(world, each):
    world[each] = {"description":
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
                                  "pickup": "no"
                                  },
                        "item2": {"desc": "placeholder",
                                  "pickup": "yes"
                                  },
                        "item3": {"desc": "placeholder",
                                  "pickup": "no"
                                  }
                        },
                   "interactions":
                       {"interact1": "placeholder",
                        "interact2": "placeholder",
                        "interact3": "placeholder"
                        },
                   "neighbours": calc_neigh(each),
                   "mapping": GROUND
                   }


def creator():
    x_axis = 9
    y_axis = 9
    world = dict()

    grid = itertools.product(range(x_axis), range(y_axis))

    for each in grid:
        x_, y_ = each
        if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
            if each == spawn:
                central(world, each)
            else:
                rim_border(world, each)
        else:
            central(world, each)

    walkable(world)

    with open("_RESOURCES/world.json", "w") as outfile:
        json.dump({str(k): v for k, v in world.items()}, outfile, indent=4)


def calc_neigh(_cell_coord):
    x_, y_ = _cell_coord
    neighbour = {}

    neighbour.update({"north": {"coord": tuple((x_-1, y_)), "walk": "yes", "why": "placeholder"}})
    neighbour.update({"south": {"coord": tuple((x_+1, y_)), "walk": "yes", "why": "placeholder"}})
    neighbour.update({"west": {"coord": tuple((x_, y_-1)), "walk": "yes", "why": "placeholder"}})
    neighbour.update({"east": {"coord": tuple((x_, y_+1)), "walk": "yes", "why": "placeholder"}})

    return neighbour


def calc_neigh_rim(_cell_coord):
    x_, y_ = _cell_coord
    neighbour_rim = {}

    neighbour_rim.update({"north": {"coord": tuple((x_-1, y_)), "walk": "no", "why": "placeholder"}})
    neighbour_rim.update({"south": {"coord": tuple((x_+1, y_)), "walk": "no", "why": "placeholder"}})
    neighbour_rim.update({"west": {"coord": tuple((x_, y_-1)), "walk": "no", "why": "placeholder"}})
    neighbour_rim.update({"east": {"coord": tuple((x_, y_+1)), "walk": "no", "why": "placeholder"}})

    return neighbour_rim


def walkable(world):
    for each in world:
        for card in world[each]["neighbours"]:
            for key, value in world[each]["neighbours"][card].items():
                if key == "coord":
                    try:
                        if world[value]["mapping"] == RIM:
                            world[each]["neighbours"][card].update({"walk": "no"})
                            world[each]["neighbours"][card].update({"why": "it's a wall"})
                            world[each]["directions"].update({card: "You see a wall"})
                        else:
                            world[each]["neighbours"][card].update({"walk": "yes"})
                            world[each]["neighbours"][card].update({"why": "It's open ground"})
                            world[each]["directions"].update({card: "You see open ground"})
                    except KeyError:
                        world[each]["neighbours"][card].update({"walk": "no"})
                        world[each]["neighbours"][card].update({"why": "there's nothing there"})
                        if each == spawn:
                            world[each]["directions"].update({card: "You see nothing there"})
                        continue

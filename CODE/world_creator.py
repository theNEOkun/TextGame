import json
import itertools
import CODE.Base as b



SPAWN = (0, 4)

WORLDS = {"world_1": {"DOORS":
                      (4, 8),
                      "NEXT_MAP":
                      (4, 9),
                      "PLACEMENT":
                      (4, 0),
                      "NEXT_WORLD":
                      1
                      },
          "world_2": {"DOORS":
                      (4, 0),
                      "NEXT_MAP":
                      (4, -1),
                      "PLACEMENT":
                      (4, 8),
                      "NEXT_WORLD":
                      0
                      }
          }


RIM, GROUND, PLAYER = 'M', ' ', 'T'


def rim_border(world, each):
    world[each] = {"description":
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
                       {"interact1": {"desc": "placeholder",
                                      "key": "no"},
                        "interact2": {"desc": "placeholder",
                                      "key": "no"},
                        "interact3": {"desc": "placeholder",
                                      "key": "no"},
                        },
                   "neighbours": calc_neigh(each),
                   "mapping": GROUND
                   }


def creator_world(grid, world, x_axis, y_axis, door, spawn=None):
    for each in grid:
        x_, y_ = each
        if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
            if spawn:
                if each == spawn or each == door:
                    central(world, each)
                else:
                    rim_border(world, each)
            else:
                if each == door:
                    central(world, each)
                else:
                    rim_border(world, each)
        else:
            central(world, each)

    return world


def calc_neigh(_cell_coord):
    x_, y_ = _cell_coord
    neighbour = {}

    neighbour.update({"north": {"coord": tuple((x_-1, y_)), "walk": "yes", "why": "placeholder", "door": "no"}})
    neighbour.update({"south": {"coord": tuple((x_+1, y_)), "walk": "yes", "why": "placeholder", "door": "no"}})
    neighbour.update({"west": {"coord": tuple((x_, y_-1)), "walk": "yes", "why": "placeholder", "door": "no"}})
    neighbour.update({"east": {"coord": tuple((x_, y_+1)), "walk": "yes", "why": "placeholder", "door": "no"}})

    return neighbour


def calc_neigh_rim(_cell_coord):
    x_, y_ = _cell_coord
    neighbour_rim = {}

    neighbour_rim.update({"north": {"coord": tuple((x_-1, y_)), "walk": "no", "why": "placeholder", "door": "no"}})
    neighbour_rim.update({"south": {"coord": tuple((x_+1, y_)), "walk": "no", "why": "placeholder", "door": "no"}})
    neighbour_rim.update({"west": {"coord": tuple((x_, y_-1)), "walk": "no", "why": "placeholder", "door": "no"}})
    neighbour_rim.update({"east": {"coord": tuple((x_, y_+1)), "walk": "no", "why": "placeholder", "door": "no"}})

    return neighbour_rim


def walkable(world, spawn):
    for each in world:
        for card in world[each]["neighbours"]:
            for key, value in world[each]["neighbours"][card].items():
                if key == "coord":
                    try:
                        if world[value]["mapping"] == RIM:
                            world[each]["neighbours"][card].update({"walk": "no", "why": "it's a wall"})
                            world[each]["directions"].update({card: "You see a wall"})
                        else:
                            world[each]["neighbours"][card].update({"walk": "yes", "why": "It's open ground"})
                            world[each]["directions"].update({card: "You see open ground"})
                    except KeyError:
                        world[each]["neighbours"][card].update({"walk": "no", "why": "there's nothing there"})
                        if each == spawn:
                            world[each]["directions"][card] = "You see a wall"
                            world[each]["description"] = {"place": "You see a dark cave"}
                        continue


def doors(world, next_map, placement, next_world):
    for each in world:
        for card in world[each]["neighbours"]:
            for key, value in world[each]["neighbours"][card].copy().items():
                if key == "coord":
                    try:
                        if next_map == value:
                            world[each]["neighbours"][card].update({"walk": "yes",
                                                                    "door": "yes",
                                                                    "world": next_world,
                                                                    "placement": str(placement)
                                                                    })
                            world[each]["directions"][card] = "it's a dark tunnel"
                        else:
                            pass
                    except KeyError:
                        continue


def caretaker(grid, world, x_axis, y_axis, number=0):
    vr = WORLDS
    for key, value in vr.items():
        print(key)
        if key == "world_1":
            spawn = SPAWN
        else:
            spawn = None
        print(spawn)
        print(vr[key]["DOORS"])
        print(vr[key]["NEXT_MAP"])
        output = "{}.json".format(key)
        vr[key]["WORLD"] = creator_world(grid, world, x_axis, y_axis, vr[key]["DOORS"], spawn)

        walkable(vr[key]["WORLD"], SPAWN)

        doors(vr[key]["WORLD"], vr[key]["NEXT_MAP"], vr[key]["PLACEMENT"], vr[key]["NEXT_WORLD"])

        with open(b.RESOURCES / output, "w") as outfile:
            json.dump({str(k): v for k, v in vr[key]["WORLD"].items()}, outfile, indent=4)


def runner():
    x_axis = 9
    y_axis = 9
    world = dict()
    x = 2
    grid = itertools.product(range(x_axis), range(y_axis))
    caretaker(grid, world, x_axis, y_axis, x)

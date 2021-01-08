import json
import itertools
import CODE.Base as b

x_axis = 9
y_axis = 9

SPAWN = (0, 4)

WORLDS = {"world_1": {"DOORS":
                      [
                          (4, 8)
                      ],
                      "east": {
                          "NEXT_MAP":
                          (4, 9),
                          "PLACEMENT":
                          (4, 0),
                          "NEXT_WORLD":
                          1
                      },
                      "WORLDS": "x"
                      },
          "world_2": {"DOORS":
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
                          0
                                },
                      "south": {
                          "NEXT_MAP":
                          (9, 5),
                          "PLACEMENT":
                          (0, 5),
                          "NEXT_WORLD":
                          2
                                },
                      "WORLDS": "x"
                      },
          "world_3": {"DOORS":
                      [
                          (0, 5)
                      ],
                      "north": {
                          "NEXT_MAP":
                              (-1, 5),
                          "PLACEMENT":
                              (8, 5),
                          "NEXT_WORLD":
                              1
                                },
                      "WORLDS": "x"
                      }
          }

WORLD_NAMES = ("world_1", "world_2", "world_3")


RIM, GROUND, PLAYER = 'M', ' ', 'T'


def rim_border(each):
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
                   "neighbours": calc_neigh_rim(each),
                   "mapping": RIM
                   }


def central(each):
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


def creator_world(each):
    x_, y_ = each
    if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
        return rim_border(each)
    else:
        return central(each)


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


'''def doors_walkable(world_output, world_key, each_thing):
    for card in world_output[each_thing]["neighbours"]:
        for key, value in world_output[each_thing]["neighbours"][card].copy().items():
            if key == "coord":
                if value == WORLDS[world_key]["DOORS"]:
                    world_output[each_thing]["neighbours"][card].update({"walk": "yes",
                                                                         "door": "yes",
                                                                         "world": WORLDS[world_key]["NEXT_WORLD"],
                                                                         "placement": WORLDS[world_key]["PLACEMENT"]
                                                                         })
                    world_output[each_thing]["directions"][card] = "it's a dark tunnel"'''


def walkable(world_output, spawn, world_key):

    for each in world_output:
        for card in world_output[each]["neighbours"]:
            for key, value in world_output[each]["neighbours"][card].copy().items():
                if key == "coord":
                    try:
                        if world_output[value]["mapping"] == RIM:
                            world_output[each]["neighbours"][card].update({"walk": "no",
                                                                           "why": "it's a wall"})
                            world_output[each]["directions"].update({card: "You see a wall"})
                            continue
                        else:
                            world_output[each]["neighbours"][card].update({"walk": "yes",
                                                                           "why": "It's open ground"})
                            world_output[each]["directions"].update({card: "You see open ground"})
                            continue
                    except KeyError:
                        if each in WORLDS[world_key]["DOORS"]:
                            try:
                                next_world = {"walk": "yes",
                                              "why": "it's a tunnel",
                                              "door": "yes",
                                              "world": WORLDS[world_key][card]["NEXT_WORLD"],
                                              "placement": WORLDS[world_key][card]["PLACEMENT"]
                                              }
                                world_output[each]["neighbours"][card].update(next_world)
                                world_output[each]["directions"][card] = "it's a dark tunnel"
                            except KeyError:
                                pass
                        else:
                            world_output[each]["neighbours"][card].update({"walk": "no",
                                                                           "why": "there's nothing there"})
                        if each == spawn:
                            world_output[each]["directions"][card] = "You see a wall"
                            world_output[each]["description"] = {"place": "You are in a cave"}
                        continue


def caretaker(key):
    grid = itertools.product(range(x_axis), range(y_axis))
    world_output = dict()
    for each in grid:
        if key == "world_1":
            if each == SPAWN:
                world_output[SPAWN] = central(SPAWN)
                continue
            if each in set(WORLDS[key]["DOORS"]):
                world_output[each] = central(each)
                continue
            elif each != SPAWN or each not in set(WORLDS[key]["DOORS"]):
                world_output.update({each: creator_world(each)})
                continue
        elif key != "world_1":
            if each in set(WORLDS[key]["DOORS"]):
                world_output[each] = central(each)
                continue
            elif each not in set(WORLDS[key]["DOORS"]):
                world_output.update({each: creator_world(each)})
                continue
    walkable(world_output, SPAWN, key)
    return world_output


def runner():
    for world in WORLD_NAMES:
        output = "{}.json".format(world)
        with open(b.RESOURCES / output, "w") as outfile:
            output = caretaker(world)
            json.dump({str(k): v for k, v in output.items()}, outfile, indent=4)

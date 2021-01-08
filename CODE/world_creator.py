import json
import itertools
import CODE.Base as b

"""LEGEND:
NEXT_MAP means where the next map "is"
PLACEMENT means where you will be placed on that map
NEXT_WORLD is the world number in the list (0=1, 1=2 etc.)
The direction that is there is in relation to the current map, so south of world_2 is world_3
coordinates go (y, x) not (x, y)"""

# The size of each map piece
x_axis = 9
y_axis = 9

# Global spawn
SPAWN = (0, 4)

"""Here is the list of maps, and where the doors are"""

WORLDS = {"world_1": {"TUNNEL":
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
                      "WORLDS": "x"
                      },
          "world_2": {"TUNNEL":
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
                      "WORLDS": "x"
                      },
          "world_3": {"TUNNEL":
                      [
                          (0, 5)
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
                      "WORLDS": "x"
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
                               "door": []}
                   }

# This is used to iterate over when setting each map
WORLD_NAMES = ("world_1", "world_2", "world_3")


RIM, GROUND, PLAYER, ROAD, BUILDING, DOORS, TUNNEL = 'M', ' ', 'P', 'R', 'B', 'D', 'T'

NON_WALKABLES = BUILDING, RIM


def rim_border(each):
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
            "neighbours": calc_neigh_rim(each),
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
                           "pickup": "no",
                           "hidden_info": "placeholder",
                           "action": "placeholder"
                           },
                 "item2": {"desc": "placeholder",
                           "pickup": "yes",
                           "hidden_info": "placeholder",
                           "action": "placeholder"
                           },
                 "item3": {"desc": "placeholder",
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


def creator_world(each):
    """Used to differentiate between the borders of the screen, and the ground"""
    x_, y_ = each
    if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
        return rim_border(each)
    else:
        return central(each)


def calc_neigh(_cell_coord):
    """Calculates the neighbours for the "ground" cells, and sets them with token values"""
    x_, y_ = _cell_coord
    neighbour = {}

    neighbour.update({"north": {"coord": tuple((x_-1, y_)), "walk": "yes", "why": "placeholder", "tunnel": "no"}})
    neighbour.update({"south": {"coord": tuple((x_+1, y_)), "walk": "yes", "why": "placeholder", "tunnel": "no"}})
    neighbour.update({"west": {"coord": tuple((x_, y_-1)), "walk": "yes", "why": "placeholder", "tunnel": "no"}})
    neighbour.update({"east": {"coord": tuple((x_, y_+1)), "walk": "yes", "why": "placeholder", "tunnel": "no"}})

    return neighbour


def calc_neigh_rim(_cell_coord):
    """Calculates the neighbours for the border cells and sets them with token values"""
    x_, y_ = _cell_coord
    neighbour_rim = {}

    neighbour_rim.update({"north": {"coord": tuple((x_-1, y_)), "walk": "no", "why": "placeholder", "tunnel": "no"}})
    neighbour_rim.update({"south": {"coord": tuple((x_+1, y_)), "walk": "no", "why": "placeholder", "tunnel": "no"}})
    neighbour_rim.update({"west": {"coord": tuple((x_, y_-1)), "walk": "no", "why": "placeholder", "tunnel": "no"}})
    neighbour_rim.update({"east": {"coord": tuple((x_, y_+1)), "walk": "no", "why": "placeholder", "tunnel": "no"}})

    return neighbour_rim


def walkable(world_output, spawn, world_key):
    """This handles whether or not you can walk on any given piece of cell, and also handles which part that is a
    door"""
    for each in world_output:
        for card in world_output[each]["neighbours"]:
            for key, value in world_output[each]["neighbours"][card].copy().items():
                if key == "coord":
                    try:
                        if world_output[value]["mapping"] in NON_WALKABLES:
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
                        if each in WORLDS[world_key]["TUNNEL"]:
                            try:
                                # This part takes care of adding the relevant data to the doors
                                next_world = {"walk": "yes",
                                              "why": "it's a tunnel",
                                              "tunnel": "yes",
                                              "world": WORLDS[world_key][card]["NEXT_WORLD"],
                                              "placement": WORLDS[world_key][card]["PLACEMENT"],
                                              "KEY": WORLDS[world_key][card]["KEY"]
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
    """Caretaker here takes care of setting everything to what it should be"""
    grid = itertools.product(range(x_axis), range(y_axis))
    world_output = dict()
    for each in grid:
        if key == "world_1":
            # This part handles "world_1" and spawn
            if each == SPAWN:
                world_output[SPAWN] = central(SPAWN)
                world_output[SPAWN]["mapping"] = ROAD
                continue
            elif each in set(WORLDS[key]["TUNNEL"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = TUNNEL
                continue
            elif each in set(THINGS_IN_WORLD[key]["building"]):
                world_output[each] = rim_border(each)
                world_output[each]["mapping"] = BUILDING
                continue
            elif each in set(THINGS_IN_WORLD[key]["road"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = ROAD
                continue
            elif each in set(THINGS_IN_WORLD[key]["door"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = DOORS
                world_output[each]["key_needed"] = "yes"
                continue
            elif each != SPAWN or each not in set(WORLDS[key]["TUNNEL"]):
                world_output.update({each: creator_world(each)})
                continue
        elif key != "world_1":
            # This bit handles everything else
            if each in set(WORLDS[key]["TUNNEL"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = DOORS
                continue
            elif each in set(THINGS_IN_WORLD[key]["building"]):
                world_output[each] = rim_border(each)
                world_output[each]["mapping"] = BUILDING
                continue
            elif each in set(THINGS_IN_WORLD[key]["road"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = ROAD
                continue
            elif each in set(THINGS_IN_WORLD[key]["door"]):
                world_output[each] = central(each)
                world_output[each]["mapping"] = DOORS
                world_output[each]["key_needed"] = "yes"
                continue
            elif each not in set(WORLDS[key]["TUNNEL"]):
                world_output.update({each: creator_world(each)})
                continue
    walkable(world_output, SPAWN, key)
    return world_output


def runner():
    """Runner takes care of starting caretaker and ouputting to file"""
    for world in WORLD_NAMES:
        output = "{}.json".format(world)
        with open(b.RESOURCES / output, "w") as outfile:
            output = caretaker(world)
            json.dump({str(k): v for k, v in output.items()}, outfile, indent=4)

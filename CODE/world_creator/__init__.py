import json
import itertools
from CODE.inventory import Item
import CODE.InputOutput as b
import CODE.world_creator.mappings as maps


class worldSize:
    world_size: list

    def to_json(self):
        return self.world_size

    def __getitem__(self, index):
        return self.world_size[index]

    def __init__(self, world_size: list):
        self.world_size = world_size



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
        "SIZE": worldSize([9, 9])
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
                               "door": [(4, 5)],
                               "spawn": [SPAWN]}
                   }

# This is used to iterate over when setting each map
WORLD_NAMES = ("world_1")


class worldCell:
    coords: tuple
    description: dict
    items: dict
    interactions: dict
    mapping: str
    walkable: bool

    def open(self, item: Item) -> bool:
        """Used to open if it is a door"""
        if self.mapping != maps.DOORS:
            return False
        if item.name == self.interactions["open_door"]["key"]:
            self.mapping = maps.GROUND
            return True


    def __str__(self):
        return json.dumps({
            "description": self.description,
            "items": self.items,
            "interactions": self.interactions,
            "mapping": self.mapping
        }, indent=4)


    def to_json(self):
        return {
            "description": self.description,
            "items": self.items,
            "interactions": self.interactions,
            "mapping": self.mapping
        }


    def __init__(self, coords, descr, items, interact, mapp):
        self.coords = coords
        self.description = descr
        self.items = items
        self.interactions = interact
        if mapp in maps.NON_WALKABLES:
            self.walkable = False
        self.mapping = mapp


def rim_cell(coords: tuple, is_door=None) -> worldCell:
    """This creates the borders, and adds the things that are needed in it"""
    description = {"place": "How did you get here?", "look": "You see mountains"}
    return worldCell(coords, description, None, None, maps.RIM)


def wall_cell(coords: tuple, is_door=None) -> worldCell:
    """This creates the borders, and adds the things that are needed in it"""
    description = {"place": "How did you get here?", "look": "It's a wall"}
    return worldCell(coords, description, None, None, maps.BUILDING)


def world_cell(coords: tuple) -> worldCell:
    description = {"place": "It is grassland", "look": "You see grassland"}
    return worldCell(coords, description, None, None, maps.GROUND)


def door_cell(coords: tuple) -> worldCell:
    description = {"description": {"place": "It is a door", "look": "You see a door"}}
    interactions = {
        "interactions": {"open_door": {"desc": "open", "key": "key", "action": "open", "happening": "door opened"}}}
    return worldCell(coords, description, None, interactions, maps.DOORS)


def road_cell(coords: tuple) -> worldCell:
    description = {"description": {"place": "It is a dirt path", "look": "you see a dirt path"}}
    return worldCell(coords, description, None, None, maps.ROAD)


def tunnel_cell(coords: tuple) -> worldCell:
    description = {"description": {"place": "You are in a dark cave", "look": "You see a cave"}}
    return worldCell(coords, description, None, None, maps.TUNNEL)


def central(coords: tuple) -> worldCell:
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
    return worldCell(coords, description, items, interactions, maps.GROUND)


def spawn_cell(coords: tuple) -> worldCell:
    description = {"description":
                       {"place": "you are standing in a dark cave",
                           "look": "It is a cave"
                        }
                   }
    return worldCell(coords, description, None, None, maps.ROAD)


def rim_or_cell(each: tuple, axis: tuple):
    """Used to differentiate between the borders of the screen, and the ground"""
    y_axis, x_axis = axis
    x_, y_ = each
    if x_ == 0 or y_ == 0 or x_ + 1 == y_axis or y_ + 1 == x_axis:  # If it is in any edge point
        True
    else:
        False


def create_grid(x_axis: int, y_axis: int):
    return itertools.product(range(x_axis), range(y_axis))


def world_size(key: str):
    """Used to get a grid of the entire world created, together with the sizes"""
    return WORLDS[key]["SIZE"]


def caretaker(world: str, grid: list, axis: tuple) -> dict:
    outgoing_world = {}
    curr_world = WORLDS[world]
    things = THINGS_IN_WORLD[world]
    for each in grid:
        if not rim_or_cell(each, axis):
            outgoing_world.update({each: check_special(each, things)})
        else:
            outgoing_world.update({each: check_world_parts(each)})

    return outgoing_world


def is_tunnel(coord: tuple, world: dict) -> bool:
    return coord in set(world["TUNNEL"])


def is_wall(coord: tuple, world: dict) -> bool:
    return coord in set(world["building"])


def is_door(coord: tuple, world: dict) -> bool:
    return coord in set(world["door"])


def is_road(coord: tuple, world: dict) -> bool:
    return coord in set(world["road"])


def is_spawn(coord: tuple, world: dict) -> bool:
    return coord in set(world["spawn"])


def check_world_parts(coord: tuple, world: dict, grid: list) -> worldCell:
    if is_tunnel(coord, world):
        return tunnel_cell(coord)
    else:
        return rim_cell(coord, grid)


def check_special(coord: tuple, world: dict) -> worldCell:
    if is_spawn(coord, world):
        return spawn_cell(coord)
    elif is_wall(coord, world):
        return wall_cell(coord)
    elif is_road(coord, world):
        return road_cell(coord)
    elif is_door(coord, world):
        return door_cell(coord)
    else:
        return world_cell(coord)


def runner():
    """Runner takes care of starting caretaker and outputting to file"""
    ouput_file = dict()
    world = WORLD_NAMES
    output = "{}.json".format(world)
    with open(b.RESOURCES / output, "w") as outfile:
        ouput_file["world_size"] = {"size": WORLDS[world]["SIZE"]}
        axis = world_size(world)
        grid = create_grid(axis[0], axis[1])
        ouput_file["world"] = caretaker(world, grid, axis)
        json.dump({str(world_info): {str(key): val.to_json() for key, val in world_data.items()} for world_info, world_data in ouput_file.items()}, outfile, indent=4)


if __name__ == '__main__':
    runner()

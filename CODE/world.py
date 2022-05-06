import CODE.InputOutput as InOut
import CODE.world_creator as wc

class world:
    all_worlds: dict
    world: dict
    world_size: tuple
    world_size_num: int

    char_pos: tuple
    curr_square: dict


    def walk(self, char_pos: tuple):
        self.char_pos = char_pos
        self.curr_square = world[char_pos]


    def change_world(self, world_int: int):
        self.world = world[world_int]
        self.world_size_num = self.world_size[world_int]


    def interact(self):
        pass


    def open_door(self, door_square: tuple, dirr: string):

        door_interact = curr_square["neighbours"][dirr]

        """This handles the opening of doors"""

        def updater_door(incoming_order, updater_world_door):
            for each in incoming_order:
                coords, direction = each.split("\n")
                updater_world_door[literal_eval(coords)]["neighbours"][direction]["walk"] = "yes"
                updater_world_door[literal_eval(coords)]["directions"][direction] = "You see an open door"

        if door_square["key_needed"] == "no":
            input_orders = door_interact["if_open"].split("\t")
            updater_door(input_orders, world)
            _status = "You opened the door"
            return _status
        else:
            if key_item == door_square["key_needed"]:
                input_orders = door_interact["if_open"].split("\t")
                updater_door(input_orders, world)
                _status = "You opened the door with the {}".format(key_item)
                return _status
            else:
                _status = "That's the wrong key"
                return _status


    def look(self):
        pass


    def neighbour_cells(self):
        pass


    def print_map(self) -> string:
        """Handles the map, and its format"""

        x_axis, y_axis = size
        _printer = []
        _i = x_axis
        
        for _cell in world:
            if world[_cell]["mapping"] != wc.RIM:
                if world[_cell] != world[posit]:
                    _printer.append(InOut.get_print_value(world[_cell]["mapping"]))
                else:
                    _printer.append(InOut.get_print_value(wc.PLAYER))
            else:
                _printer.append(InOut.get_print_value(wc.RIM))

        while _i < len(_printer):
            _printer.insert(_i, "\n")  # Adds linebreaks where needed.
            _i += x_axis + 1

        return "{}".format(''.join(_printer))  # Prints the map out
       

    def __init__(self, world_int: int = 0, init_char_pos: tuple = wc.SPAWN):
        self.all_worlds, self.world_size = InOut.open_file()
        change_world(world_int)
        walk(init_char_pos)


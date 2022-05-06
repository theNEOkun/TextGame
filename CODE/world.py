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


    def describe_place(self):
        """Just takes the description of the place the player currently is in"""
        return self.world[self.char_pos]["description"]["place"] + "\n"


    def get_items(self) -> list:
        return self.curr_square["items"].items()


    def get_item(self, item: string) -> dict:
        if self.curr_square["mapping"] != wc.DOORS:
            item_pool = self.curr_square["items"]
            item = " ".join(inputs[1:])
            _status = pickup(item_pool, item, inventory)
        else:
            _status = "There's nothing to pick up here"

        return _status


    def get_interactions(self) -> list:
        return self.curr_square["interactions"].items()


    def get_interaction(self, interaction: string) -> dict:
        return self.curr_square["interactions"][interaction]


    def look_cardinals(self, cardinal: string):
        return self.curr_square["directions"][cardinal]


    def look_around(self, inventory: Inventory):
        output = str()
        output += square["description"]["place"] + "\n"
        output += "You see:\n"
        for keys, values in self.get_items():
            if inventory.is_in_inventory(keys):  # Can't look at something you already have
                pass
            else:
                output += "{}\n".format(values["desc"])
        output += "You also see:\n"
        for openables, values in self.get_interactions():
            output += "{}\n".format(values["desc"])
        return "{:^}\n".format(output)


    def look_at(self, item:string):
        try:
            if inventory.is_in_inventory(item):  # In case player has an item from the square in his inventory
                return "What do you mean?"
            else:
                return self.get_item(item)["desc"]
        except KeyError:
            return "You can't do that"


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


if __name__ == '__main__':
    pass

import CODE.InputOutput as InOut
import CODE.world_creator as wc

class world:
    all_worlds: dict
    world: dict
    world_size: tuple
    
    char_pos: tuple
    curr_square: dict


    def walk(self, char_pos: tuple = wc.SPAWN):
        self.char_pos = char_pos
        self.curr_square = world[char_pos]


    def change_world(self, world_int: int = 0):
        self.world = world[world_int]


    def interact(self):
        pass


    def look(self):
        pass


    def neighbour_cells(self):
        pass


    def __init__(self):
        self.all_worlds, self.world_size = InOut.open_file()
        change_world()
        walk()


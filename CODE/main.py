from CODE.runner import MainClass
from CODE.world import World
from CODE.char import Char

import CODE.InputOutput as IO
import CODE.world_creator as wc

def load_save(self):
    pass

def main():
    world = World(IO.get_file("world_1.json"))
    char = Char(pos = wc.SPAWN)

    mc = MainClass(world, char)


if __name__ == '__main__':
    main()


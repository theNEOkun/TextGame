import CODE.world_creator as wc
import CODE.InputOutput as IO
from CODE.world import World
from CODE.char import Char

from enum import IntEnum


world: World
char: Char

class Dir(IntEnum):
    UP = 1
    DOWN = -1
    LEFT = -1
    RIGHT = 1


def load_save():
    pass


def walk_char(char: Char, ew: Dir, ns: Dir):
    char.walk(ew, ns)


def main():
    world = World(IO.get_file("world_1.json"))
    char = Char(pos = wc.SPAWN)

    IO.print_to_screen("", world.getMap(str(char.getPos())))


if __name__ == '__main__':
    main()

import CODE.world_creator as wc
import CODE.InputOutput as IO
from CODE.world import World
from CODE.char import Char

from enum import IntEnum
from CODE.char.directions import Directions as Dir


class MainClass(object):

    world: World
    char: Char


    def walk_char(self, ew: Dir, ns: Dir):
        """Used to walk the character, and check if a position is walkable"""
        x_, y_ = self.char.getPos()
        x_ += ew
        y_ += ns
        if self.world.walkableCell((x_, y_)):
            self.char.walk(ew, ns)


    def main_loop(self):
        #IO.print_to_screen(self.char.getPos(), self.world.getMap(self.char.getPos()))
        self.walk_char(Dir.DOWN, Dir.NOT)
        #IO.print_to_screen(self.char.getPos(), self.world.getMap(self.char.getPos()))


    def __init__(self, world: World, char: Char):
        self.world = world
        self.char = char
        self.main_loop()


def load_save(self):
    pass


def main():
    world = World(IO.get_file("world_1.json"))
    char = Char(pos = wc.SPAWN)

    mc = MainClass(world, char)


if __name__ == '__main__':
    main()


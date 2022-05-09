import CODE.world_creator as wc
from CODE.world import World
from CODE.char import Char

from enum import Enum
from CODE.char.directions import Directions as Dir


class MainClass(object):

    world: World
    char: Char


    def walk_char(self, direction: Dir):
        """Used to walk the character, and check if a position is walkable"""
        y_, x_ = self.char.getPos()
        if direction == Dir.UP:
            y_ -= 1
        elif direction == Dir.DOWN:
            y_ += 1
        elif direction == Dir.LEFT:
            x_ -= 1
        elif direction == Dir.RIGHT:
            x_ += 1
        test_cell = (y_, x_)
        if self.world.walkableCell(test_cell):
            self.char.walk(direction)


    def main_loop(self):
        #IO.print_to_screen(self.char.getPos(), self.world.getMap(self.char.getPos()))
        self.walk_char(Dir.DOWN)
        #IO.print_to_screen(self.char.getPos(), self.world.getMap(self.char.getPos()))


    def __init__(self, world: World, char: Char):
        self.world = world
        self.char = char

if __name__ == '__main__':
    pass


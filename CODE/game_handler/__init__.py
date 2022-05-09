import CODE.world_creator as wc
from CODE.world import World
from CODE.char import Char
from CODE.game_handler.command import Command
import CODE.InputOutput as IO

from enum import Enum
from CODE.char.directions import Directions as Dir


class MainClass(object):

    __world: World
    __char: Char


    def walk_char(self, direction: Dir) -> bool:
        """Used to walk the character to a walkable position"""
        y_, x_ = self.__char.getPos()
        if direction == Dir.UP:
            y_ -= 1
        elif direction == Dir.DOWN:
            y_ += 1
        elif direction == Dir.LEFT:
            x_ -= 1
        elif direction == Dir.RIGHT:
            x_ += 1
        test_cell = (y_, x_)
        if self.__world.walkableCell(test_cell):
            self.__char.walk(direction)
            return True
        return False


    def char_pos(self) -> tuple:
        return self.__char.getPos()


    def get_map(self) -> tuple:
        return self.__world.getMap(self.char_pos())


    def walk_command(self, arguments: list) -> str:
        argument = arguments[0]
        direction = Dir.get_direction(argument)
        if not self.walk_char(direction):
            return "You cannot walk there"


    def look_command(self, arguments: list):
        pass


    def checkCommand(self, command: str):
        steps = command.split(" ")
        first_command = steps[0]
        if first_command == "walk" or first_command == "w":
            return Command.WALK, steps[1:]
        if first_command == "look" or first_command == "l":
            return Command.LOOK, steps[1:]
        else:
            return None, None


    def main_loop(self):
        IO.print_to_screen("", self.get_map())
        self.walk_char(Dir.DOWN)
        IO.print_to_screen("", self.get_map())


    def __init__(self, world: World, char: Char):
        self.__world = world
        self.__char = char

if __name__ == '__main__':
    pass

